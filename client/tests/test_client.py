import unittest
from client.cli import parse_arguments

class TestClient(unittest.TestCase):
    def test_parse_arguments(self):
        args = parse_arguments(["--query", "test query", "--library", "docker"])
        self.assertEqual(args.query, "test query")
        self.assertEqual(args.library, "docker")