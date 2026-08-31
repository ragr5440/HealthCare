from src.rag.chunking import (
    fixed_size_chunk,
    sentence_chunk,
)


def test_fixed_chunking():

    text = "A" * 500

    chunks = fixed_size_chunk(
        text,
        chunk_size=250,
        overlap=50,
    )

    assert len(chunks) > 1


def test_sentence_chunking():

    text = (
        "Sentence one. "
        "Sentence two. "
        "Sentence three. "
        "Sentence four."
    )

    chunks = sentence_chunk(
        text,
        sentences_per_chunk=2,
    )

    assert len(chunks) == 2