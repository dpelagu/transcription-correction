import streamlit as st
import requests
import os
import openai
from dotenv import load_dotenv

# Cargar claves API desde el archivo .env
load_dotenv()

GLADIA_API_KEY = os.getenv("GLADIA_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurar claves API para OpenAI
openai.api_key = OPENAI_API_KEY

# Interfaz en Streamlit
st.title('Transcripción y Corrección de Audios con Gladia y GPT')

# Subida de archivo de audio
audio_file = st.file_uploader("Sube tu archivo de audio", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.audio(audio_file, format='audio/wav')

    # Paso 1: Enviar archivo de audio a Gladia para transcripción
    with st.spinner("Transcribiendo el audio..."):
        url = "https://api.gladia.io/audio/text/audio-transcription/"
        headers = {
            "accept": "application/json",
            "x-gladia-key": GLADIA_API_KEY
        }
        files = {"audio": audio_file}
        
        response = requests.post(url, headers=headers, files=files)

        if response.status_code == 200:
            transcription = response.json()["text"]
            st.write("**Transcripción inicial:**")
            st.text_area("Texto transcrito:", transcription, height=200)

            # Paso 2: Usar GPT para corregir el texto transcrito
            with st.spinner("Corrigiendo la transcripción..."):
                prompt = f"Corrige el siguiente texto transcrito: {transcription}"
                
                corrected_response = openai.Completion.create(
                    model="text-davinci-003",  # O puedes usar gpt-4 si tienes acceso
                    prompt=prompt,
                    max_tokens=2000
                )
                
                corrected_text = corrected_response['choices'][0]['text']
                st.write("**Texto corregido:**")
                st.text_area("Texto corregido:", corrected_text, height=200)
        else:
            st.error("Error en la transcripción. Verifica el archivo y vuelve a intentarlo.")
