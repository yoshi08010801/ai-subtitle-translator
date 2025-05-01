import streamlit as st
from openai import OpenAI
import os

# OpenAI APIキーを環境変数から取得（または直接書いてもOK）
api_key = os.getenv("OPENAI_API_KEY")  # 安全な方法
client = OpenAI(api_key=api_key)

# SRTファイルを読み込んで翻訳
def translate_text(text, target_lang="en"):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"Translate the following subtitles into {target_lang}."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()

# Streamlit UI
st.title("Subtitle Translator App")
uploaded_file = st.file_uploader("Upload an SRT file", type=["srt"])

if uploaded_file:
    original_srt = uploaded_file.read().decode("utf-8")
    st.text_area("Original Subtitles", original_srt, height=200)

    if st.button("Translate"):
        with st.spinner("Translating..."):
            translated = translate_text(original_srt)
            st.text_area("Translated Subtitles", translated, height=200)
            st.download_button("Download Translated SRT", translated, file_name="translated.srt")
