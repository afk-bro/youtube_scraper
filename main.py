import typer
from src.fetcher import process_video_or_playlist, list_transcript_languages
from src.utils import extract_video_id

app = typer.Typer(help="YouTube Transcript Scraper CLI")

@app.command()
def scrape(
    url: str = typer.Option(..., help="YouTube video or playlist URL"),
    format: str = typer.Option("txt", help="Output format: txt, csv, or json"),
    lang: str = typer.Option("en", help="Preferred transcript language code (e.g. 'en', 'ja')"),
):
    """
    Fetch transcripts from a video or playlist in a specific language (if available).
    """
    process_video_or_playlist(url, output_format=format, preferred_lang=lang)

@app.command()
def list_langs(
    url: str = typer.Option(..., help="YouTube video URL")
):
    """
    List available transcript languages for a YouTube video.
    """
    video_id = extract_video_id(url)
    if not video_id:
        typer.echo("[ERROR] Invalid YouTube URL.")
        raise typer.Exit(code=1)

    langs = list_transcript_languages(video_id)
    if not langs:
        typer.echo("[INFO] No transcripts available.")
        raise typer.Exit()

    typer.echo("Available transcript languages:")
    for lang in langs:
        typer.echo(f"- {lang['language']} ({lang['language_code']})")

if __name__ == "__main__":
    app()
