---
description: "BPE, WordPiece, Unigram, SentencePiece and tokenizer design"
描述: "BPE、WordPiece、Unigram、SentencePiece 原理与分词器设计"
name: "Tokenizers"
名称: "分词器"
---

# M1 分词器（Tokenizer）

分词把文本切成模型能处理的基本单元（token）。它是 LLM 流水线的第一环，决定了词表大小、序列长度、覆盖能力与多语言表现。

## 为什么需要子词分词

- 词级（word-level）：词表巨大、无法处理未见词、稀有词稀疏。
- 字符级（char-level）：序列过长、语义粒度太细。
- **子词（subword）**：在两者之间取平衡——常见词保留为整体，罕见词拆成有意义的片段。主流 LLM 全部使用子词分词。

## 四种算法对照

| 算法 | 词表构建 | 合并/切分准则 | 新文本分词方式 | 多语言 | 代表模型 |
|---|---|---|---|---|---|
| **BPE** | 自底向上 | 合并频率最高的相邻对 | 按学习到的顺序重放合并 | 一般 | GPT-2~GPT-5、Llama 3、Qwen、Mistral、DeepSeek |
| **WordPiece** | 自底向上 | 合并使训练数据似然提升最大的对 | 贪心最长匹配，`##` 标记续接 | 英语为主 | BERT、DistilBERT、ELECTRA |
| **Unigram** | 自顶向下 | 从大词表逐步删除使似然损失最小的子词 | 取概率最大的切分（Viterbi） | 优 | T5、XLM-RoBERTa、ALBERT |
| **SentencePiece** | 框架（内含 BPE/Unigram） | 视具体算法 | 可逆、无需预分词 | 优 | LLaMA、T5、Gemma 3 |

## BPE（Byte-Pair Encoding）

流程（自底向上贪心合并）：

1. 从字符开始：`['h','e','l','l','o']`
2. 找频率最高的相邻对：`('l','l')` → 合并为 `ll`
3. 得到 `['h','e','ll','o']`
4. 重复直到词表达到目标大小。

- **优点**：训练/推理快、压缩率高、对代码友好、通过子词处理罕见词。
- **缺点**：贪心合并，可能把常见词切得很怪；无概率打分。
- **字节级 BPE（GPT-2 起）**：先把文本编码为 UTF-8 字节再合并，好处是**没有 UNK、全覆盖**，代价是非拉丁文字序列更长。

### 从零实现最小 BPE

```python
import re
from collections import Counter, defaultdict

def preprocess_text(text):
    return re.findall(r"\w+|[^\w\s]", text.lower())

def build_initial_vocab(tokens):
    vocab = Counter()
    for token in tokens:
        vocab[" ".join(list(token)) + " "] += 1
    return vocab

def get_pair_frequencies(vocab):
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[(symbols[i], symbols[i + 1])] += freq
    return pairs

def merge_vocab(pair, vocab):
    merged = "".join(pair)
    pattern = re.compile(r"(?<!\S)" + re.escape(" ".join(pair)) + r"(?!\S)")
    new_vocab = Counter()
    for word, freq in vocab.items():
        new_vocab[pattern.sub(merged, word)] += freq
    return new_vocab

def train_bpe(tokens, num_merges=50):
    vocab = build_initial_vocab(tokens)
    merges = []
    for _ in range(num_merges):
        pairs = get_pair_frequencies(vocab)
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        vocab = merge_vocab(best, vocab)
        merges.append(best)
    return merges
```

这段代码的价值在于把"合并如何被学习"可视化——高频模式（如 `tion`）会先成为 token。改变 `num_merges` 观察切分变化，是理解词表权衡的最佳练习。

### 生产实现（HuggingFace tokenizers）

```python
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders, processors

tokenizer = Tokenizer(models.BPE())
tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
tokenizer.decoder = decoders.ByteLevel()
tokenizer.post_processor = processors.ByteLevel(trim_offsets=False)
trainer = trainers.BpeTrainer(
    vocab_size=32000, min_frequency=2,
    special_tokens=["<pad>", "<unk>", "<bos>", "<eos>"],
    initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
)
tokenizer.train(["corpus.txt"], trainer)
tokenizer.save("tokenizer.json")
```

## WordPiece

与 BPE 类似但选合并对的标准不同——选**使训练数据似然提升最大**的对。常用近似打分：

```
score(a, b) = count(ab) / (count(a) × count(b))
```

它偏好"共同出现得比偶然预期更频繁"的相邻片段。用 `##` 标记非词首子词，如 `unaffable → un ##aff ##able`。分词时贪心最长匹配优先。

示例对比（同一玩具语料）：BPE 第一次合并 `e+s`（频次 9）；WordPiece 选 `i+d`（出现 3 次，i、d 各出现 3 次，score=3/(3×3)=0.33），而 `e+s` 只有 9/(17×9)=0.06，因为 e 太常见。WordPiece 偏好"紧密排他"的片段而非" merely common"。

## Unigram

由 Taku Kudo 2018 提出，方向相反——**自顶向下剪枝**：

1. 先构造一个很大的候选词表。
2. 每个子词有概率，切分 S 的概率为各子词概率之积 `P(S)=∏p(t)`。
3. 用 EM 估计概率，反复删除"删掉后对语料似然影响最小"的子词，直到目标大小。
4. 分词时用 Viterbi 找概率最大的切分，而非重放合并。

因为保留概率，Unigram 可以在训练时**采样多种切分**（subword regularization），提升对切分方式的鲁棒性。更适合多语言与形态丰富的语言。

## SentencePiece

SentencePiece 是**工具库/框架**（Kudo & Richardson 2018），不是第四种算法——它内部可跑 BPE 或 Unigram。关键特性：

- 直接处理原始文本，**无需预分词**（不需要按空格切词）。
- 把空格当作普通字符，用 `▁` 表示词首空格 → 中文、日文等无空格语言也能直接用。
- 所有字符显式编码，分词**可逆**（token 拼接即可还原原文）。
- 支持 byte fallback，避免真正的 OOV。

```python
import sentencepiece as spm
spm.SentencePieceTrainer.train(
    input="corpus.txt", model_prefix="sp", vocab_size=32000,
    model_type="unigram",            # 或 "bpe"
    character_coverage=0.9995,       # 拉丁为主可设 1.0
    byte_fallback=True,
    pad_id=0, unk_id=1, bos_id=2, eos_id=3,
)
sp = spm.SentencePieceProcessor(model_file="sp.model")
sp.encode("Hello world", out_type=str)   # ['▁Hello', '▁world']
```

T5、XLM-RoBERTa 用 Unigram SentencePiece 词表；Gemma 3 用 SentencePiece BPE。

## 词表大小怎么选

| 词表大小 | token 产出率 | 训练成本 | 适用 |
|---|---|---|---|
| 8K–16K | 高（每词更多 token） | 低 | 小模型、单语言 |
| 32K | 均衡 | 中 | 通用单语（BERT、GPT-2） |
| 50K–64K | 较低 | 中高 | 大型单语 LLM |
| 100K–128K | 低 | 高 | 多语言 |
| 200K+ | 极低 | 很高 | 超大多语言（Gemma） |

原则：词表越大，同一段文本 token 越少（序列越短、推理越省），但embedding 表和 softmax 越大、训练成本越高。

## 扩展已有分词器（领域适配）

```python
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(base_model)
num_added = tok.add_tokens(["<.domain_token>", "..."])
# 必须同步 resize model embeddings：model.resize_token_embeddings(len(tok))
```

添加领域 token 前先看 token fertility（切分效率）；加完必须 resize 模型 embedding，并重新训练这些新 token 的表示。

## 实践要点

- 先跑最小 BPE 实现理解机制，再上生产库——否则切分权衡是黑箱。
- 字节级 BPE 是当前 decoder-only LLM 主流（覆盖全、无 UNK）。
- 分词器要与模型配套；用错 chat template 或与基座不匹配的词表会静默破坏效果。
- 分词影响 token 频率分布、标点/空格处理乃至推理成本，不是纯工程细节。

## 参考资料

- Neural Machine Translation of Rare Words with Subword Units（BPE）：https://arxiv.org/abs/1508.07909
- Subword Regularization: Improving Neural Network Translation Models with Multiple Subword Candidates（Unigram / SentencePiece）：https://arxiv.org/abs/1804.10959
- Google's Neural Machine Translation System（WordPiece）：https://arxiv.org/abs/1609.08144
