# spotify-sc-mp3-fetcher

````markdown
# Spotify → SoundCloud MP3 Downloader

🎵 Fetch tracks from a Spotify playlist and download them from SoundCloud using Python.

**Note:** This tool is for **educational purposes only**. Do **not** use it to distribute copyrighted content.

---

## ⚠️ Legal Disclaimer

- This tool is intended **for personal and educational use only**.  
- Downloading copyrighted music without permission may violate copyright laws in your country.  
- The developer is **not responsible** for any misuse.  

By using this software, you agree to comply with local copyright laws.

---

## 🛠 Setup Instructions

1. **Clone the repository**
```bash
git clone [this repo link]
````

2. **Install dependencies**

```bash
pip install spotipy yt-dlp
```

3. **Set up Spotify API credentials**

   * Create a Spotify Developer app: [https://developer.spotify.com/dashboard/applications](https://developer.spotify.com/dashboard/applications)
   * Copy your **Client ID** and **Client Secret**.
   * Open `downloader.py` and replace:

```python
client_id = ""  # <-- your client ID
client_secret = ""  # <-- your client secret
```

4. **Run the script**

```bash
python downloader.py
```

5. Enter the Spotify **Playlist ID** (not URL) when prompted.
   Downloads will be saved in the `downloads/` folder.

---

## ⚡ Features

* Fetch all tracks from a Spotify playlist.
* Search and download tracks from SoundCloud.
* Clean filenames automatically.
* Uses `yt-dlp` caching for faster downloads.

---

## ❗ Limitations

* Some songs may not be available on SoundCloud.
* Designed for small playlists and educational use only.
* Redistribution of downloaded copyrighted content is **prohibited**.
