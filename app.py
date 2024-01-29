import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.llms import CTransformers
import threading
import queue
import time
from fpdf import FPDF

# Function to get response from LLAma 2 model
def getLLamaresponse(input_text, no_words, result_queue):
    llm = CTransformers(model='models/llama-2-7b-chat.ggmlv3.q8_0.bin',
                        model_type='llama',
                        config={'max_new_tokens': 256,
                                'temperature': 0.01})

    # Prompt Template
    template = """
        Generate notes for the topic {input_text}
        within {no_words} words.
    """

    prompt = PromptTemplate(input_variables=["input_text", 'no_words'],
                            template=template)

    # Generate the response from the LLama 2 model
    response = llm(prompt.format(input_text=input_text, no_words=no_words))

    # Put the response in the result queue
    result_queue.put(response)

# Function to continuously update notes and save to PDF
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
st.set_page_config(page_title="Generate Notes",
                   page_icon='📝',
                   layout='centered',
                   initial_sidebar_state='collapsed')

st.header("Generate Notes 📝")

input_text = st.text_input("Enter the Topic")

# Creating a column for additional field
col1, _ = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')

submit = st.button("Generate")

# Result queue for communication between threads
result_queue = queue.Queue()

# Thread for updating notes
pdf = FPDF()
notes_thread = threading.Thread(target=update_notes, args=(result_queue, pdf))
notes_thread.start()

# Final response
if submit:
    getLLamaresponse(input_text, no_words, result_queue)

# Stop the notes thread when the app is closed
st.experimental_rerun()  # Rerun the app when the user closes it to stop the thread