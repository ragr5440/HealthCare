from src.rag.retrieval import retrieve


def search_policy(query: str):
    """
    Wrapper around the retrieval system.
    This will later be exposed as a CrewAI tool.
    """

    response = retrieve(
        query=query,
        collection_name="clinic_sentence_chunks",
        top_k=3,
    )

    if not response["in_scope"]:
        return {
            "found": False,
            "message": (
                "No relevant clinic policy "
                "information found."
            )
        }

    return {
        "found": True,
        "results": response["results"]
    }


def main():

    query = (
        "How do I cancel my appointment?"
    )

    result = search_policy(
        query
    )

    print(result)


if __name__ == "__main__":
    main()