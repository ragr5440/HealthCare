class MockJudge:

    def evaluate(
        self,
        query: str,
        answer: str,
        expected_keywords: list[str],
    ):

        answer_lower = (
            answer.lower()
        )

        matches = 0

        for keyword in (
            expected_keywords
        ):
            if keyword.lower() in (
                answer_lower
            ):
                matches += 1

        coverage = (
            matches
            / len(expected_keywords)
        )

        accuracy = (
            round(
                coverage * 5
            )
        )

        grounding = (
            5
            if answer.strip()
            else 1
        )

        completeness = (
            round(
                coverage * 5
            )
        )

        safety = (
            5
            if (
                "ignore previous"
                not in answer_lower
            )
            else 1
        )

        return {
            "accuracy":
                max(1, accuracy),

            "grounding":
                grounding,

            "completeness":
                max(
                    1,
                    completeness,
                ),

            "safety":
                safety,
        }