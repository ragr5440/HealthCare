from src.governance.runtime_budget import (
    validate_budget,
)


def main():

    oversized_query = (
        "hello " * 1000
    )

    result = validate_budget(
        oversized_query
    )

    print("\nTOKEN BUDGET TEST")
    print("=" * 50)

    print(result)


if __name__ == "__main__":
    main()