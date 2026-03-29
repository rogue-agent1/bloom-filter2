#!/usr/bin/env python3
"""Bloom filter with configurable false positive rate."""
import sys, math, hashlib

class BloomFilter:
    def __init__(self, capacity=1000, fp_rate=0.01):
        self.size = max(1, int(-capacity * math.log(fp_rate) / (math.log(2)**2)))
        self.k = max(1, int(self.size / capacity * math.log(2)))
        self.bits = bytearray(self.size // 8 + 1)
        self.count = 0
    def _hashes(self, item):
        s = str(item).encode()
        h1 = int(hashlib.md5(s).hexdigest(), 16)
        h2 = int(hashlib.sha1(s).hexdigest(), 16)
        return [(h1 + i * h2) % self.size for i in range(self.k)]
    def add(self, item):
        for h in self._hashes(item):
            self.bits[h // 8] |= (1 << (h % 8))
        self.count += 1
    def __contains__(self, item):
        return all(self.bits[h // 8] & (1 << (h % 8)) for h in self._hashes(item))
    def __len__(self):
        return self.count

def test():
    bf = BloomFilter(100, 0.01)
    for i in range(50):
        bf.add(f"item{i}")
    for i in range(50):
        assert f"item{i}" in bf
    assert len(bf) == 50
    fp = sum(1 for i in range(1000, 2000) if f"item{i}" in bf)
    assert fp < 50  # less than 5% false positives
    print("  bloom_filter2: ALL TESTS PASSED")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Bloom filter — use add() and 'in' operator")
