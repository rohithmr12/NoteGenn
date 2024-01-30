# main_app.py
import streamlit as st
from speech_rec import recognize_speech
from chunk_manager import chunk_text
from llama import get_llama_response
from pdf_manager import generate_pdf

# Streamlit app
st.set_page_config(page_title="Generate Notes",
                   page_icon='📝',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Notes 📝")

# User input
audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
topic = st.text_input("Enter the Topic")
chunk_size = st.slider("Select Chunk Size", min_value=1, max_value=100, value=10)

# Result queue for communication between threads
result_queue = st.empty()

# Final response
if st.button("Generate Notes"):
    if audio_file is not None and topic:
        transcribed_text = recognize_speech(audio_file)
        text_chunks = chunk_text(transcribed_text, chunk_size)
        llama_response = get_llama_response(topic, len(text_chunks))
        updated_text_chunks = [chunk + llama_response for chunk in text_chunks]

        pdf_path = generate_pdf(updated_text_chunks)
        st.success(f"Notes generated successfully! [Download PDF]({pdf_path})")
    else:
        st.warning("Please upload an audio file and enter a topic.")
