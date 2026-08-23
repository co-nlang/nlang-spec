#!/usr/bin/env python3
"""TAG_REGISTRY ↔ 引擎 標籤盤點（符合性量測，不是規範）。

用法:
    python3 scripts/error-code-inventory.py --engine-src ../nlang-tools/crates
    python3 scripts/error-code-inventory.py --engine-src ../nlang-tools/crates --md

規格側讀 spec/zh_TW/TAG_REGISTRY.md 的表格列；引擎側用**四種掃描形狀**，
因為掃描的形狀決定了它看得見什麼：

  enum      — 出現在 cause 列舉的標籤對映裡（`BottomCause::X => "#x"` 之類）
  literal   — 以字串字面值出現在非註解的程式行
  comment   — 只在註解裡出現
  absent    — 四種形狀都找不到

`enum` 是最強的證據（引擎有一個名字叫它）；`literal` 次之（某處會印出它）；
`comment` 表示有人提過但沒有程式路徑；`absent` 表示規格自己在說話。

**本檔輸出的是某一版引擎的事實，不是規範。** 規範在 TAG_REGISTRY.md；
本輸出的歸屬是 meta/ENGINE_SYNC.md（用戶裁定 2026-07-28：符合性量測不進規格正文）。
"""
import argparse
import os
import re
import sys

SPEC_FILE = "spec/zh_TW/TAG_REGISTRY.md"
ROW_RE = re.compile(r"^\|\s*\*\*`(#[a-z_0-9]+)`\*\*\s*\|")
SEC_RE = re.compile(r"^###\s+(\d+\.\d+)\s+(.+?)\s*$")


def spec_rows(path):
    """[(section, heading, tag)] in document order."""
    rows, sec = [], ("?", "?")
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = SEC_RE.match(line)
            if m:
                sec = (m.group(1), m.group(2))
                continue
            m = ROW_RE.match(line)
            if m:
                rows.append((sec[0], sec[1], m.group(1)))
    return rows


def read_engine(src):
    """Return (all_text, code_only_text, enum_tags)."""
    all_parts, code_parts = [], []
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ("target", ".git")]
        for fn in files:
            if not fn.endswith(".rs"):
                continue
            with open(os.path.join(root, fn), encoding="utf-8", errors="replace") as f:
                text = f.read()
            all_parts.append(text)
            code_parts.append(
                "\n".join(l for l in text.split("\n") if not l.lstrip().startswith("//"))
            )
    all_text = "\n".join(all_parts)
    code_text = "\n".join(code_parts)
    # Carrier-aware: only the enums that actually carry a `%cause`, by
    # qualified match arm `BottomCause::FuelExhausted => "#fuel_exhausted"`.
    # A bare `Variant => "..."` scan also picks up weekday names and log
    # levels — measured, and that is why this is qualified.
    carriers = {}
    arm = re.compile(r"\b(BottomCause|BlurCause)::(\w+)\s*(?:\(.*?\))?\s*=>\s*(?:b)?\"(#?[a-z_0-9]+)\"")
    for m in arm.finditer(code_text):
        tag = m.group(3)
        tag = tag if tag.startswith("#") else "#" + tag
        carriers.setdefault(tag, set()).add(m.group(1))
    # Caused Top hangs its cause on a bare string.
    for m in re.finditer(r"Value::TopCaused\s*\{\s*cause:\s*\"([a-z_0-9]+)\"", code_text):
        carriers.setdefault("#" + m.group(1), set()).add("TopCaused")
    enum_tags = set(carriers)
    return all_text, code_text, enum_tags, carriers


def classify(tag, all_text, code_text, enum_tags):
    if tag in enum_tags:
        return "enum"
    bare = '"' + tag[1:] + '"'
    if tag in code_text or bare in code_text:
        return "literal"
    if tag in all_text or bare in all_text:
        return "comment"
    return "absent"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--engine-src", required=True, help="path to nlang-tools/crates")
    ap.add_argument("--md", action="store_true", help="emit a markdown table")
    args = ap.parse_args()

    if not os.path.isdir(args.engine_src):
        sys.exit(f"[FATAL] engine source not found: {args.engine_src}")
    if not os.path.exists(SPEC_FILE):
        sys.exit(f"[FATAL] run from the nlang-spec root ({SPEC_FILE} not found)")

    rows = spec_rows(SPEC_FILE)
    all_text, code_text, enum_tags, carriers = read_engine(args.engine_src)

    # CONTROL: a tag that must classify as `enum`, and one that must be `absent`.
    ctl_present = classify("#conflict", all_text, code_text, enum_tags)
    ctl_absent = classify("#definitely_not_a_real_tag", all_text, code_text, enum_tags)
    if ctl_present != "enum" or ctl_absent != "absent":
        sys.exit(
            f"[FATAL] controls failed (#conflict={ctl_present}, "
            f"bogus={ctl_absent}) — the scan is not measuring what it claims"
        )

    verdicts = [(s, h, t, classify(t, all_text, code_text, enum_tags)) for s, h, t in rows]

    # engine-side tags the spec never documents
    documented = {t for _, _, t in rows}
    undocumented = sorted(t for t in enum_tags if t not in documented)

    def carrier_of(tag):
        return "/".join(sorted(carriers.get(tag, []))) or "—"

    if args.md:
        print("| 標籤 | 節 | 引擎 | 載體 |")
        print("| :-- | :-- | :-- | :-- |")
        for s, _h, t, v in verdicts:
            print(f"| `{t}` | §{s} | {v} | {carrier_of(t)} |")
    else:
        for s, _h, t, v in verdicts:
            print(f"{v:8} §{s:4} {t:32} {carrier_of(t)}")

    counts = {}
    for _s, _h, _t, v in verdicts:
        counts[v] = counts.get(v, 0) + 1
    print("\n--- Summary ---", file=sys.stderr)
    print(f"TAG_REGISTRY 列數 = {len(rows)}", file=sys.stderr)
    for k in ("enum", "literal", "comment", "absent"):
        print(f"  {k:8} {counts.get(k, 0)}", file=sys.stderr)
    print(f"引擎列舉中而 TAG_REGISTRY 未收錄 = {len(undocumented)}", file=sys.stderr)
    for t in undocumented:
        print(f"    {t}", file=sys.stderr)


if __name__ == "__main__":
    main()
