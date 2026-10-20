
import unittest

from app.llm.local_model import LLMModel


class TestLLMModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.llm = LLMModel()

    def test_generate_response(self):
        response = self.llm.generate_response(
            "What is a college transcript? Answer in two sentences."
        )

        self.assertIsInstance(response, str)
        self.assertGreater(len(response.strip()), 0)

        print("\nGenerated response:", response)

    def test_empty_prompt(self):
        with self.assertRaises(ValueError):
            self.llm.generate_response("   ")


if __name__ == "__main__":
    unittest.main()
