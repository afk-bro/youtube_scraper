from pytube import Playlist

def get_video_ids_from_playlist(playlist_url):
    try:
        pl = Playlist(playlist_url)
        return [video.video_id for video in pl.videos]
    except Exception as e:
        print(f"[ERROR] Could not load playlist: {e}")
        return []
