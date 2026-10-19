import unittest
from utils.llm_helpers import generate_llm_response

class TestLLMHelpers(unittest.TestCase):
    def test_generate_llm_response(self):
        query = "How to start a Docker container?"
        context = "Docker allows you to start containers using the `docker run` command."
        response = generate_llm_response(query, context)
        self.assertIn("docker run", response)