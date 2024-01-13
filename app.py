import streamlit as st
from bhashini_pipelines import bhashini_asr, bhashini_translate, bhashini_tts, record_audio, save_wav
from gemini_response import send_frame_with_text_to_gemini
import base64
import cv2
from collections import deque
from datetime import datetime
import pyaudio
import os

# Initialize PyAudio
pa = pyaudio.PyAudio()

# Create a stream object
stream = pa.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024,
)

# Initialize video capture
video = cv2.VideoCapture(0)
if not video.isOpened():
    raise IOError("Could not open the camera.")

# Initialize deque to store previous texts
previous_texts = deque(maxlen=5)

# Initialize streamlit app
st.title("Apni_Bhasha")

# Create drop-down menus for input and output languages
input_language = st.selectbox(
    "Select your language for communication:",
    ["en", "hi", "ta", "te", "mr", "bn", "gu", "kn", "ml", "pa", "or", "sa", "ur"],
)
output_language = st.selectbox(
    "Select the language for the response:",
    ["en", "hi", "ta", "te", "mr", "bn", "gu", "kn", "ml", "pa"],
)

# Create text elements to display query and response
# query_text = st.empty()
# response_text = st.empty()

# Get the current state of the toggle
on = st.checkbox('Record')
placeholder = st.empty()

# Create a video capture element
video_frame = st.empty()

input_file_path = 'temp\input.wav'


while True:
    # Read the frame from the video capture
    success, frame = video.read()
    # Check if the frame is empty
    if not success:
        print("Failed to read frame.")
        break

    # Check if the record button is pressed
    if on:
        # Start recording
        placeholder.text("Recording...")
        enc = record_audio(stream)
        placeholder.text("Recording stopped")
        save_wav(enc)

        # Update the on to False
        on = False
        # st.empty()

    if os.path.exists(input_file_path):
        # Encode the audio to base64
        enc = base64.b64encode(open(input_file_path, "rb").read())
        enc = enc.decode("utf-8")
        os.remove(input_file_path)

        # Send the audio to Bhashini ASR
        asr_output = bhashini_asr(enc, input_language)

        # If ASR output is not empty
        if asr_output:
            # Translate the ASR output if langugae != 'en'
            if input_language != 'en':
                translate_output = bhashini_translate(asr_output, input_language)
            else:
                translate_output = asr_output

            # Display the query text
            with st.chat_message('user'):
                st.text(f"Query: {asr_output}")

            # Capture the frame
            # success, frame = video.read()
            # if not success:
            #     print("Failed to read frame.")
            #     break

            # Get the current datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

            # Send the frame and text to Gemini
            generated_text = send_frame_with_text_to_gemini(frame, previous_texts, timestamp, translate_output)

            # Display the response text
            with st.chat_message('assistant'):
                st.text(f"Response: {generated_text}")

            # Add the text to the deque
            previous_texts.append(f"Timestamp: {timestamp}\nUser Message: {translate_output}\nYour Response {generated_text}\n")

            # Play the TTS of the generated text
            bhashini_tts(generated_text, input_language='en')

    # Display the frame
    video_frame.image(frame)


# Release the video capture object
video.release()

# Terminate the PyAudio object
pa.terminate()