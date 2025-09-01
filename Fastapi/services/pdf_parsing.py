from PyPDF2 import PdfReader

# Read text from PDF
def read_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Split into word chunks
def split_text(text: str, max_length=500):
    words = text.split()
    chunks, current_chunk = [], []
    
    for word in words:
        if len(current_chunk) + len(word.split()) <= max_length:
            current_chunk.append(word)
        else:
            chunks.append(" ".join(current_chunk))
            current_chunk = [word]
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks