# speech_rec.py

import os
import speech_recognition as sr

def recognize_speech(audio_file_path):
    if not os.path.isfile(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file_path) as source:
            audio_data = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio_data)

        return transcribed_text

    except Exception as e:
        raise RuntimeError(f"Error processing audio file: {e}")
