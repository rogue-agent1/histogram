#!/usr/bin/env python3
"""histogram - Generate text histograms from data. Zero deps."""
import sys, collections
def main():
    bins = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10
    numbers = [float(l.strip()) for l in sys.stdin if l.strip()]
    if not numbers: print("No data"); sys.exit(1)
    lo, hi = min(numbers), max(numbers)
    width = (hi - lo) / bins if hi != lo else 1
    buckets = [0] * bins
    for n in numbers:
        idx = min(int((n - lo) / width), bins - 1)
        buckets[idx] += 1
    mx = max(buckets)
    for i, count in enumerate(buckets):
        lo_b = lo + i * width
        bar = "█" * int(count / mx * 40) if mx else ""
        print(f"{lo_b:8.2f} | {bar} {count}")
    print(f"\nn={len(numbers)} min={lo:.2f} max={hi:.2f} mean={sum(numbers)/len(numbers):.2f}")
if __name__ == "__main__": main()
