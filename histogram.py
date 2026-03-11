#!/usr/bin/env python3
"""Histogram — terminal bar chart from data."""
import sys, re
from collections import Counter
def histogram(data, width=40):
    counts = Counter(data)
    mx = max(counts.values()) if counts else 1
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        bar = "█" * (v * width // mx)
        print(f"  {str(k):>15s} |{bar} {v}")
if __name__ == "__main__":
    if not sys.stdin.isatty():
        words = re.findall(r'\w+', sys.stdin.read().lower())
    else:
        words = "the quick brown fox jumps over the lazy dog the fox the dog".split()
    histogram(words)
