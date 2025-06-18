from youtube_transcript_api import YouTubeTranscriptApi
from src.utils import extract_video_id, save_transcript, distill_transcript
from src.playlist import get_video_ids_from_playlist

def list_transcript_languages(video_id):
    try:
        transcripts = YouTubeTranscriptApi.list_transcripts(video_id)
        return [
            {
                "language": t.language,
                "language_code": t.language_code
            }
            for t in transcripts
        ]
    except Exception as e:
        print(f"[ERROR] Could not retrieve transcript list for {video_id}: {e}")
        return []

def fetch_transcript(video_id, preferred_lang="en"):
    try:
        return YouTubeTranscriptApi.get_transcript(video_id, languages=[preferred_lang, "en"])
    except Exception as e:
        print(f"[ERROR] Failed to fetch transcript for {video_id}: {e}")
        return None
    
def chunk_transcript(entries, chunk_size=3):
    chunks = []
    buffer = []

    for entry in entries:
        buffer.append(entry["text"])
        if len(buffer) >= chunk_size:
            chunks.append({"text": " ".join(buffer)})
            buffer = []

    if buffer:
        chunks.append({"text": " ".join(buffer)})

    return chunks

def process_video_or_playlist(url, output_format="txt", preferred_lang="en"):
    video_ids = []

    if "playlist" in url:
        video_ids = get_video_ids_from_playlist(url)
    else:
        vid = extract_video_id(url)
        if vid:
            video_ids.append(vid)

    for video_id in video_ids:
        transcript = fetch_transcript(video_id, preferred_lang)
        if not transcript:
            continue

        filtered = distill_transcript(transcript)
        chunked = chunk_transcript(filtered)

    print(f"[INFO] Processed {video_id}: {len(chunked)} chunks saved.")

    save_transcript(video_id, chunked, output_format, language=preferred_lang)
