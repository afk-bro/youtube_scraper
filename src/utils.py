import re
import os
import json
import pandas as pd
from datetime import datetime
from pytube import YouTube

def extract_video_id(url_or_id):
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", url_or_id)
        return match.group(1) if match else None
    return url_or_id

def get_video_title(video_id):
    try:
        url = f"https://www.youtube.com/watch?v={video_id}"
        yt = YouTube(url)
        title = yt.title.strip()
        return title
    except Exception as e:
        print(f"[WARNING] Could not fetch title for {video_id}: {e}")
        return f"video_{video_id}"   # fallback
    
def sanitize_filename(name: str) -> str:
    return re.sub(r"[^\w\-_.() ]", "", name).strip().replace(" ", "_")

def save_transcript(video_id, transcript, output_format="txt", output_dir="transcripts", language="unknown"):
    if not transcript:
        print(f"[INFO] No transcript for {video_id}")
        return None
    
    title = get_video_title(video_id)
    safe_title = sanitize_filename(title)

    os.makedirs(output_dir, exist_ok=True)
    file_base = os.path.join(output_dir, safe_title)
    file_path = f"{file_base}.{output_format}"
    word_count = sum(len(entry["text"].split()) for entry in transcript)

    if output_format == "txt":
        with open(file_path, "w", encoding="utf-8") as f:
            for entry in transcript:
                f.write(f"{entry['text']}\n")

    elif output_format == "csv":
        pd.DataFrame(transcript).to_csv(file_path, index=False)

    elif output_format == "json":
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(transcript, f, ensure_ascii=False, indent=2)

    elif output_format == "md":
        with open(file_path, "w", encoding="utf-8") as f:
            for entry in transcript:
                f.write(f"- {entry['text']}\n")

    else:
        print(f"[WARNING] Unsupported format: '{output_format}'. No file saved.")
        return None

    print(f"[SUCCESS] Saved transcript to {file_path}")
    print(f"[INFO] Word count: ~{word_count}")

    meta = {
        "video_id": video_id,
        "video_title": title,
        "file_path": file_path,
        "format": output_format,
        "language": language,
        "word_count": word_count,
        "entry_count": len(transcript),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    with open(f"{file_base}.meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

    return meta