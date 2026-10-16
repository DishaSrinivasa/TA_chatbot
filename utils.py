"""PDF text extraction and chunking helpers."""
import pdfplumber


def extract_text_from_pdf(file_path):
    """Return all text in a PDF. Pages with no extractable text are skipped."""
    pages = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n".join(pages)


def chunk_text(text, chunk_size=500, overlap=50):
    """Split text into chunks of `chunk_size` words that overlap by `overlap` words."""
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")
    words = text.split()
    step = chunk_size - overlap
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), step)
    ]
