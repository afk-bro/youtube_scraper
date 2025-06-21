from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.utils import extract_video_id, save_transcript, distill_transcript
from src.playlist import get_video_ids_from_playlist
from src.distiller import distill_with_local_llm
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    
def chunk_transcript(entries, chunk_size_tokens=2000, overlap_tokens=200):
    """
    Combine all transcript lines into one string, then split it into chunks
    based on token count using LangChain's RecursiveCharacterTextSplitter.
    """
    full_text = " ".join(entry["text"] for entry in entries)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size_tokens,
        chunk_overlap=overlap_tokens,
        separators=["\n\n", "\n", ".", " ", ""],  # handles natural boundaries
    )

    chunks = splitter.create_documents([full_text])
    return [{"text": chunk.page_content} for chunk in chunks]

def distill_chunk_parallel(chunks, max_workers=4):
    def task(chunk):
        try:
            distilled = distill_with_local_llm(chunk["text"])
            return {"text": distilled}
        except Exception as e:
            print(f"[ERROR] Distillation failed: {e}")
            return {"text": "[ERROR] Distillation failed."}

    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(task, chunk) for chunk in chunks]
        for future in as_completed(futures):
            results.append(future.result())

    return results

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
        #Logging
        print(f"[DEBUG] Filtered {len(filtered)} high-signal lines")
        print(f"[DEBUG] Example filtered line:\n  {filtered[0]['text'] if filtered else '[empty]'}")

        chunked = chunk_transcript(filtered)
        print(f"[DEBUG] Created {len(chunked)} token chunks")
        print(f"[DEBUG] Example raw chunk:\n  {chunked[0]['text'][:300]}...\n")

        chunked = distill_chunk_parallel(chunked)
        print(f"[DEBUG] Distilled {len(chunked)} chunks")
        print(f"[DEBUG] Example distilled chunk:\n  {chunked[0]['text'][:300]}...\n")


    print(f"[INFO] Processed {video_id}: {len(chunked)} chunks saved.")

    save_transcript(video_id, chunked, output_format, language=preferred_lang)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Process YouTube video or playlist")
    parser.add_argument("--url", required=True, help="YouTube video or playlist URL")
    parser.add_argument("--format", default="txt", choices=["txt", "csv", "json", "md"], help="Output format")
    parser.add_argument("--lang", default="en", help="Preferred transcript language")

    args = parser.parse_args()
    process_video_or_playlist(args.url, output_format=args.format, preferred_lang=args.lang)