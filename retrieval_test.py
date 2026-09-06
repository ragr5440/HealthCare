from src.rag.retrieval import retrieve

TEST_QUERIES = [
    {
        "query": "How do I cancel my appointment?",
        "expected_doc": "appointment_cancellation"
    },
    {
        "query": "Can I change my appointment time?",
        "expected_doc": "appointment_rescheduling"
    },
    {
        "query": "How do insurance claims work?",
        "expected_doc": "insurance_claims"
    },
    {
        "query": "Can I consult a doctor online?",
        "expected_doc": "telemedicine_policy"
    },
    {
        "query": "When will lab results be available?",
        "expected_doc": "lab_turnaround"
    }, 
    {
        "query": "Will I get my money back after cancelling?",
        "expected_doc": "payment_refunds",
    },

    {
        "query": "Is there a lower fee for a return visit?",
        "expected_doc": "follow_up_discounts",
    },
    {

        "query": "Who can see my medical information?",
        "expected_doc": "data_privacy",
    } 
]

def evaluate_collection(collection_name):

    total_true_positives = 0
    total_retrieved_documents = 0
    total_relevant_documents = len(TEST_QUERIES)

    print(f"\nEvaluating: {collection_name}")
    print("-" * 50)

    for item in TEST_QUERIES:

        response = retrieve(
            query=item["query"],
            collection_name=collection_name,
            top_k=3,
        )

        expected_doc = item["expected_doc"]

        if response["in_scope"]:
            retrieved_documents = {
                result["document_id"]
                for result in response["results"]
            }
        else:
            retrieved_documents = set()

        true_positives = int(
            expected_doc in retrieved_documents
        )

        total_true_positives += true_positives
        total_retrieved_documents += len(
            retrieved_documents
        )

        print(f"\nQuery: {item['query']}")
        print(f"Expected: {expected_doc}")
        print(
            f"Retrieved documents: "
            f"{sorted(retrieved_documents)}"
        )
        print(
            f"Relevant document retrieved: "
            f"{bool(true_positives)}"
        )

    precision = (
        total_true_positives
        / total_retrieved_documents
        if total_retrieved_documents
        else 0.0
    )

    recall = (
        total_true_positives
        / total_relevant_documents
        if total_relevant_documents
        else 0.0
    )

    print(f"\nPrecision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")

    return {
        "precision": precision,
        "recall": recall,
    }

def main():

    fixed_metrics = evaluate_collection(
        "clinic_fixed_chunks"
    )

    sentence_metrics = evaluate_collection(
        "clinic_sentence_chunks"
    )

    print("\nSUMMARY")
    print("=" * 50)

    print(
        "Fixed Chunking\n"
        f"Precision: {fixed_metrics['precision']:.2%}\n"
        f"Recall: {fixed_metrics['recall']:.2%}"
    )

    print(
        "\nSentence Chunking\n"
        f"Precision: {sentence_metrics['precision']:.2%}\n"
        f"Recall: {sentence_metrics['recall']:.2%}"
    )

if __name__ == "__main__":
    main()