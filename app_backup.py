# app.py
import streamlit as st
import openai
import os
import tempfile
import subprocess
from dotenv import load_dotenv
import time
import zipfile
from io import BytesIO

# Load API key
load_dotenv()

st.set_page_config(page_title="Subtitle Translator App", layout="centered")
st.title("🎬 Subtitle Translator App - Multi-language SRT Translator")

# File type selection
input_type = st.radio("Select file type", ("Subtitle file (.srt)", "Video file (.mp4)"))

# API key input
api_key = st.text_input("Enter your OpenAI API key", type="password")

# YouTube-supported languages
youtube_languages = [
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", "Basque", "Belarusian",
    "Bengali", "Bosnian", "Bulgarian", "Catalan", "Cebuano", "Chinese (Simplified)", "Chinese (Traditional)",
    "Corsican", "Croatian", "Czech", "Danish", "Dutch", "English", "Esperanto", "Estonian", "Filipino",
    "Finnish", "French", "Frisian", "Galician", "Georgian", "German", "Greek", "Gujarati", "Haitian Creole",
    "Hausa", "Hawaiian", "Hebrew", "Hindi", "Hmong", "Hungarian", "Icelandic", "Igbo", "Indonesian", "Irish",
    "Italian", "Japanese", "Javanese", "Kannada", "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish",
    "Kyrgyz", "Lao", "Latin", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", "Malay",
    "Malayalam", "Maltese", "Maori", "Marathi", "Mongolian", "Myanmar", "Nepali", "Norwegian", "Nyanja",
    "Odia", "Pashto", "Persian", "Polish", "Portuguese (Portugal)", "Portuguese (Brazil)", "Punjabi",
    "Romanian", "Russian", "Samoan", "Scots Gaelic", "Serbian", "Sesotho", "Shona", "Sindhi", "Sinhala",
    "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", "Tajik", "Tamil",
    "Tatar", "Telugu", "Thai", "Turkish", "Turkmen", "Ukrainian", "Urdu", "Uyghur", "Uzbek", "Vietnamese",
    "Welsh", "Xhosa", "Yiddish", "Yoruba", "Zulu"
]
selected_langs = st.multiselect("Select target translation languages", youtube_languages)

uploaded_file = st.file_uploader("Upload your file", type=["srt", "mp4"])

# Whisper transcription (requires whisper CLI)
def transcribe_video_to_srt(video_path, output_path):
    try:
        subprocess.run(["whisper", video_path, "--model", "base", "--output_format", "srt", "--output_dir", output_path], check=True)
        srt_file = os.path.join(output_path, os.path.splitext(os.path.basename(video_path))[0] + ".srt")
        return srt_file
    except Exception as e:
        st.error("Error while transcribing with Whisper: " + str(e))
        return None

# Translation function
def translate_srt(text, target_lang):
    client = openai.OpenAI(api_key=api_key)
    prompt = f"Translate the following subtitles into natural {target_lang}. Keep time codes and numbers unchanged. Only translate the text.\n{text}"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Translation error for {target_lang}: " + str(e))
        return ""

if uploaded_file and api_key and selected_langs:
    if st.button("🌐 Translate to All Selected Languages"):
        with st.spinner("🔁 Translating into multiple languages, please wait..."):
            with tempfile.TemporaryDirectory() as tmpdir:
                filepath = os.path.join(tmpdir, uploaded_file.name)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getvalue())

                if input_type == "Subtitle file (.srt)":
                    with open(filepath, "r", encoding="utf-8") as f:
                        srt_text = f.read()
                else:
                    st.info("Generating subtitles with Whisper...")
                    srt_path = transcribe_video_to_srt(filepath, tmpdir)
                    if srt_path and os.path.exists(srt_path):
                        with open(srt_path, "r", encoding="utf-8") as f:
                            srt_text = f.read()
                    else:
                        st.stop()

                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zipf:
                    for lang in selected_langs:
                        translated = translate_srt(srt_text, lang)
                        filename = f"translated_{lang.replace(' ', '_')}.srt"
                        zipf.writestr(filename, translated)

                zip_buffer.seek(0)

        st.success("🎉 Translation complete! Your subtitles are ready.")
        st.balloons()
        time.sleep(1.5)

        st.download_button(
            label="📦 Download All Translations (ZIP)",
            data=zip_buffer,
            file_name="translated_subtitles.zip",
            mime="application/zip"
        )