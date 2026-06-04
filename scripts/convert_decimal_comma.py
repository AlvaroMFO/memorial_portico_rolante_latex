#!/usr/bin/env python3
"""Convert N{,}D decimals to \\num{N.D}; inside \\SI{...}{...} only replace {,} with ."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

# SI value may contain {,} (e.g. 14{,}11) or e-notation (100{,}75e3)
SI_PATTERN = re.compile(
    r"\\SI(\[[^\]]*\])?\{((?:-)?(?:[^{}]|\{,\})+)\}\{([^{}]+)\}"
)

SI_NEG_NUM_FIX = re.compile(
    r"\\SI(\[[^\]]*\])?\{-\s*\\num\{([^}]+)\}\}"
)

DECIMAL_PATTERN = re.compile(
    r"(?<!\\num\{)(?:(\d+)\{,\}(\d+)|(?<![0-9])\{,\}(\d+))"
)

# Repair \\SI{\\num{12.5}} or \\SI{\\num{1.39}e-3} from a previous bad run
SI_NUM_FIX = re.compile(
    r"\\SI(\[[^\]]*\])?\{\\num\{([^}]+)\}([eE][+-]?\d+)?\}"
)


def fix_si(match: re.Match) -> str:
    opt = match.group(1) or ""
    value = match.group(2).replace("{,}", ".")
    unit = match.group(3)
    return f"\\SI{opt}{{{value}}}{{{unit}}}"


def fix_si_num(match: re.Match) -> str:
    opt = match.group(1) or ""
    value = match.group(2) + (match.group(3) or "")
    return f"\\SI{opt}{{{value}}}"


def fix_si_neg_num(match: re.Match) -> str:
    opt = match.group(1) or ""
    value = match.group(2)
    return f"\\SI{opt}{{-{value}}}"


def fix_decimal(match: re.Match) -> str:
    if match.group(1) is not None:
        return f"\\num{{{match.group(1)}.{match.group(2)}}}"
    return f"\\num{{0.{match.group(3)}}}"


def process(text: str) -> str:
    text = SI_NEG_NUM_FIX.sub(fix_si_neg_num, text)
    text = SI_NUM_FIX.sub(fix_si_num, text)
    text = SI_PATTERN.sub(fix_si, text)
    text = DECIMAL_PATTERN.sub(fix_decimal, text)
    text = SI_NUM_FIX.sub(fix_si_num, text)
    text = SI_NEG_NUM_FIX.sub(fix_si_neg_num, text)
    return text


def main() -> None:
    changed = []
    for path in sorted(CONTENT.rglob("*.tex")):
        original = path.read_text(encoding="utf-8")
        updated = process(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed.append(path.relative_to(ROOT))

    print(f"Updated {len(changed)} file(s):")
    for p in changed:
        print(f"  {p}")


if __name__ == "__main__":
    main()
