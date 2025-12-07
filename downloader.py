import os
import sys
import traceback
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp

ASCII_ART = r"""

                ________o8A888888o_
            _o888888888888K_]888888o
                      ~~~+8888888888o
                          ~8888888888
                          o88888888888
                         o8888888888888
                       _8888888888888888
                      o888888888888888888_
                     o88888888888888888888_
                    _8888888888888888888888_
                    888888888888888888888888_
                    8888888888888888888888888
                    88888888888888888888888888
                    88888888888888888888888888
                    888888888888888888888888888
                    ~88888888888888888888888888_
                     (88888888888888888888888888
                      888888888888888888888888888
                       888888888888888888888888888_
                       ~8888888888888888888888888888
                         +88888888888888888888~~~~~
                          ~=888888888888888888o
                   _=oooooooo888888888888888888
                    _o88=8888==~88888888===8888_   unknown
                    ~   =~~ _o88888888=      ~~~
                            ~ o8=~88=~
                     
Spotify → SoundCloud MP3 Downloader (Python 3.14)
"""


# CONFIG, scroll down an replace client id and secret!!!

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
SONG_FILE = "songs.txt"
CACHE_DIR = "./yt-dlp-cache"
os.makedirs(CACHE_DIR, exist_ok=True)


# UTILITY FUNCTIONS
def safe_filename(text):
    """Remove invalid filename characters for filesystem."""
    banned = ['<','>',':','"','/','\\','|','?','*']
    for b in banned:
        text = text.replace(b, "")
    return text

def clean_query(text):
    """Remove special characters for search."""
    return re.sub(r"[^a-zA-Z0-9\s]", "", text)


# SPOTIFY FUNCTIONS
def fetch_spotify_tracks(playlist_id, client_id, client_secret):
    """Fetch tracks from Spotify playlist and save to SONG_FILE."""
    try:
        print("[+] Authenticating with Spotify...")
        auth = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=auth)
    except Exception as e:
        print("❌ Spotify authentication failed.")
        print(e)
        sys.exit(1)

    try:
        print("[+] Fetching playlist tracks...")
        results = sp.playlist_tracks(playlist_id)
        tracks = results["items"]

        while results["next"]:
            results = sp.next(results)
            tracks.extend(results["items"])

        print(f"[+] Found {len(tracks)} tracks.")

        with open(SONG_FILE, "w", encoding="utf-8") as f:
            for item in tracks:
                track = item["track"]
                artists = ", ".join([a["name"] for a in track["artists"]])
                line = f"{track['name']} : {artists}"
                f.write(line + "\n")

        print(f"[✓] Saved track list to {SONG_FILE}")
    except Exception as e:
        print("❌ Failed to fetch tracks from playlist.")
        traceback.print_exc()
        sys.exit(1)

# SOUNDCLOUD SEARCH & DOWNLOAD
def search_soundcloud(query, max_results=3):
    """Search SoundCloud using yt-dlp and return the first track URL."""
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'cache_dir': CACHE_DIR
    }
    search_query = f"scsearch{max_results}:{query}"  # SoundCloud search

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(search_query, download=False)
            if 'entries' in info and len(info['entries']) > 0:
                first = info['entries'][0]
                if 'webpage_url' in first:
                    return first['webpage_url']
            return None
    except Exception as e:
        print(f"❌ SoundCloud search error for '{query}': {e}")
        return None

def download_audio(url, title):
    """Download audio from SoundCloud using yt-dlp with cache fix."""
    ydl_opts = {
        "cache_dir": CACHE_DIR,
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/{title}.%(ext)s",
        "quiet": False,
        "ignoreerrors": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return True
    except Exception as e:
        print(f"❌ Failed to download {title}: {e}")
        return False

# MAIN CLI
def main():
    print(ASCII_ART)
    print("Welcome! This tool fetches a Spotify playlist and downloads the songs from SoundCloud.\n")

    playlist_id = input("Enter Spotify Playlist ID (not URL): ").strip()


    client_id = "".strip() #change THIS to your spotify client id 
    client_secret = "".strip() #change THIS to your spotify client secret

    fetch_spotify_tracks(playlist_id, client_id, client_secret)

    try:
        with open(SONG_FILE, "r", encoding="utf-8") as f:
            songs = [line.strip() for line in f.readlines()]
    except Exception as e:
        print(f"❌ Failed to read {SONG_FILE}: {e}")
        sys.exit(1)

    print("\n[+] Starting download from SoundCloud...\n")

    for song in songs:
        if not song:
            continue

        if " : " in song:
            song_name, artists = song.split(" : ", 1)
            query = f"{song_name} {artists.split(',')[0]}"
        else:
            query = song

        query = clean_query(query)
        url = search_soundcloud(query, max_results=3)

        if not url:
            print(f"[-] No SoundCloud result found for '{query}', skipping.\n")
            continue

        print(f"[✓] Found: {url}")
        filename = safe_filename(song)
        if download_audio(url, filename):
            print(f"[✓] Downloaded: {filename}.mp3\n")
        else:
            print(f"[-] Failed to download: {filename}\n")

    print("\n🎉 All done! Check the 'downloads' folder.")

if __name__ == "__main__":
    main()
