from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_NAME = "all-MiniLM-L6-v2"

MODEL = SentenceTransformer(MODEL_NAME)

CHROMA_PATH = PROJECT_ROOT / "chroma_db"

SIMILARITY_THRESHOLD = 1.4

def get_collection(collection_name):
    """
    Connect to existing collection.
    """

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    return client.get_collection(
        name=collection_name
    )

def retrieve(
    query: str,
    collection_name: str,
    top_k: int = 3,
):
    """
    Retrieve top matching chunks.
    """
    query_embedding = MODEL.encode(
        query
    ).tolist()

    collection = get_collection(
        collection_name
    )

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k,
    )

    formatted_results = []

    for i in range(
        len(results["ids"][0])
    ):
        formatted_results.append(
            {
                "chunk_id":
                    results["ids"][0][i],

                "document_id":
                    results["metadatas"][0][i]["document_id"],

                "distance":
                    results["distances"][0][i],

                "text":
                    results["documents"][0][i],
            }
        )

    if not formatted_results:
        return []

    best_result = formatted_results[0]

    if best_result["distance"] > SIMILARITY_THRESHOLD:
        return {
        "in_scope": False,
        "results": []
        }

    print("Threshold:", SIMILARITY_THRESHOLD)
    print("best result:", best_result)

    return {
        "in_scope": True,
        "results": formatted_results
    }

def print_results(results):

    for idx, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\nResult #{idx}"
        )

        print(
            f"Document: "
            f"{result['document_id']}"
        )

        print(
            f"Distance: "
            f"{result['distance']:.4f}"
        )

        print(
            "\nChunk:"
        )

        print(
            result["text"]
        )

        print(
            "\n" + "=" * 60
        )

def main():

    query = (
        "How do I cancel my appointment?"
    )

    print(
        f"\nQuery: {query}"
    )

    results = retrieve(
        query=query,
        collection_name=
        "clinic_sentence_chunks",
        top_k=3,
    )

    if not results["in_scope"]:
        print(
            "\nNo relevant clinic policy found."
        )
        return

    print_results(results["results"])

if __name__ == "__main__":
    main()