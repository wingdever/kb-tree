"""lint.py 的回归测试：在临时树里构造最小节点，验证关键规则。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

LINT = Path(__file__).resolve().parents[1] / "scripts" / "lint.py"
FRONT = '''---
description: "demo node"
描述: "演示节点"
name: "Demo Node"
名称: "演示节点"
---

# 演示节点

## 小节

正文出现 RAG 与检索增强生成。

## 参考资料

- 示例来源：https://example.com
'''


class LintTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.demo = self.root / "trees" / "demo"
        self.target = self.demo / "target"
        self.target.mkdir(parents=True)
        (self.target / "target.md").write_text(
            FRONT.replace("演示节点", "目标节点"), encoding="utf-8"
        )
        (self.target / "links.csv").write_text("term,target\n", encoding="utf-8")
        (self.demo / "demo.md").write_text(FRONT, encoding="utf-8")
        (self.demo / "object.json").write_text(json.dumps({
            "realm": "logical", "kind": "event", "generality": "type",
            "canonical": "演示对象", "volatility": "medium", "verify": "示例来源"
        }, ensure_ascii=False), encoding="utf-8")
        (self.demo / "questions.jsonl").write_text(
            json.dumps({"q": "演示问题是什么？", "section": "小节"}, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self.set_links("{RAG|检索增强生成},trees/demo/target\n")

    def tearDown(self):
        self.tmp.cleanup()

    def set_links(self, body):
        (self.demo / "links.csv").write_text("term,target\n" + body, encoding="utf-8")

    def run_lint(self):
        return subprocess.run(
            [sys.executable, str(LINT), str(self.demo)],
            capture_output=True, text=True,
        )

    def assert_lint_error(self, needle):
        proc = self.run_lint()
        self.assertEqual(proc.returncode, 1, proc.stdout + proc.stderr)
        self.assertIn(needle, proc.stdout + proc.stderr)

    def test_valid_group_passes(self):
        proc = self.run_lint()
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)

    def test_group_needs_two_variants(self):
        self.set_links("{RAG},trees/demo/target\n")
        self.assert_lint_error("至少要有两个")

    def test_target_must_exist(self):
        self.set_links("RAG,trees/demo/missing\n")
        self.assert_lint_error("target 目录不存在")

    def test_term_must_appear_in_body(self):
        self.set_links("不存在词,trees/demo/target\n")
        self.assert_lint_error("term 未在正文出现")

    def test_object_enum_rejects_invalid_value(self):
        data = json.loads((self.demo / "object.json").read_text(encoding="utf-8"))
        data["realm"] = "physical"
        (self.demo / "object.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        self.assert_lint_error("realm")

    def test_question_section_must_match_heading(self):
        (self.demo / "questions.jsonl").write_text(
            json.dumps({"q": "演示问题是什么？", "section": "不存在的小节"}, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        self.assert_lint_error("section")


if __name__ == "__main__":
    unittest.main()
