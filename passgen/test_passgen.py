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


class TestStrength(unittest.TestCase):
    def test_long_beats_short(self):
        from passgen import strength
        short = strength("abc123")
        long_ = strength("aB3!xY9#qW2!eR5$")
        self.assertGreater(long_["bits"], short["bits"])
        self.assertIn(long_["rating"], ("strong", "excellent"))

    def test_empty_is_zero(self):
        from passgen import strength
        self.assertEqual(strength(""), {"bits": 0.0, "rating": "weak"})


if __name__ == "__main__":
    unittest.main()


class TestNoAmbiguous(unittest.TestCase):
    def test_lookalikes_removed(self):
        from passgen import AMBIGUOUS
        pwd = generate(length=48, no_ambiguous=True)[0]
        self.assertFalse(set(pwd) & AMBIGUOUS)

    def test_digits_pool_excludes_zero(self):
        for _ in range(20):
            pwd = generate(length=40, lower=False, upper=False, digits=True,
                           symbols=False, no_ambiguous=True)[0]
            self.assertNotIn("0", pwd)


class TestStrength(unittest.TestCase):
    def test_long_beats_short(self):
        from passgen import strength
        short = strength("abc123")
        long_ = strength("aB3!xY9#qW2!eR5$")
        self.assertGreater(long_["bits"], short["bits"])
        self.assertIn(long_["rating"], ("strong", "excellent"))

    def test_empty_is_zero(self):
        from passgen import strength
        self.assertEqual(strength(""), {"bits": 0.0, "rating": "weak"})


if __name__ == "__main__":
    unittest.main()


class TestPassphrase(unittest.TestCase):
    def test_shape(self):
        from passgen import passphrase
        pp = passphrase(4)
        self.assertEqual(len(pp.split("-")), 4)
        self.assertTrue(all(w.isalpha() for w in pp.split("-")))

    def test_custom_separator(self):
        from passgen import passphrase
        self.assertIn(" ", passphrase(3, separator=" "))


if __name__ == "__main__":
    unittest.main()
