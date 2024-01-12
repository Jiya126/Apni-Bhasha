from bhashini_pipelines import bhashini_asr, bhashini_translate, bhashini_tts, record_audio, save_wav
from gemini_response import send_frame_with_text_to_gemini
import base64
import cv2
from collections import deque
from datetime import datetime
import pyaudio

def main():

    print('*'*10, 'Apni_Bhasha', '*'*10)
    input_language = input('Enter your language for communication: ')
    
    pa = pyaudio.PyAudio()
    stream = pa.open(format = pyaudio.paInt16,
                            channels = 1,
                            rate = 44100,
                            input=True,
                            frames_per_buffer = 1024)

    video = cv2.VideoCapture(0)
    previous_texts = deque(maxlen=5)

    while True:
        success, frame = video.read()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cv2.imshow('Video Frame', frame)

        enc = record_audio(stream)
        save_wav(enc)
        enc = base64.b64encode(open("temp\input.wav", "rb").read())
        enc = enc.decode("utf-8")
        asr_output = bhashini_asr(enc, input_language)
        if input_language != 'en':
            translate_output = bhashini_translate(asr_output, input_language)
        else:
            translate_output = asr_output
        print('Query: ', translate_output)        

        generated_text = send_frame_with_text_to_gemini(frame, previous_texts, timestamp, translate_output)

        previous_texts.append(f"Timestamp: {timestamp}\nUser Message: {translate_output}\nYour Response: {generated_text}\n")
        print('Response: ', generated_text, '\n')

        audio_output = bhashini_tts(generated_text, input_language='en')

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break


if __name__ == '__main__':
    main()