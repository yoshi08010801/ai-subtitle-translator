# 🎬 AI Subtitle Translator – GPT + Whisper Tool

Easily translate `.srt` or `.mp4` subtitle files into 100+ languages using OpenAI's GPT and Whisper.  
Perfect for YouTubers, educators, and content creators who want to reach a global audience.

## 🔧 Features
- Translate `.srt` or `.mp4` subtitle files
- Supports 100+ languages (YouTube-compatible)
- Simple and intuitive GUI built with Streamlit
- Cross-platform (macOS & Windows)
- No coding skills required
- Fully open-source and customizable

## 📦 Included Files
- `app.py` — GUI launcher (Streamlit)  
- `main.py` — Subtitle translation logic  
- `requirements.txt` — Dependency list  
- `.env.template` — Sample for setting up OpenAI API key  
- `sample_files/test_subtitles.srt` — Sample subtitle file  

## 🚀 Getting Started
Follow these steps to run the tool locally on your machine.

### 1. Clone this repository
git clone https://github.com/yoshi08010801/ai-subtitle-translator.git  
cd ai-subtitle-translator

### 2. Install dependencies
Make sure Python 3.9+ is installed, then run:
pip install -r requirements.txt

If you get an error with `whisper`, run:
pip install git+https://github.com/openai/whisper.git

### 3. Set up your OpenAI API key
Copy `.env.template` and rename it to `.env`, then open it and insert:
OPENAI_API_KEY=your_openai_key_here

Get your key here: https://platform.openai.com/account/api-keys

### 4. Run the app
streamlit run app.py

Your browser will open the GUI automatically.

## 🔗 Try without setup (no install required)
Don’t want to install anything?

Download the ready-to-use version here (free, no signup):  
https://yoshiverse1.gumroad.com

## 🧠 Powered by
- OpenAI GPT
- OpenAI Whisper
- Streamlit

## 📄 License
MIT License – Free to use, modify, and distribute.

Enjoy translating your content into the world! 🌍  
If you find this helpful, give it a ⭐ on GitHub or share it with others!
