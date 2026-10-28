"""Khuôn file bộ đề duy nhất của MedMCQ: medmcq-bank v1 (1 file = 1 bộ đề, tên file = <id>.json).

{
  "format": "medmcq-bank", "version": 1,
  "id": "bank_ped40_hoi_chung_than_hu",      # duy nhất, trùng tên file
  "lesson": "PED-40",                         # mã bài, "" nếu không có
  "group": "Nhi khoa",                        # một trong GROUPS
  "title": "...", "description": "...",
  "updated": "2026-10-27T15:03:40Z",          # ISO 8601 UTC; bản mới hơn thắng khi trùng id
  "questions": [{
    "id": "PED40-A01",                        # duy nhất trong bộ; lịch sử làm bài bám theo id này
    "text": "...", "options": ["...", ...],   # 2–6 phương án
    "correct": 0,                             # chỉ số phương án đúng, đếm từ 0
    "explanation": "...",
    # tùy chọn:
    "option_explanations": [...],             # cùng số phần tử với options
    "type": "vignette|concept|calc", "topic": "...", "subtopic": "...",
    "bloom": "...", "difficulty": 1|2|3, "source": "..."
  }]
}

index.html (BankFormat) kiểm tra đúng các luật này khi nhập và khi xuất; sửa luật thì sửa cả hai nơi.
"""
from __future__ import annotations

import json
import re
from datetime import datetime

FORMAT = "medmcq-bank"
VERSION = 1
GROUPS = ("Nhi khoa", "Nội khoa", "Sản phụ khoa", "Ngoại khoa", "Khác")
TYPES = ("vignette", "concept", "calc")
BANK_KEYS = ("format", "version", "id", "lesson", "group", "title", "description", "updated", "questions")
QUESTION_KEYS = ("id", "type", "topic", "subtopic", "bloom", "difficulty", "source",
                 "text", "options", "correct", "explanation", "option_explanations")
QUESTION_REQUIRED = ("id", "text", "options", "correct", "explanation")
TEXT_FIELDS = ("topic", "subtopic", "bloom", "source")
# Same pattern as BankFormat.ISO_RE in index.html (JS Date.toISOString() output passes).
ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$")


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _iso(v) -> bool:
    if not isinstance(v, str) or not ISO_RE.match(v):
        return False
    try:
        datetime.fromisoformat(v.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def validate(bank) -> list[str]:
    """Danh sách lỗi (rỗng = hợp lệ)."""
    if not isinstance(bank, dict) or bank.get("format") != FORMAT:
        return [f'không phải file bộ đề {FORMAT} (thiếu "format": "{FORMAT}")']
    if type(bank.get("version")) is not int or bank["version"] != VERSION:
        return [f'khuôn {FORMAT} phiên bản {json.dumps(bank.get("version"))} chưa hỗ trợ (app đọc version {VERSION})']
    errs: list[str] = []
    extra = [k for k in bank if k not in BANK_KEYS]
    if extra:
        errs.append(f"trường lạ ở cấp bộ đề: {', '.join(extra)}")
    for k in ("id", "title"):
        if not _nonempty_str(bank.get(k)):
            errs.append(f'"{k}" phải là chuỗi không rỗng')
    for k in ("lesson", "description"):
        if not isinstance(bank.get(k), str):
            errs.append(f'"{k}" phải là chuỗi (có thể rỗng)')
    if bank.get("group") not in GROUPS:
        errs.append(f'"group" phải là một trong: {", ".join(GROUPS)}')
    if not _iso(bank.get("updated")):
        errs.append('"updated" phải là thời điểm ISO, vd 2026-10-29T08:00:00Z')
    qs = bank.get("questions")
    if not isinstance(qs, list) or not qs:
        errs.append('"questions" phải là danh sách có ít nhất 1 câu')
        return errs
    seen: set[str] = set()
    for i, q in enumerate(qs, 1):
        where = f"câu {i}"
        if not isinstance(q, dict):
            errs.append(f"{where}: không phải object")
            continue
        if _nonempty_str(q.get("id")):
            where += f" ({q['id']})"
            if q["id"] in seen:
                errs.append(f"{where}: trùng id")
            seen.add(q["id"])
        for k in QUESTION_REQUIRED:
            if k not in q:
                errs.append(f'{where}: thiếu "{k}"')
        extra = [k for k in q if k not in QUESTION_KEYS]
        if extra:
            errs.append(f"{where}: trường lạ {', '.join(extra)}")
        if "id" in q and not _nonempty_str(q["id"]):
            errs.append(f'{where}: "id" phải là chuỗi không rỗng')
        if "text" in q and not _nonempty_str(q["text"]):
            errs.append(f'{where}: "text" rỗng')
        opts = q.get("options")
        n = len(opts) if isinstance(opts, list) else 0
        if "options" in q and (not 2 <= n <= 6 or not all(_nonempty_str(o) for o in opts)):
            errs.append(f'{where}: "options" phải có 2–6 phương án không rỗng')
        c = q.get("correct")
        if "correct" in q and (not isinstance(c, int) or isinstance(c, bool) or not 0 <= c < max(n, 1)):
            errs.append(f'{where}: "correct" phải là số từ 0 đến {max(n - 1, 0)}')
        if "explanation" in q and not isinstance(q["explanation"], str):
            errs.append(f'{where}: "explanation" phải là chuỗi')
        oe = q.get("option_explanations")
        if oe is not None and (not isinstance(oe, list) or len(oe) != n or not all(isinstance(s, str) for s in oe)):
            errs.append(f'{where}: "option_explanations" phải có đúng {n} chuỗi')
        if "type" in q and q["type"] not in TYPES:
            errs.append(f'{where}: "type" phải là một trong {", ".join(TYPES)}')
        d = q.get("difficulty")
        if d is not None and (isinstance(d, bool) or d not in (1, 2, 3)):
            errs.append(f'{where}: "difficulty" phải là 1, 2 hoặc 3')
        for k in TEXT_FIELDS:
            if k in q and not isinstance(q[k], str):
                errs.append(f'{where}: "{k}" phải là chuỗi')
    return errs


def canonical(bank: dict) -> dict:
    """Sắp xếp trường theo thứ tự chuẩn (để file giống hệt nhau dù ai tạo ra)."""
    out = {k: bank[k] for k in BANK_KEYS if k in bank}
    out["questions"] = [{k: q[k] for k in QUESTION_KEYS if k in q} for q in bank["questions"]]
    return out
