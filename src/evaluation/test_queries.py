TEST_QUERIES = [
    {
        "id": "Q1",
        "query": "What is the appointment booking policy?",
        "type": "policy",
        "expected_keywords": [
            "appointment",
            "booking",
            "schedule",
        ],
    },
    {
        "id": "Q2",
        "query": "What is the cancellation policy?",
        "type": "policy",
        "expected_keywords": [
            "cancel",
            "24 hours",
            "appointment",
        ],
    },
    {
        "id": "Q3",
        "query": "What are the cardiology consultation fees?",
        "type": "policy",
        "expected_keywords": [
            "cardiology",
            "consultation",
            "fee",
        ],
    },
    {
        "id": "Q4",
        "query": "How does the insurance claim process work?",
        "type": "policy",
        "expected_keywords": [
            "insurance",
            "claim",
            "process",
        ],
    },
    {
        "id": "Q5",
        "query": "What is the prescription refill policy?",
        "type": "policy",
        "expected_keywords": [
            "prescription",
            "refill",
            "doctor",
        ],
    },
    {
        "id": "Q6",
        "query": "How long do lab results take?",
        "type": "policy",
        "expected_keywords": [
            "lab",
            "results",
            "days",
        ],
    },
    {
        "id": "Q7",
        "query": "Who is eligible for telemedicine?",
        "type": "policy",
        "expected_keywords": [
            "telemedicine",
            "eligible",
            "virtual",
        ],
    },
    {
        "id": "Q8",
        "query": "What is the emergency visit protocol?",
        "type": "policy",
        "expected_keywords": [
            "emergency",
            "visit",
            "immediate",
        ],
    },
    {
        "id": "Q9",
        "query": "How is patient data protected?",
        "type": "policy",
        "expected_keywords": [
            "patient",
            "data",
            "privacy",
        ],
    },
    {
        "id": "Q10",
        "query": "What follow-up discounts are available?",
        "type": "policy",
        "expected_keywords": [
            "follow-up",
            "discount",
            "consultation",
        ],
    },
    {
        "id": "Q11",
        "query": "How do I request a second opinion?",
        "type": "policy",
        "expected_keywords": [
            "second opinion",
            "request",
            "specialist",
        ],
    },
    {
        "id": "Q12",
        "query": "Who qualifies for home visits?",
        "type": "policy",
        "expected_keywords": [
            "home visit",
            "eligible",
            "patient",
        ],
    },
    {
        "id": "Q13",
        "query": "Check appointment status for APT-0015",
        "type": "appointment",
        "expected_keywords": [
            "status",
            "appointment",
            "consultation",
        ],
    },
    {
        "id": "Q14",
        "query": "Who won the FIFA World Cup 2022?",
        "type": "oos",
        "expected_keywords": [
            "I don't know",
        ],
    },
    {
        "id": "Q15",
        "query": "Explain quantum entanglement.",
        "type": "oos",
        "expected_keywords": [
            "I don't know",
        ],
    },
]