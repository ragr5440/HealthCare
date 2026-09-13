from src.cache.query_cache import (
    get_cached_answer,
    store_cached_answer,
    increment_retrieval_count,
    get_retrieval_count,
)

from src.crew.runner import (
    run_policy_query,
)


def process_query(
    query: str,
):

    cached_answer = get_cached_answer(
        query
    )

    if cached_answer is not None:

        print("CACHE HIT")

        return cached_answer

    print("CACHE MISS")

    increment_retrieval_count()

    answer = run_policy_query(
        query
    )

    store_cached_answer(
        query,
        answer,
    )

    return answer


def main():

    query = (
        "What is the cancellation policy?"
    )

    print("\nFIRST REQUEST")
    print("=" * 50)

    answer_1 = process_query(
        query
    )

    print("\nAnswer:")
    print(answer_1)

    print(
        "\nRetrieval Calls:",
        get_retrieval_count(),
    )

    print("\nSECOND REQUEST")
    print("=" * 50)

    answer_2 = process_query(
        query
    )

    print("\nAnswer:")
    print(answer_2)

    print(
        "\nRetrieval Calls:",
        get_retrieval_count(),
    )


if __name__ == "__main__":
    main()