import pytest

from utils import chunk_text


def test_chunk_text_overlaps():
    words = " ".join(str(i) for i in range(10))
    chunks = chunk_text(words, chunk_size=4, overlap=1)
    assert chunks[0] == "0 1 2 3"
    assert chunks[1].startswith("3 ")


def test_chunk_text_empty():
    assert chunk_text("") == []


def test_overlap_must_be_smaller():
    with pytest.raises(ValueError):
        chunk_text("a b c", chunk_size=2, overlap=2)
