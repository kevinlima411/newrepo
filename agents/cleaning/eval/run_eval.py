#!/usr/bin/env python3
"""
Live eval: runs every row of labeled_sms.csv through Haiku and reports accuracy.

  python agents/cleaning/eval/run_eval.py
  python agents/cleaning/eval/run_eval.py --csv my_real_export.csv --threshold 0.7

CSV columns: id, case_type, expected, message, history
  expected: one category, or several joined by "|" when more than one is acceptable
  history:  empty, or a JSON list of strings / {"role", "text"} objects
Cost: ~30 Haiku calls per run, well under $0.05.
"""

import argparse
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parent))
from sms_classifier import CONFIDENCE_THRESHOLD, HISTORY_WINDOW, classify  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default=HERE / "labeled_sms.csv")
    parser.add_argument("--threshold", type=float, default=CONFIDENCE_THRESHOLD)
    parser.add_argument("--window", type=int, default=HISTORY_WINDOW)
    parser.add_argument("--out", default=HERE / "results.json")
    args = parser.parse_args()

    rows = list(csv.DictReader(open(args.csv, newline="", encoding="utf-8")))
    per_cat = defaultdict(lambda: [0, 0])   # expected category -> [correct, total]
    per_case = defaultdict(lambda: [0, 0])  # case_type -> [correct, total]
    results, misses, missed_complaints, flagged_complaints = [], [], [], []

    for row in rows:
        history = json.loads(row["history"]) if row.get("history") else []
        expected = row["expected"].split("|")
        result = classify(row["message"], history,
                          threshold=args.threshold, history_window=args.window)
        ok = result["category"] in expected
        for bucket in (per_cat[expected[0]], per_case[row.get("case_type", "all")]):
            bucket[0] += ok
            bucket[1] += 1
        if result["category"] == "complaint" and result["flagged_for_review"]:
            flagged_complaints.append((row, result))
        if not ok:
            misses.append((row, result))
            if "complaint" in expected:
                missed_complaints.append(row["id"])
        results.append({**row, "result": result, "correct": ok})

    total = sum(r["correct"] for r in results)
    print(f"\nOverall: {total}/{len(results)} = {total / len(results):.0%}"
          f"  (threshold={args.threshold}, window={args.window})\n")
    print("By expected category:")
    for cat, (c, t) in sorted(per_cat.items()):
        print(f"  {cat:12} {c}/{t}")
    print("\nBy case type:")
    for case, (c, t) in sorted(per_case.items()):
        print(f"  {case:12} {c}/{t}")
    flagged = sum(r["result"]["flagged_for_review"] for r in results)
    errors = sum("error" in r["result"] for r in results)
    print(f"\nFlagged for review: {flagged}   API/parse errors: {errors}")
    if flagged_complaints:
        print("\nLow-confidence complaints (escalated anyway, flagged):")
        for row, res in flagged_complaints:
            print(f"  #{row['id']} @ {res['confidence']:.2f} expected {row['expected']} | {row['message']}")
    if missed_complaints:
        print(f"!! Missed complaints (worst failure): ids {', '.join(missed_complaints)}")
    if misses:
        print("\nMisses:")
        for row, res in misses:
            raw = f" (raw {res['raw_category']})" if "raw_category" in res else ""
            err = f" ERROR {res['error']}" if "error" in res else ""
            print(f"  #{row['id']} expected {row['expected']:22} got {res['category']}"
                  f" @ {res['confidence']:.2f}{raw}{err} | {row['message']}")

    Path(args.out).write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(f"\nFull results: {args.out}")


if __name__ == "__main__":
    main()
