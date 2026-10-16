# AI TA Chatbot

A retrieval-augmented chatbot that answers questions about your Machine Learning course using your own lecture-slide PDFs. Built as a final project for CSCI 5930.

## How it works

1. **Extract**: text is pulled from every PDF in `data/` with `pdfplumber`.
2. **Chunk**: text is split into overlapping 500-word chunks.
3. **Embed and index**: chunks are embedded with OpenAI `text-embedding-3-small` and stored in a FAISS index (embeddings are cached in `.cache/`, so you only pay once per set of slides).
4. **Retrieve and answer**: for each question, the 3 closest chunks are sent to the chat model (`gpt-4o-mini` by default), which answers from that context. The source PDFs are shown under each answer.
5. **UI**: a Streamlit chat interface.

## Setup

Requires Python 3.10+ and an [OpenAI API key](https://platform.openai.com/api-keys).

```bash
git clone https://github.com/<your-username>/TA_chatbot.git
cd TA_chatbot
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env and paste your key
```

Put your lecture PDFs in the `data/` folder. They are not included in this repo because they are copyrighted course material.

## Run

```bash
streamlit run app.py
```

The first launch embeds your PDFs, which takes a short while; later launches reuse the cache.

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `OPENAI_API_KEY` | none (required) | Your OpenAI key |
| `CHAT_MODEL` | `gpt-4o-mini` | Chat model used for answers |
| `DATA_DIR` | `data` | Folder containing the PDFs |

## Tests

```bash
pip install pytest
pytest
```

## Project layout

- `app.py`: Streamlit chat interface
- `main.py`: indexing, retrieval and answering
- `utils.py`: PDF text extraction and chunking
- `tests/`: unit tests

## Authors

Shrujal Mogadati, Disha Srinivasa, Kavya Avula

Released under the [MIT License](LICENSE).
