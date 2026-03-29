#!/usr/bin/env python3
"""histogram - Image histogram analysis and equalization."""
import sys, json, math

def compute_histogram(pixels, channel=0):
    hist = [0]*256
    for row in pixels:
        for p in row:
            hist[p[channel] if isinstance(p, tuple) else p] += 1
    return hist

def cumulative_histogram(hist):
    cum = [0]*256; cum[0] = hist[0]
    for i in range(1, 256): cum[i] = cum[i-1] + hist[i]
    return cum

def equalize(pixels, width, height):
    result = [[None]*width for _ in range(height)]
    for ch in range(3):
        hist = compute_histogram(pixels, ch)
        cum = cumulative_histogram(hist)
        total = width * height
        lut = [round(cum[i]/total*255) for i in range(256)]
        for y in range(height):
            for x in range(width):
                if result[y][x] is None: result[y][x] = [0,0,0]
                result[y][x][ch] = lut[pixels[y][x][ch]]
    return [[tuple(p) for p in row] for row in result]

def histogram_stats(hist):
    total = sum(hist)
    if total == 0: return {}
    mean = sum(i*h for i,h in enumerate(hist)) / total
    var = sum(h*(i-mean)**2 for i,h in enumerate(hist)) / total
    mode = max(range(256), key=lambda i: hist[i])
    median_target = total // 2; cum = 0; median = 0
    for i in range(256):
        cum += hist[i]
        if cum >= median_target: median = i; break
    return {"mean": round(mean,1), "std": round(math.sqrt(var),1), "mode": mode, "median": median}

def main():
    import random; random.seed(42)
    w, h = 32, 32
    # Low contrast image
    pixels = [[(random.randint(100,155), random.randint(100,155), random.randint(100,155)) for _ in range(w)] for _ in range(h)]
    print("Histogram analysis demo\n")
    hist_r = compute_histogram(pixels, 0)
    stats = histogram_stats(hist_r)
    print(f"  Original R channel: {stats}")
    eq = equalize(pixels, w, h)
    hist_eq = compute_histogram(eq, 0)
    stats_eq = histogram_stats(hist_eq)
    print(f"  Equalized R channel: {stats_eq}")
    print(f"  Contrast improved: std {stats['std']:.1f} -> {stats_eq['std']:.1f}")
    # Full range test
    full = [[(x*8,y*8,128) for x in range(w)] for y in range(h)]
    full_stats = histogram_stats(compute_histogram(full, 0))
    print(f"  Full range R: {full_stats}")

if __name__ == "__main__":
    main()
