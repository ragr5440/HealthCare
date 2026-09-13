from src.crew.full_crew_runner import (
    run_full_crew,
)


def main():

    print("\nPOLICY QUERY")
    print("=" * 50)

    result = run_full_crew(
        "What is the cancellation policy?"
    )

    print(result)

    print("\nAPPOINTMENT QUERY")
    print("=" * 50)

    result = run_full_crew(
        "Check appointment status for APT-0015"
    )

    print(result)


if __name__ == "__main__":
    main()