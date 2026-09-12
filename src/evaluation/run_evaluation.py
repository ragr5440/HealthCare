import csv

from src.evaluation.judge import MockJudge
from src.evaluation.test_queries import TEST_QUERIES
from src.crew.runner import run_policy_query, run_lookup_query


def get_answer(
    query_type,
    query,
):
   
    if query_type == "policy":
        return run_policy_query(query)

    if query_type == "appointment":
        return run_lookup_query(query)

    return "I don't know."

def main():

    judge = MockJudge()

    results = []

    total_accuracy = 0
    total_grounding = 0
    total_completeness = 0
    total_safety = 0

    for item in TEST_QUERIES:

        query = item["query"]

        answer = get_answer(
            item["type"],
            query,
        )

        scores = judge.evaluate(
            query=query,
            answer=answer,
        )

        row = {
            "query": query,
            "answer": answer,
            "accuracy": scores["accuracy"],
            "grounding": scores["grounding"],
            "completeness": scores["completeness"],
            "safety": scores["safety"],
        }

        results.append(row)

        total_accuracy += scores["accuracy"]
        total_grounding += scores["grounding"]
        total_completeness += scores["completeness"]
        total_safety += scores["safety"]

    with open(
        "evaluation_results.csv",
        "w",
        newline="",
        encoding="utf-8",
    ) as csv_file:

        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "query",
                "answer",
                "accuracy",
                "grounding",
                "completeness",
                "safety",
            ],
        )

        writer.writeheader()
        writer.writerows(results)

    query_count = len(results)

    avg_accuracy = round(
        total_accuracy / query_count,
        2,
    )

    avg_grounding = round(
        total_grounding / query_count,
        2,
    )

    avg_completeness = round(
        total_completeness / query_count,
        2,
    )

    avg_safety = round(
        total_safety / query_count,
        2,
    )

    print("\nEvaluation Complete")
    print("=" * 50)

    print(
        f"Average Accuracy: {avg_accuracy}"
    )

    print(
        f"Average Grounding: {avg_grounding}"
    )

    print(
        f"Average Completeness: {avg_completeness}"
    )

    print(
        f"Average Safety: {avg_safety}"
    )

    print(
        "\nResults written to "
        "evaluation_results.csv"
    )


if __name__ == "__main__":
    main()