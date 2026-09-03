from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from chunking import (
    load_documents,
    build_fixed_chunks,
    build_sentence_chunks,
)


MODEL_NAME = "all-MiniLM-L6-v2"


def create_collection(client, name):
    """
    Delete existing collection if present
    and recreate cleanly.
    """

    try:
        client.delete_collection(name)
    except Exception:
        pass

    return client.create_collection(name=name)


def add_chunks_to_collection(
    collection,
    chunks,
    model,
):
    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts
    ).tolist()

    ids = [
        chunk["chunk_id"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "document_id": chunk["document_id"],
            "strategy": chunk["strategy"],
        }
        for chunk in chunks
    ]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas,
    )


def main():

    print("Loading documents...")
    documents = load_documents()

    fixed_chunks = build_fixed_chunks(
        documents
    )

    sentence_chunks = (
        build_sentence_chunks(
            documents
        )
    )

    print(
        f"Documents Loaded: {len(documents)}"
    )

    print(
        f"Fixed Chunks: {len(fixed_chunks)}"
    )

    print(
        f"Sentence Chunks: "
        f"{len(sentence_chunks)}"
    )

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    client = chromadb.PersistentClient(
        path="chroma_db"
    )

    fixed_collection = (
        create_collection(
            client,
            "clinic_fixed_chunks",
        )
    )

    sentence_collection = (
        create_collection(
            client,
            "clinic_sentence_chunks",
        )
    )

    print(
        "Indexing fixed chunks..."
    )

    add_chunks_to_collection(
        fixed_collection,
        fixed_chunks,
        model,
    )

    print(
        "Indexing sentence chunks..."
    )

    add_chunks_to_collection(
        sentence_collection,
        sentence_chunks,
        model,
    )

    print(
        "\nIndexing completed."
    )

    print(
        "Collections created:"
    )

    print(
        "- clinic_fixed_chunks"
    )

    print(
        "- clinic_sentence_chunks"
    )


if __name__ == "__main__":
    main()