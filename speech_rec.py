import os
import speech_recognition as sr
from pydub import AudioSegment

def recognize_speech(audio_file):
    if not os.path.isfile(audio_file):
        raise FileNotFoundError(f"Audio file not found: {audio_file}")

    recognizer = sr.Recognizer()

    try:
        # Convert the audio file to WAV format
        audio = AudioSegment.from_file(audio_file)
        temp_wav_file = "temp_audio.wav"
        audio.export(temp_wav_file, format="wav")

        with sr.AudioFile(temp_wav_file) as source:
            audio_data = recognizer.record(source)
            transcribed_text = recognizer.recognize_google(audio_data)

        return transcribed_text

    except Exception as e:
        raise RuntimeError(f"Error processing audio file: {e}")

    finally:
        
        if os.path.isfile(temp_wav_file):
            os.remove(temp_wav_file)