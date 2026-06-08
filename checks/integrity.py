#!/usr/bin/env python
"""Integrity checks for the Working Learning Framework.

Run before committing:  python checks/integrity.py

Checks:
  1. Bibliography — [1]..[N] contiguous (intentional-gap markers count as
     present); every in-text [n] resolves to a bibliography entry.
  2. Title sync — every claim title is character-identical between the
     framework and the compendium, with the same claim roster in both
     (the title is the join key between the two documents).

Exit code 0 = all checks pass; 1 = at least one hard failure.
Orphan bibliography entries (real entries never cited in-text) are reported
as WARNINGS only and do not fail the run.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FRAMEWORK = os.path.join(ROOT, "Working_Learning_Framework.md")
COMPENDIUM = os.path.join(ROOT, "Framework_Compendium.md")

CLAIM_ID = r"R?[TP]\d+[a-z]?"

errors = []
warnings = []


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def check_bibliography(text):
    lines = text.splitlines()
    bib_nums = []
    gap_nums = set()
    for ln in lines:
        m = re.match(r"^\[(\d+)\]\s*(.*)", ln)
        if not m:
            continue
        n = int(m.group(1))
        bib_nums.append(n)
        if "intentional gap" in m.group(2).lower():
            gap_nums.add(n)
    if not bib_nums:
        errors.append("bibliography: no [n] entries found")
        return
    # duplicate entry numbers
    dupes = sorted({n for n in bib_nums if bib_nums.count(n) > 1})
    if dupes:
        errors.append(f"bibliography: duplicate entry numbers {dupes}")
    nums = set(bib_nums)
    hi = max(nums)
    missing = [n for n in range(1, hi + 1) if n not in nums]
    if missing:
        errors.append(f"bibliography: non-contiguous; missing entries {missing}")
    # in-text citations: [n] not at start of a bibliography line
    body = "\n".join(l for l in lines if not re.match(r"^\[\d+\]", l))
    intext = set(int(x) for x in re.findall(r"\[(\d+)\]", body))
    unresolved = sorted(n for n in intext if n not in nums)
    if unresolved:
        errors.append(f"bibliography: in-text cites with no entry {unresolved}")
    # orphans (warning): real entries never cited in-text
    orphans = sorted(n for n in nums if n not in intext and n not in gap_nums)
    if orphans:
        warnings.append(f"bibliography: entries never cited in-text {orphans}")
    print(f"  bibliography: {len(nums)} entries (1..{hi}), "
          f"{len(gap_nums)} intentional gaps, {len(intext)} distinct in-text cites")


def _clean_fw_title(rest):
    # P-claims: "Title -> operationalizes ..." ; drop the arrow clause
    rest = re.split(r"\s+→\s+operationalizes", rest)[0]
    # T-claims: drop trailing "[provenance]" / "[type: ...]"
    rest = re.sub(r"\s*\[[^\]]*\]\s*$", "", rest)
    return rest.strip()


def extract_framework_titles(text):
    out = {}
    for ln in text.splitlines():
        m = re.match(rf"^#{{3,5}}\s+({CLAIM_ID})\.\s+(.*)$", ln)
        if m:
            out[m.group(1)] = _clean_fw_title(m.group(2))
    return out


def extract_compendium_titles(text):
    out = {}
    for ln in text.splitlines():
        m = re.search(rf"\*\*({CLAIM_ID})\.\s+(.*?)\*\*", ln)
        if m and m.group(1) not in out:
            out[m.group(1)] = m.group(2).strip()
    return out


def check_titles(fw_text, co_text):
    fw = extract_framework_titles(fw_text)
    co = extract_compendium_titles(co_text)
    only_fw = sorted(set(fw) - set(co))
    only_co = sorted(set(co) - set(fw))
    if only_fw:
        errors.append(f"title-sync: claims in framework but not compendium {only_fw}")
    if only_co:
        errors.append(f"title-sync: claims in compendium but not framework {only_co}")
    mismatches = []
    for cid in sorted(set(fw) & set(co)):
        if fw[cid] != co[cid]:
            mismatches.append(cid)
            errors.append(f"title-sync [{cid}]:\n    framework:  {fw[cid]!r}\n    compendium: {co[cid]!r}")
    print(f"  title-sync: {len(fw)} framework / {len(co)} compendium claims, "
          f"{len(mismatches)} title mismatches")


def main():
    fw = read(FRAMEWORK)
    co = read(COMPENDIUM)
    print("Running framework integrity checks...")
    check_bibliography(fw)
    check_titles(fw, co)
    if warnings:
        print("\nWARNINGS:")
        for w in warnings:
            print("  ! " + w)
    if errors:
        print("\nFAILED:")
        for e in errors:
            print("  ✗ " + e)
        print(f"\n{len(errors)} error(s).")
        return 1
    print("\nAll checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
