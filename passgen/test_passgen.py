import string
import unittest

from passgen import SETS, generate


class TestGenerate(unittest.TestCase):
    def test_length_and_count(self):
        pwds = generate(length=24, count=5)
        self.assertEqual(len(pwds), 5)
        self.assertTrue(all(len(p) == 24 for p in pwds))

    def test_guarantees_each_set(self):
        for _ in range(50):  # shuffle is random — sample generously
            pwd = generate(length=8)[0]
            for pool in SETS.values():
                self.assertTrue(set(pwd) & set(pool), f"missing {pool!r} in {pwd}")

    def test_subset_selection(self):
        pwd = generate(length=32, lower=True, upper=True, digits=False, symbols=False)[0]
        self.assertTrue(set(pwd) <= set(string.ascii_letters))

    def test_empty_pools_rejected(self):
        with self.assertRaises(ValueError):
            generate(lower=False, upper=False, digits=False, symbols=False)

    def test_short_length_rejected(self):
        with self.assertRaises(ValueError):
            generate(length=2)


if __name__ == "__main__":
    unittest.main()
