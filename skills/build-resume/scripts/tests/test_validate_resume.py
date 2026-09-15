import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "validate-resume.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_resume", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateResumeTests(unittest.TestCase):
    def make_valid_task(self):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        (root / "job-model.md").write_text("# 岗位模型\n\n## 招聘目标\n虚构岗位。\n", encoding="utf-8")
        (root / "match-matrix.md").write_text(
            "# 岗位能力 × 候选人证据\n\n| 能力 | JD重要度 | 最强证据 | 证据强度 | 策略 |\n|---|---:|---|---:|---|\n| 数据分析 | 4 | 项目/E1 | 3 | 强调 |\n",
            encoding="utf-8",
        )
        (root / "positioning.md").write_text(
            "# 本次简历定位\n\n## Target Identity\n数据分析实习候选人。\n",
            encoding="utf-8",
        )
        (root / "resume.md").write_text(
            "# 虚构候选人\n\n## 核心能力\n\n- 数据分析：SQL、Python；完成课程项目数据清洗。\n",
            encoding="utf-8",
        )
        (root / "claim-audit.md").write_text(
            "# Claim Audit\n\n## C1\n\n### 判断\n\nFACT\n\n### 处理\n\n保留\n",
            encoding="utf-8",
        )
        return td, root

    def test_minimal_valid_task_directory_passes(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        self.assertEqual([], validator.validate_task_dir(root))

    def test_missing_required_file_fails(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        (root / "positioning.md").unlink()
        errors = validator.validate_task_dir(root)
        self.assertTrue(any("positioning.md" in error for error in errors))

    def test_placeholder_is_rejected(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        (root / "resume.md").write_text("# 虚构候选人\n\nTODO: 补充项目\n", encoding="utf-8")
        errors = validator.validate_task_dir(root)
        self.assertTrue(any("placeholder" in error.lower() for error in errors))

    def test_banned_mastery_word_is_rejected(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        (root / "resume.md").write_text("# 虚构候选人\n\n- 精通 Python\n", encoding="utf-8")
        errors = validator.validate_task_dir(root)
        self.assertTrue(any("精通" in error for error in errors))

    def test_duplicate_bullet_is_rejected(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        duplicate = "- 完成数据清洗与指标分析\n"
        (root / "resume.md").write_text("# 虚构候选人\n\n" + duplicate + duplicate, encoding="utf-8")
        errors = validator.validate_task_dir(root)
        self.assertTrue(any("duplicate bullet" in error.lower() for error in errors))

    def test_unresolved_unsupported_claim_is_rejected(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        (root / "claim-audit.md").write_text(
            "# Claim Audit\n\n## C1\n\n### 判断\n\nUNSUPPORTED\n\n### 处理\n\n待处理\n",
            encoding="utf-8",
        )
        errors = validator.validate_task_dir(root)
        self.assertTrue(any("unsupported" in error.lower() for error in errors))

    def test_deleted_unsupported_claim_is_allowed(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        (root / "claim-audit.md").write_text(
            "# Claim Audit\n\n## C1\n\n### 判断\n\nUNSUPPORTED\n\n### 处理\n\n删除\n",
            encoding="utf-8",
        )
        self.assertEqual([], validator.validate_task_dir(root))

    def test_pdf_missing_is_rejected_when_requested(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        errors, warnings = validator.validate_pdf(root / "missing.pdf")
        self.assertTrue(any("pdf" in error.lower() for error in errors))
        self.assertEqual([], warnings)

    def test_nonempty_pdf_file_passes_existence_check(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        pdf = root / "resume.pdf"
        pdf.write_bytes(b"%PDF-1.4\n% fictional fixture\n")
        errors, warnings = validator.validate_pdf(pdf)
        self.assertEqual([], errors)
        self.assertIsInstance(warnings, list)

    def test_latex_temp_file_is_rejected(self):
        validator = load_validator()
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        (root / "resume.aux").write_text("fixture", encoding="utf-8")
        errors = validator.validate_task_dir(root)
        self.assertTrue(any(".aux" in error for error in errors))

    def test_cli_returns_nonzero_for_invalid_task(self):
        td, root = self.make_valid_task()
        self.addCleanup(td.cleanup)
        (root / "resume.md").write_text("# 虚构候选人\n\n- 专家级 SQL\n", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(MODULE_PATH), str(root)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("专家级", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
