# app.py

import streamlit as st
from langchain.llms import CTransformers
from langchain.prompts import PromptTemplate
from io import BytesIO
from fpdf import FPDF
import threading
import queue
import time
import os
from llama import generate_llama_response
from speech_rec import recognize_speech

# Function to get response from LLAma 2 model
def getLLamaresponse(input_text, no_words, result_queue):
    response = generate_llama_response(input_text, no_words)

    # Put the response in the result queue
    result_queue.put(response)

# Function to update notes
def update_notes(result_queue, pdf):
    while True:
        if not result_queue.empty():
            response = result_queue.get()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, response)
            time.sleep(1)  # Simulate some processing time
        else:
            time.sleep(0.5)

# Streamlit app
st.set_page_config(
    page_title="Generate Notes",
    page_icon='📝',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Generate Notes 📝")

# File upload
uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav"])

# Option to test with a local audio file directly
audio_file_path = st.text_input("Enter the path of a local audio file (if testing directly)")

if audio_file_path:
    uploaded_file = None  # Ignore the uploaded file if a local path is provided

if uploaded_file or audio_file_path:
    # Save the uploaded file in the working directory or use the provided local path
    if uploaded_file:
        audio_file_path = "output_file.wav"  # Adjust the file name as needed
        with open(audio_file_path, "wb") as audio_file:
            audio_file.write(uploaded_file.read())

    # Display the audio file
    st.audio(audio_file_path, format='audio/mp3', start_time=0)

    input_text = st.text_input("Enter the Topic")
    submit = st.button("Generate")

    # Result queue for communication between threads
    result_queue = queue.Queue()

    # Thread for updating notes
    pdf = FPDF()
    notes_thread = threading.Thread(target=update_notes, args=(result_queue, pdf))
    notes_thread.start()

    # Final response
    if submit:
        # Perform speech recognition on the audio file
        transcribed_text = recognize_speech(audio_file_path)

        # Generate LLama 2 model response
        getLLamaresponse(transcribed_text,70, result_queue)

    # Stop the notes thread when the app is closed
    st.rerun()


