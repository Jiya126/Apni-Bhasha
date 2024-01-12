import google.generativeai as genai
import cv2
from collections import deque
import os
import PIL
from datetime import datetime

def save_temp_frame(frame, filename, directory='./temp'):
    # Create the directory if it does not exist
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Creating the path for the filename
    filepath = os.path.join(directory, filename)
    # Saving the frame
    cv2.imwrite(filepath, frame)
    return filepath  # Returning the path of the saved file


def send_frame_with_text_to_gemini(frame, previous_texts, timestamp, user_input, client = genai):
    ############### ENTER GEMINI API KEY ###################
    genai.configure(api_key='ENTER YOUR KEY HERE')
    temp_file_path = save_temp_frame(frame, "temp.jpg")
    img = PIL.Image.open(temp_file_path)

    # Combining past texts as context
    context = ' '.join(previous_texts)

    # Adding system message
    system_message = "System Message - Your identity: Gemini, you are helpful AI assistant."

    # Initializing Gemini model
    model = client.GenerativeModel('gemini-pro-vision')

    # Sending image and text instructions to the model
    prompt = f"{system_message}\nGiven the context: {context} and the current time: {timestamp},please respond to the following message without repeating the context. Message: {user_input}"
    
    response = model.generate_content([prompt, img], stream=True)
    response.resolve()
    # Returning the generated text
    return response.text