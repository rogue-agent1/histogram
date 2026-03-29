#!/usr/bin/env python3
"""histogram - Terminal histogram and distribution analysis."""
import sys, math

def histogram(data, bins=10, width=50):
    if not data:
        return []
    mn, mx = min(data), max(data)
    if mn == mx:
        return [{"lo": mn, "hi": mx, "count": len(data), "bar": "#" * width}]
    
    bin_width = (mx - mn) / bins
    counts = [0] * bins
    for v in data:
        idx = min(int((v - mn) / bin_width), bins - 1)
        counts[idx] += 1
    
    max_count = max(counts) or 1
    result = []
    for i in range(bins):
        lo = mn + i * bin_width
        hi = lo + bin_width
        bar_len = int(counts[i] / max_count * width)
        result.append({"lo": round(lo, 2), "hi": round(hi, 2),
                       "count": counts[i], "bar": "█" * bar_len})
    return result

def stats(data):
    if not data:
        return {}
    n = len(data)
    mean = sum(data) / n
    var = sum((x - mean)**2 for x in data) / n
    std = math.sqrt(var)
    sorted_d = sorted(data)
    
    def percentile(p):
        k = (n-1) * p / 100
        f = math.floor(k)
        c = math.ceil(k)
        if f == c:
            return sorted_d[int(k)]
        return sorted_d[f] * (c-k) + sorted_d[c] * (k-f)
    
    return {
        "count": n, "min": min(data), "max": max(data),
        "mean": round(mean, 4), "std": round(std, 4),
        "median": percentile(50),
        "p25": percentile(25), "p75": percentile(75),
        "p95": percentile(95), "p99": percentile(99),
    }

def ascii_sparkline(data, width=40):
    if not data:
        return ""
    mn, mx = min(data), max(data)
    chars = " ▁▂▃▄▅▆▇█"
    if mn == mx:
        return chars[4] * min(len(data), width)
    
    # Bucket if too many points
    if len(data) > width:
        bucket_size = len(data) / width
        buckets = []
        for i in range(width):
            start = int(i * bucket_size)
            end = int((i+1) * bucket_size)
            buckets.append(sum(data[start:end]) / max(1, end-start))
        data = buckets
    
    return "".join(chars[min(8, int((v-mn)/(mx-mn)*8))] for v in data)

def frequency(data):
    freq = {}
    for v in data:
        freq[v] = freq.get(v, 0) + 1
    return sorted(freq.items(), key=lambda x: -x[1])

def test():
    data = [1, 2, 2, 3, 3, 3, 4, 4, 5, 10]
    
    h = histogram(data, bins=5)
    assert len(h) == 5
    assert sum(b["count"] for b in h) == len(data)
    
    s = stats(data)
    assert s["count"] == 10
    assert s["min"] == 1
    assert s["max"] == 10
    assert 3 < s["mean"] < 4
    
    spark = ascii_sparkline([1,2,3,4,5,4,3,2,1])
    assert len(spark) == 9
    
    freq = frequency([1,1,2,2,2,3])
    assert freq[0] == (2, 3)
    
    # Edge cases
    assert stats([]) == {}
    assert histogram([]) == []
    assert ascii_sparkline([]) == ""
    
    print(f"Stats: {s}")
    print(f"Sparkline: {spark}")
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    elif len(sys.argv) > 1:
        data = [float(x) for x in sys.argv[1:]]
        s = stats(data)
        for k, v in s.items():
            print(f"  {k}: {v}")
        print()
        for b in histogram(data):
            print(f"  [{b['lo']:8.2f}-{b['hi']:8.2f}] {b['count']:4d} {b['bar']}")
    else:
        print("Usage: histogram.py <numbers...>")
