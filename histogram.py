#!/usr/bin/env python3
"""histogram - Histogram computation and equalization."""
import sys

def compute_histogram(data, bins=10, range_=None):
    if range_ is None:
        mn, mx = min(data), max(data)
    else:
        mn, mx = range_
    if mn == mx:
        return [len(data)], [(mn, mx)]
    bin_width = (mx - mn) / bins
    counts = [0] * bins
    edges = [(mn + i*bin_width, mn + (i+1)*bin_width) for i in range(bins)]
    for v in data:
        idx = int((v - mn) / bin_width)
        idx = min(idx, bins - 1)
        if idx >= 0:
            counts[idx] += 1
    return counts, edges

def cumulative_histogram(counts):
    result = []
    total = 0
    for c in counts:
        total += c
        result.append(total)
    return result

def equalize(values, levels=256):
    counts, _ = compute_histogram(values, bins=levels, range_=(0, levels-1))
    cumul = cumulative_histogram(counts)
    n = len(values)
    cdf_min = min(c for c in cumul if c > 0)
    lut = [round((c - cdf_min) / (n - cdf_min) * (levels - 1)) if n > cdf_min else 0 for c in cumul]
    return [lut[min(int(v), levels-1)] for v in values]

def percentile(data, p):
    sorted_data = sorted(data)
    k = (len(sorted_data) - 1) * p / 100
    f = int(k)
    c = f + 1 if f + 1 < len(sorted_data) else f
    d = k - f
    return sorted_data[f] + d * (sorted_data[c] - sorted_data[f])

def test():
    data = [1, 2, 2, 3, 3, 3, 4, 4, 5]
    counts, edges = compute_histogram(data, bins=5, range_=(1, 5))
    assert len(counts) == 5
    assert sum(counts) == 9
    cumul = cumulative_histogram(counts)
    assert cumul[-1] == 9
    # percentile
    assert percentile(data, 50) == 3.0
    assert percentile(data, 0) == 1.0
    assert percentile(data, 100) == 5.0
    # equalize
    dark = [10, 20, 30, 10, 20, 30, 10, 20]
    eq = equalize(dark, 256)
    assert max(eq) > max(dark)  # spread out
    print("OK: histogram")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: histogram.py test")
