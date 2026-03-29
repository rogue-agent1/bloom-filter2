#!/usr/bin/env python3
"""bloom_filter2 - Counting Bloom filter with delete support and FPR estimation."""
import sys, math

class CountingBloom:
    def __init__(self, capacity=1000, fp_rate=0.01):
        self.size = max(1, int(-capacity * math.log(fp_rate) / (math.log(2)**2)))
        self.k = max(1, int(self.size / capacity * math.log(2)))
        self.counts = [0] * self.size
        self.n = 0
    def _hashes(self, item):
        s = str(item)
        h1 = hash(s) & 0xFFFFFFFF
        h2 = hash(s + "_salt") & 0xFFFFFFFF
        return [(h1 + i * h2) % self.size for i in range(self.k)]
    def add(self, item):
        for idx in self._hashes(item):
            self.counts[idx] += 1
        self.n += 1
    def __contains__(self, item):
        return all(self.counts[idx] > 0 for idx in self._hashes(item))
    def remove(self, item):
        if item not in self: return False
        for idx in self._hashes(item):
            self.counts[idx] = max(0, self.counts[idx] - 1)
        self.n -= 1
        return True
    def fp_rate(self):
        if self.n == 0: return 0.0
        return (1 - math.exp(-self.k * self.n / self.size)) ** self.k

def test():
    bf = CountingBloom(100, 0.01)
    for i in range(50): bf.add(f"item_{i}")
    for i in range(50): assert f"item_{i}" in bf
    fp = sum(1 for i in range(1000, 2000) if f"item_{i}" in bf)
    assert fp < 100  # <10% FP
    bf.remove("item_0")
    assert "item_0" not in bf
    assert "item_1" in bf
    assert bf.fp_rate() > 0
    print("bloom_filter2: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: bloom_filter2.py --test")
