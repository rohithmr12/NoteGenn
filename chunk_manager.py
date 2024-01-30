# text_chunking.py
def chunk_text(transcribed_text, chunk_size):
    chunks = [transcribed_text[i:i + chunk_size] for i in range(0, len(transcribed_text), chunk_size)]
    return chunks
