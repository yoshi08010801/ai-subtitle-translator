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

# ロジック層を別ファイルから読み込み
from logic import transcribe_video_to_srt, translate_srt

# 環境変数から API キー読み込み（.env 用）
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

# メイン処理
if uploaded_file and api_key and selected_langs:
    if st.button("🌐 Translate to All Selected Languages"):
        with st.spinner("🔁 Translating into multiple languages, please wait..."):
            # 一時フォルダにファイル保存
            with tempfile.TemporaryDirectory() as tmpdir:
                filepath = os.path.join(tmpdir, uploaded_file.name)
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getvalue())

                # 入力が SRT か動画かで分岐
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

                # 翻訳結果を ZIP にまとめる
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zipf:
                    for lang in selected_langs:
                        translated = translate_srt(srt_text, lang, api_key)  # ← api_key を渡すのがポイント
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
