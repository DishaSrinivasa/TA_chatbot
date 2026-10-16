"""Retrieval-augmented answering over lecture PDFs (OpenAI embeddings + FAISS)."""
import os
import hashlib

import faiss
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

from utils import extract_text_from_pdf, chunk_text

load_dotenv()

DATA_DIR = os.environ.get("DATA_DIR", "data")
CACHE_DIR = ".cache"
EMBEDDING_MODEL = "text-embedding-3-small"
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gpt-4o-mini")
EMBED_BATCH = 64

SYSTEM_PROMPT = (
    "You are a helpful teaching assistant for a Machine Learning course. "
    "Answer using the provided lecture context. If the context does not "
    "contain the answer, say so instead of guessing."
)

_client = None


def get_client():
    """Create the OpenAI client lazily so importing this module needs no key."""
    global _client
    if _client is None:
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy .env.example to .env and add your key."
            )
        _client = OpenAI()
    return _client


def load_chunks(data_dir=DATA_DIR):
    """Read every PDF in `data_dir` and return (chunks, sources)."""
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Data folder '{data_dir}' not found. Put your lecture PDFs there.")
    chunks, sources = [], []
    for filename in sorted(os.listdir(data_dir)):
        if filename.lower().endswith(".pdf"):
            text = extract_text_from_pdf(os.path.join(data_dir, filename))
            for chunk in chunk_text(text):
                chunks.append(chunk)
                sources.append(filename)
    if not chunks:
        raise FileNotFoundError(f"No PDFs with extractable text found in '{data_dir}'.")
    return chunks, sources


def embed_texts(texts):
    """Embed a list of strings in batches; returns a float32 array."""
    vectors = []
    for i in range(0, len(texts), EMBED_BATCH):
        resp = get_client().embeddings.create(input=texts[i:i + EMBED_BATCH], model=EMBEDDING_MODEL)
        vectors.extend(item.embedding for item in resp.data)
    return np.array(vectors, dtype="float32")


def build_index(data_dir=DATA_DIR):
    """Build (or load from disk cache) the FAISS index. Returns (index, chunks, sources)."""
    chunks, sources = load_chunks(data_dir)
    key = hashlib.sha256((EMBEDDING_MODEL + "\x00".join(chunks)).encode()).hexdigest()[:16]
    cache_file = os.path.join(CACHE_DIR, f"embeddings-{key}.npy")

    if os.path.exists(cache_file):
        embeddings = np.load(cache_file)
    else:
        embeddings = embed_texts(chunks)
        os.makedirs(CACHE_DIR, exist_ok=True)
        np.save(cache_file, embeddings)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, chunks, sources


def retrieve_and_answer(query, index, chunks, sources, k=3):
    """Return (answer, list of source filenames) for `query`."""
    query_vec = embed_texts([query])
    _, ids = index.search(query_vec, k)
    ids = [i for i in ids[0] if i != -1]
    context = "\n\n".join(chunks[i] for i in ids)

    response = get_client().chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
        ],
    )
    used = list(dict.fromkeys(sources[i] for i in ids))
    return response.choices[0].message.content, used
