"""Build data/library.js from every bank JSON in data/ so the app needs no manual import.

- Reads data/*.json in any of the app's formats: single bank, list of banks, or
  sync/backup file {banks: [...]}. Skips files whose name contains "BACKUP".
- The same bank id often appears in several master files with different sizes;
  the version with the most questions wins, then the newest file.
- Adds `group` (chuyên khoa) and `lesson` (e.g. IM-53b, PED-62) for the library view,
  and `updated` from the file time when the bank has none.

Usage: python tools/build_library.py
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "library.js"

GROUPS = [
    (re.compile(r"^(PED|NHI)\b", re.I), "Nhi khoa"),
    (re.compile(r"^(IM|NK|NOI)\b", re.I), "Nội khoa"),
    (re.compile(r"^(SK|OB|SAN)\b", re.I), "Sản phụ khoa"),
    (re.compile(r"^(SG|NGOAI)\b", re.I), "Ngoại khoa"),
]
LESSON_RE = re.compile(r"^\s*([A-Z]{2,4})[-\s]?(\d{1,3}[a-z]?)\b")


def lesson_code(bank: dict) -> str:
    m = LESSON_RE.match(bank.get("title", ""))
    return f"{m.group(1)}-{m.group(2)}" if m else ""


def group_of(code: str) -> str:
    for pat, name in GROUPS:
        if code and pat.match(code):
            return name
    return "Khác"


def banks_in(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("banks"), list):
        data = data["banks"]
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        return []
    return [b for b in data if isinstance(b, dict) and b.get("id") and isinstance(b.get("questions"), list) and b["questions"]]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    # id -> (rank, bank, file name, file mtime). Rank does not use mtime, so the choice
    # survives git checkouts: most questions, then a dedicated single-bank file over a
    # master file, then file name.
    best: dict[str, tuple[tuple, dict, str, float]] = {}
    variants: dict[str, dict[str, list[str]]] = {}  # id -> question-content fingerprint -> files
    for path in sorted(DATA.glob("*.json")):
        if "backup" in path.name.lower():
            continue
        try:
            found = banks_in(path)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"BỎ QUA {path.name}: không đọc được JSON ({e})")
            continue
        mtime = path.stat().st_mtime
        for bank in found:
            rank = (len(bank["questions"]), len(found) == 1, path.name)
            fp = json.dumps([[q.get("text"), q.get("options"), q.get("correct")] for q in bank["questions"]], ensure_ascii=False)
            variants.setdefault(bank["id"], {}).setdefault(fp, []).append(path.name)
            cur = best.get(bank["id"])
            if cur is None or rank > cur[0]:
                best[bank["id"]] = (rank, bank, path.name, mtime)

    for bid, fps in sorted(variants.items()):
        if len(fps) > 1:
            chosen = best[bid][2]
            others = sorted(f for files in fps.values() if chosen not in files for f in files)
            print(f"CHÚ Ý {bid}: {len(fps)} phiên bản khác nhau; dùng {chosen} ({len(best[bid][1]['questions'])} câu), bản khác bị bỏ: {', '.join(others)}")

    prefix = "window.MCQ_LIBRARY = "
    old_banks: dict[str, dict] = {}
    if OUT.exists():
        try:
            old_banks = {b["id"]: b for b in json.loads(OUT.read_text(encoding="utf-8").strip()[len(prefix):].rstrip(";"))["banks"]}
        except (ValueError, KeyError):
            old_banks = {}

    library = []
    for _, (rank, bank, fname, mtime) in sorted(best.items()):
        code = lesson_code(bank)
        entry = dict(bank)
        entry["lesson"] = code
        entry["group"] = bank.get("group") or group_of(code)
        entry["source_file"] = fname
        if "updated" not in bank:
            # Keep the previous timestamp while the content is unchanged, so a git checkout
            # (new file mtimes) does not make every bank look "newer" to the app.
            old = old_banks.get(bank["id"])
            same = old is not None and {k: v for k, v in old.items() if k != "updated"} == entry
            entry["updated"] = old["updated"] if same else datetime.fromtimestamp(mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        library.append(entry)

    if library != list(old_banks.values()):
        payload = {"generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "banks": library}
        tmp = OUT.with_suffix(".js.tmp")
        tmp.write_text(prefix + json.dumps(payload, ensure_ascii=False) + ";\n", encoding="utf-8")
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
