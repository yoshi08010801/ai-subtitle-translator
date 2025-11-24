# logic.py  ：アプリのロジックだけ管理

import os
import subprocess
import openai
import streamlit as st


# Whisper: 動画 → SRT変換
def transcribe_video_to_srt(video_path, output_path):
    try:
        subprocess.run(
            [
                "whisper",
                video_path,
                "--model",
                "base",
                "--output_format",
                "srt",
                "--output_dir",
                output_path,
            ],
            check=True,
        )
        srt_file = os.path.join(
            output_path,
            os.path.splitext(os.path.basename(video_path))[0] + ".srt",
        )
        return srt_file
    except Exception as e:
        st.error("Error while transcribing with Whisper: " + str(e))
        return None


# 翻訳機能
def translate_srt(text, target_lang, api_key):
    client = openai.OpenAI(api_key=api_key)
    prompt = (
        f"Translate the following subtitles into natural {target_lang}. "
        "Keep time codes and numbers unchanged. Only translate the text.\n"
        f"{text}"
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Translation error for {target_lang}: " + str(e))
        return ""
