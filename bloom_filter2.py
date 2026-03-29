#!/usr/bin/env python3
"""bloom_filter2 - Bloom filter with optimal sizing and false positive estimation."""
import sys, math, hashlib

class BloomFilter:
    def __init__(self, capacity, fp_rate=0.01):
        self.capacity = capacity
        self.fp_rate = fp_rate
        self.size = self._optimal_size(capacity, fp_rate)
        self.num_hashes = self._optimal_hashes(self.size, capacity)
        self.bits = [False] * self.size
        self.count = 0
    @staticmethod
    def _optimal_size(n, p):
        return max(1, int(-n * math.log(p) / (math.log(2) ** 2)))
    @staticmethod
    def _optimal_hashes(m, n):
        return max(1, int(m / n * math.log(2)))
    def _hashes(self, item):
        s = str(item).encode()
        h1 = int(hashlib.md5(s).hexdigest(), 16)
        h2 = int(hashlib.sha1(s).hexdigest(), 16)
        return [(h1 + i * h2) % self.size for i in range(self.num_hashes)]
    def add(self, item):
        for idx in self._hashes(item):
            self.bits[idx] = True
        self.count += 1
    def __contains__(self, item):
        return all(self.bits[idx] for idx in self._hashes(item))
    def estimated_fp_rate(self):
        ones = sum(self.bits)
        if ones == 0:
            return 0.0
        return (ones / self.size) ** self.num_hashes

def test():
    bf = BloomFilter(1000, 0.01)
    for i in range(500):
        bf.add(f"item_{i}")
    for i in range(500):
        assert f"item_{i}" in bf
    fp = sum(1 for i in range(10000, 11000) if f"item_{i}" in bf)
    assert fp < 50  # should be ~1% = ~10, allow some margin
    assert bf.count == 500
    assert bf.size > 0 and bf.num_hashes > 0
    print("OK: bloom_filter2")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: bloom_filter2.py test")
