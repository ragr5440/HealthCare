from pathlib import Path
import re

KNOWLEDGE_BASE_PATH = "knowledgebase"

def load_documents():
    """
    Load all markdown documents from the knowledgebase folder.
    """

    documents = {}

    for file_path in Path(KNOWLEDGE_BASE_PATH).glob("*.md"):
        document_id = file_path.stem

        with open(file_path, "r", encoding="utf-8") as file:
            documents[document_id] = file.read()

    return documents


def fixed_size_chunk(
    text: str,
    chunk_size: int = 250,
    overlap: int = 50,
):
    """
    Character-based chunking.
    """

    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


def sentence_chunk(
    text: str,
    sentences_per_chunk: int = 2,
):
    """
    Group sentences together.
    """

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    chunks = []

    for i in range(
        0,
        len(sentences),
        sentences_per_chunk,
    ):
        chunk = " ".join(
            sentences[i : i + sentences_per_chunk]
        )

        if chunk.strip():
            chunks.append(chunk)

    return chunks


def build_fixed_chunks(documents):
    """
    Build metadata-rich chunks using
    fixed-size chunking.
    """

    all_chunks = []

    for document_id, text in documents.items():

        chunks = fixed_size_chunk(text)

        for idx, chunk in enumerate(chunks, start=1):
            all_chunks.append(
                {
                    "chunk_id": (
                        f"{document_id}_chunk_{idx}"
                    ),
                    "document_id": document_id,
                    "strategy": "fixed",
                    "text": chunk,
                }
            )

    return all_chunks


def build_sentence_chunks(documents):
    """
    Build metadata-rich chunks using
    sentence-based chunking.
    """

    all_chunks = []

    for document_id, text in documents.items():

        chunks = sentence_chunk(text)

        for idx, chunk in enumerate(chunks, start=1):
            all_chunks.append(
                {
                    "chunk_id": (
                        f"{document_id}_chunk_{idx}"
                    ),
                    "document_id": document_id,
                    "strategy": "sentence",
                    "text": chunk,
                }
            )

    return all_chunks


def main():

    documents = load_documents()

    fixed_chunks = build_fixed_chunks(
        documents
    )

    sentence_chunks = build_sentence_chunks(
        documents
    )

    print(
        f"\nLoaded Documents: "
        f"{len(documents)}"
    )

    print(
        f"Fixed Chunks: "
        f"{len(fixed_chunks)}"
    )

    print(
        f"Sentence Chunks: "
        f"{len(sentence_chunks)}"
    )

    print("\nSample Fixed Chunk:")
    print(fixed_chunks[0])

    print("\nSample Sentence Chunk:")
    print(sentence_chunks[0])


if __name__ == "__main__":
    main()