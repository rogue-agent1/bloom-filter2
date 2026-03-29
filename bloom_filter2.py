#!/usr/bin/env python3
"""Bloom filter with configurable false positive rate."""
import math, hashlib

class BloomFilter:
    def __init__(self, expected_items: int = 1000, fp_rate: float = 0.01):
        self.size = self._optimal_size(expected_items, fp_rate)
        self.num_hashes = self._optimal_hashes(self.size, expected_items)
        self.bits = bytearray(math.ceil(self.size / 8))
        self._count = 0

    @staticmethod
    def _optimal_size(n, p):
        return int(-n * math.log(p) / (math.log(2) ** 2))

    @staticmethod
    def _optimal_hashes(m, n):
        return max(1, int(m / n * math.log(2)))

    def _hashes(self, item: str):
        h1 = int(hashlib.md5(item.encode()).hexdigest(), 16)
        h2 = int(hashlib.sha1(item.encode()).hexdigest(), 16)
        for i in range(self.num_hashes):
            yield (h1 + i * h2) % self.size

    def add(self, item: str):
        for pos in self._hashes(item):
            self.bits[pos // 8] |= (1 << (pos % 8))
        self._count += 1

    def __contains__(self, item: str) -> bool:
        return all(self.bits[pos // 8] & (1 << (pos % 8)) for pos in self._hashes(item))

    @property
    def count(self):
        return self._count

    def estimated_fp_rate(self) -> float:
        set_bits = sum(bin(b).count("1") for b in self.bits)
        if set_bits == 0:
            return 0.0
        return (set_bits / self.size) ** self.num_hashes

def test():
    bf = BloomFilter(1000, 0.01)
    for i in range(500):
        bf.add(f"item{i}")
    for i in range(500):
        assert f"item{i}" in bf
    fps = sum(1 for i in range(10000) if f"notitem{i}" in bf)
    fp_rate = fps / 10000
    assert fp_rate < 0.05, f"FP rate too high: {fp_rate}"
    assert bf.count == 500
    # Empty filter
    bf2 = BloomFilter(100, 0.1)
    assert "anything" not in bf2
    print("  bloom_filter2: ALL TESTS PASSED")

if __name__ == "__main__":
    test()
