import os
import tempfile
import unittest

from audit import audit


class TestAudit(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        os.makedirs(f"{self.root}/sub/deep")
        self._w(f"{self.root}/a.txt", 100)
        self._w(f"{self.root}/sub/b.bin", 200)
        self._w(f"{self.root}/sub/deep/c.bin", 400)

    def _w(self, p, n):
        with open(p, "wb") as f:
            f.write(b"x" * n)

    def test_sizes_aggregate_up(self):
        stats, total, count = audit(self.root)
        self.assertEqual(count, 3)
        self.assertEqual(total, 700)
        sizes = {s.path.split(os.sep)[-1]: s.size for s in stats}
        self.assertEqual(sizes["deep"], 400)
        self.assertEqual(sizes["sub"], 600)

    def test_min_size_filter(self):
        stats, _, _ = audit(self.root, min_size=500)
        self.assertEqual([s.path for s in stats], [f"{self.root}/sub"])

    def test_exclude(self):
        _, total, count = audit(self.root, exclude={"sub"})
        self.assertEqual((total, count), (100, 1))

    def test_symlink_skipped(self):
        try:
            os.symlink(f"{self.root}/sub", f"{self.root}/link")
        except OSError:
            self.skipTest("no symlink support")
        _, _, count = audit(self.root)
        self.assertEqual(count, 3)


if __name__ == "__main__":
    unittest.main()
