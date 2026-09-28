import json
import tempfile
import unittest
from pathlib import Path

import todo


class TestTodo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Path(self.tmp.name) / "todo.json"
        self.old = todo.STORE
        todo.STORE = self.store
        self.addCleanup(self.tmp.cleanup)
        self.addCleanup(setattr, todo, "STORE", self.old)

    def test_add_and_list(self):
        todo.add("write tests")
        todo.add("ship it")
        self.assertEqual(len(todo.load()), 2)
        self.assertFalse(todo.load()[0]["done"])

    def test_done_and_undone(self):
        todo.add("a")
        todo.done(1)
        self.assertTrue(todo.load()[0]["done"])
        todo.done(1, False)
        self.assertFalse(todo.load()[0]["done"])

    def test_rm(self):
        todo.add("keep")
        todo.add("drop")
        self.assertEqual(todo.rm(2), "drop")
        self.assertEqual(len(todo.load()), 1)

    def test_persistence_format(self):
        todo.add("persist me")
        data = json.loads(self.store.read_text())
        self.assertEqual(data[0]["task"], "persist me")
        self.assertIn("created", data[0])

    def test_rm_out_of_range(self):
        with self.assertRaises(IndexError):
            todo.rm(7)


if __name__ == "__main__":
    unittest.main()
