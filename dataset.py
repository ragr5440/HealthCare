import json
import random
from collections import Counter
from pathlib import Path

SEED = 42
TOTAL_RECORDS = 50

CATEGORIES = [
    "General Medicine",
    "Cardiology",
    "Dermatology",
    "Pediatrics",
    "Orthopedics"
]

CATEGORY_WEIGHTS = [
    0.30,
    0.20,
    0.15,
    0.15,
    0.20,
]

STATUSES = [
    "Scheduled",
    "Completed",
    "Cancelled",
    "No-Show",
    "Rescheduled"
]

STATUS_WEIGHTS = [
    0.25,
    0.40,
    0.10,
    0.05,
    0.20,
]

MIN_FEE = 300
MAX_FEE = 2500

FOLLOW_UP_PROBABILITY = 0.20


def create_record(
    record_id,
    category,
    status,
    fee,
    days_since_created,
    follow_up_required,
):
    return {
        "record_id": record_id,
        "category": category,
        "status": status,
        "consultation_fee_inr": fee,
        "days_since_created": days_since_created,
        "follow_up_required": follow_up_required,
    }


def generate_dataset():
    random.seed(SEED)

    records = []
    record_number = 1

    # --------------------------------------------------
    # Guaranteed coverage records
    # Ensures every category and status appears
    # --------------------------------------------------

    for category, status in zip(CATEGORIES, STATUSES):
        records.append(
            create_record(
                record_id=f"APT-{record_number:04d}",
                category=category,
                status=status,
                fee=random.randint(MIN_FEE, MAX_FEE),
                days_since_created=random.randint(0, 30),
                follow_up_required=random.random()
                < FOLLOW_UP_PROBABILITY,
            )
        )

        record_number += 1

    # --------------------------------------------------
    # Remaining records
    # --------------------------------------------------

    while len(records) < TOTAL_RECORDS:
        records.append(
            create_record(
                record_id=f"APT-{record_number:04d}",
                category=random.choices(
                    CATEGORIES,
                    weights=CATEGORY_WEIGHTS,
                    k=1,
                )[0],
                status=random.choices(
                    STATUSES,
                    weights=STATUS_WEIGHTS,
                    k=1,
                )[0],
                fee=random.randint(MIN_FEE, MAX_FEE),
                days_since_created=random.randint(0, 30),
                follow_up_required=random.random()
                < FOLLOW_UP_PROBABILITY,
            )
        )

        record_number += 1

    return records


def validate_dataset(records):
    assert len(records) >= 40

    category_counts = Counter(
        r["category"] for r in records
    )

    status_counts = Counter(
        r["status"] for r in records
    )

    for category in CATEGORIES:
        assert category_counts[category] >= 3

    for status in STATUSES:
        assert status_counts[status] >= 1

    follow_up_percentage = (
        sum(
            r["follow_up_required"]
            for r in records
        )
        / len(records)
    ) * 100

    assert 10 <= follow_up_percentage <= 30

    return {
        "category_counts": category_counts,
        "status_counts": status_counts,
        "follow_up_percentage": follow_up_percentage,
    }


def save_dataset(records):
    Path("data").mkdir(exist_ok=True)

    with open(
        "data/appointments.json",
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(records, f, indent=2)


def print_report(validation):
    print("\nCategory Counts")
    print("-" * 30)

    for key, value in validation[
        "category_counts"
    ].items():
        print(f"{key}: {value}")

    print("\nStatus Counts")
    print("-" * 30)

    for key, value in validation[
        "status_counts"
    ].items():
        print(f"{key}: {value}")

    print(
        f"\nFollow-up Percentage: "
        f"{validation['follow_up_percentage']:.2f}%"
    )


if __name__ == "__main__":
    records = generate_dataset()

    validation = validate_dataset(records)

    save_dataset(records)

    print_report(validation)

    print(
        "\nDataset successfully generated."
    )