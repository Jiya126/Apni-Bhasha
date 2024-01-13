# Apni Bhasha

Apni Bhasha is a streamlit application that allows users to have a conversation with a generative model in a choice of Indian languages. It takes in audio input and live video feed, and responds with audio output.

**Features:**

* **Generative model:** Apni Bhasha uses a generative model that is trained on a large corpus of text and audio data in multiple Indian languages. This allows the model to generate natural-sounding text in response to user input.
* **Speech recognition:** Apni Bhasha uses the Bhashini API for speech recognition. This API can recognize speech in multiple Indian languages: Hindi, Marathi, Bengali, Telugu, Tamil, Kannada, Malayalam, Gujarati, Punjabi, and Odia.
* **Text-to-speech:** Apni Bhasha uses the Bhashini API for text-to-speech. This API can synthesize speech in 10 Indian languages.
* **Translation:** Apni Bhasha uses the Bhashini API for translation. This API can translate text between any two of the 10 Indian languages supported by the app.
* **Live video feed:** Apni Bhasha uses the Gemini Vision API for taking in live video feed. This API can be used to track the user's head pose and gaze.

**How to Use:**

1. Clone the repository to your local machine:

```
git clone https://github.com/Jiya126/Apni-Bhasha.git
```

2. Install the required Python packages:

```
pip install -r requirements.txt
```

3. Start the app:

```
streamlit run app.py
```

4. Visit http://localhost:8501 in your web browser.
