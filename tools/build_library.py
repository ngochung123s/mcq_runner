"""Build data/library.js from data/<id>.json so the app needs no manual import.

Every file in data/ (except library.js) must be one bank in the medmcq-bank v1 format
(see tools/bank_format.py) and be named after its id. Any invalid file stops the build
with the reasons, so a broken bank never reaches the app.

Usage: python tools/build_library.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import bank_format

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "library.js"
PREFIX = "window.MCQ_LIBRARY = "


def load_banks() -> tuple[list[dict], list[str]]:
    banks: list[dict] = []
    errors: list[str] = []
    for path in sorted(DATA.iterdir()):
        if not path.is_file() or path == OUT:
            continue
        # File rác của hệ điều hành / bản tạm của lần build bị ngắt: bỏ qua, không coi là lỗi.
        if path.name.startswith(".") or path.name.lower() in ("desktop.ini", "thumbs.db") or path.suffix == ".tmp":
            continue
        if path.suffix != ".json":
            errors.append(f"{path.name}: data/ chỉ chứa file bộ đề .json (khuôn {bank_format.FORMAT})")
            continue
        try:
            bank = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            errors.append(f"{path.name}: không đọc được JSON ({e})")
            continue
        errs = bank_format.validate(bank)
        if not errs and bank["id"] != path.stem:
            errs.append(f'tên file phải là "{bank["id"]}.json" (trùng "id")')
        if errs:
            errors.extend(f"{path.name}: {e}" for e in errs)
            continue
        banks.append(bank)
    return banks, errors


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    banks, errors = load_banks()
    if errors:
        print("LỖI: file bộ đề không đúng khuôn, chưa dựng thư viện:")
        for e in errors:
            print("  " + e)
        return 1

    # The app reads the library as plain banks; format/version only matter for files.
    library = [{k: v for k, v in b.items() if k not in ("format", "version")} for b in banks]
    old: list[dict] | None = None
    if OUT.exists():
        try:
            old = json.loads(OUT.read_text(encoding="utf-8").strip()[len(PREFIX):].rstrip(";"))["banks"]
        except (ValueError, KeyError):
            old = None
    if library != old:
        payload = {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "banks": library}
        tmp = OUT.with_suffix(".js.tmp")
        tmp.write_text(PREFIX + json.dumps(payload, ensure_ascii=False) + ";\n", encoding="utf-8")
        tmp.replace(OUT)

    by_group: dict[str, list[dict]] = {}
    for b in library:
        by_group.setdefault(b["group"], []).append(b)
    total = sum(len(b["questions"]) for b in library)
    print(f"Thư viện: {len(library)} bộ đề, {total} câu → {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1e6:.1f} MB)")
    for g, bs in sorted(by_group.items()):
        print(f"  {g}: {len(bs)} bộ, {sum(len(b['questions']) for b in bs)} câu")
    return 0


if __name__ == "__main__":
    sys.exit(main())
