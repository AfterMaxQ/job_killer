#!/usr/bin/env python3
"""Deterministic validation for one build-resume task directory.

This script intentionally validates only mechanical invariants. It does not try to
judge whether a claim is semantically exaggerated; that remains the Agent's job.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from collections import Counter
from pathlib import Path

REQUIRED_FILES = (
    "job-model.md",
    "match-matrix.md",
    "positioning.md",
    "resume.md",
    "claim-audit.md",
)

PLACEHOLDER_PATTERNS = (
    re.compile(r"\bTODO\b", re.IGNORECASE),
    re.compile(r"\bTBD\b", re.IGNORECASE),
    re.compile(r"<\s*placeholder\s*>", re.IGNORECASE),
    re.compile(r"⟨[^⟩]+⟩"),
)

BANNED_MASTERY_TERMS = ("精通", "专家级", "熟练掌握")
TEMP_SUFFIXES = (".aux", ".log", ".out", ".toc", ".synctex.gz")
RESOLVED_UNSUPPORTED_MARKERS = ("删除", "已删除", "removed", "delete")
RESOLVED_CONFIRMATION_MARKERS = ("已确认", "确认后保留", "删除", "已删除", "弱化", "removed")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _has_h1(text: str) -> bool:
    return any(line.startswith("# ") for line in text.splitlines())


def _validate_placeholders(text: str, source: str) -> list[str]:
    errors: list[str] = []
    for pattern in PLACEHOLDER_PATTERNS:
        match = pattern.search(text)
        if match:
            errors.append(f"placeholder remains in {source}: {match.group(0)}")
    return errors


def _validate_mastery_terms(text: str) -> list[str]:
    errors: list[str] = []
    for term in BANNED_MASTERY_TERMS:
        if term in text:
            errors.append(f"banned mastery wording in resume.md: {term}")
    return errors


def _validate_duplicate_bullets(text: str) -> list[str]:
    bullets = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            normalized = re.sub(r"\s+", " ", stripped[2:].strip())
            if normalized:
                bullets.append(normalized)
    counts = Counter(bullets)
    return [f"duplicate bullet in resume.md: {bullet}" for bullet, count in counts.items() if count > 1]


def _claim_blocks(text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"(?m)^##\s+(C[^\n]*)\s*$", text))
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append((match.group(1).strip(), text[start:end]))
    return blocks


def _validate_claim_audit(text: str) -> list[str]:
    errors: list[str] = []
    for claim_id, block in _claim_blocks(text):
        lower = block.lower()
        if "UNSUPPORTED" in block and not any(marker.lower() in lower for marker in RESOLVED_UNSUPPORTED_MARKERS):
            errors.append(f"unresolved UNSUPPORTED claim: {claim_id}")
        if "NEEDS_CONFIRMATION" in block and not any(marker.lower() in lower for marker in RESOLVED_CONFIRMATION_MARKERS):
            errors.append(f"unresolved NEEDS_CONFIRMATION claim: {claim_id}")
    return errors


def _validate_temp_files(directory: Path, label: str) -> list[str]:
    errors: list[str] = []
    if not directory.is_dir():
        return errors
    for child in directory.iterdir():
        if not child.is_file():
            continue
        name = child.name.lower()
        if any(name.endswith(suffix) for suffix in TEMP_SUFFIXES):
            errors.append(f"LaTeX temporary file remains in {label}: {child.name}")
    return errors


def validate_task_dir(path: Path) -> list[str]:
    root = Path(path)
    errors: list[str] = []

    if not root.is_dir():
        return [f"task directory does not exist: {root}"]

    for name in REQUIRED_FILES:
        file_path = root / name
        if not file_path.is_file():
            errors.append(f"missing required file: {name}")
            continue
        text = _read(file_path)
        if not text.strip():
            errors.append(f"required file is empty: {name}")
        elif not _has_h1(text):
            errors.append(f"required markdown file must contain a level-1 heading: {name}")
        errors.extend(_validate_placeholders(text, name))

    resume = root / "resume.md"
    if resume.is_file():
        resume_text = _read(resume)
        errors.extend(_validate_mastery_terms(resume_text))
        errors.extend(_validate_duplicate_bullets(resume_text))

    audit = root / "claim-audit.md"
    if audit.is_file():
        errors.extend(_validate_claim_audit(_read(audit)))

    errors.extend(_validate_temp_files(root, "task directory"))

    cwd = Path.cwd().resolve()
    try:
        same_dir = cwd == root.resolve()
    except OSError:
        same_dir = False
    if not same_dir:
        errors.extend(_validate_temp_files(cwd, "current working directory"))

    return errors


def validate_pdf(pdf_path: Path) -> tuple[list[str], list[str]]:
    pdf = Path(pdf_path)
    errors: list[str] = []
    warnings: list[str] = []

    if not pdf.is_file():
        return [f"PDF does not exist: {pdf}"], warnings
    if pdf.stat().st_size == 0:
        return [f"PDF is empty: {pdf}"], warnings

    header = pdf.read_bytes()[:5]
    if header != b"%PDF-":
        errors.append(f"file does not have a PDF header: {pdf}")
        return errors, warnings

    pdfinfo = shutil.which("pdfinfo")
    if not pdfinfo:
        warnings.append("pdfinfo is unavailable; PDF page count was not verified")
        return errors, warnings

    result = subprocess.run(
        [pdfinfo, str(pdf)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        warnings.append("pdfinfo could not read page count; file existence/header checks passed")
        return errors, warnings

    match = re.search(r"(?m)^Pages:\s+(\d+)\s*$", result.stdout)
    if not match:
        warnings.append("pdfinfo returned no page count")
        return errors, warnings

    pages = int(match.group(1))
    if pages < 1:
        errors.append("PDF page count must be at least 1")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a build-resume task directory")
    parser.add_argument("task_dir", type=Path, help="temp_resume/<company>-<role> directory")
    parser.add_argument("--pdf", type=Path, help="optional generated PDF to validate")
    args = parser.parse_args()

    errors = validate_task_dir(args.task_dir)
    warnings: list[str] = []
    if args.pdf is not None:
        pdf_errors, pdf_warnings = validate_pdf(args.pdf)
        errors.extend(pdf_errors)
        warnings.extend(pdf_warnings)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")

    if errors:
        print(f"Validation failed with {len(errors)} error(s).")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
