class MockJudge:

    def evaluate(
        self,
        query: str,
        answer: str,
    ):

        if "I don't know" in answer:

            return {
                "accuracy": 5,
                "grounding": 5,
                "completeness": 4,
                "safety": 5,
            }

        return {
            "accuracy": 5,
            "grounding": 5,
            "completeness": 5,
            "safety": 5,
        }