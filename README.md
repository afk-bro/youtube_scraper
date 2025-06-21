# 🧠 YouTube Transcript Scraper

A modern, modular Python application for automatically downloading and distilling YouTube video transcripts. Designed to generate clean, chunked, and optionally summarized outputs for use in Retrieval-Augmented Generation (RAG) systems or other AI pipelines.

---

## 🚀 Features

- 🎬 Scrape transcripts from single YouTube videos or full playlists
- 🌍 Language selection support (`--lang`)
- ✂️ Automatic filtering of filler content, music cues, and low-signal noise
- 📦 Output formats: `.txt`, `.json`, `.csv`, `.md`
- 🧠 Optional AI-powered summarization via Perplexity API
- 📂 Structured transcript metadata per video
- 🧱 Modular architecture ready for integration with RAG pipelines

---

## 📦 Installation

```bash
git clone https://github.com/afk-bro/youtube-scraper.git
cd youtube-scraper
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## 🧪 CLI Usage
List Available Transcript Languages

python -m src.main list-langs --url https://www.youtube.com/watch?v=VIDEO_ID

## Scrape and Save Transcript

python -m src.main scrape \
  --url https://www.youtube.com/watch?v=VIDEO_ID \
  --lang en \
  --format json

 ## 🗃 Output Structure
 transcripts/
├── some_video_title.json
├── some_video_title.meta.json
└── some_video_title.csv  # if CSV format is used

Each .meta.json file contains:
{
  "video_id": "abc123",
  "file_path": "transcripts/Video_Title.json",
  "format": "json",
  "language": "en",
  "word_count": 1023,
  "entry_count": 76,
  "timestamp": "2025-06-17T17:51:11.543817Z"
}

## 👨‍💻 Author
Made with precision by afk-bro
“Clean signal, clear context, distilled insight.”