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


if __name__ == "__main__":
    unittest.main()
