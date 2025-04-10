import streamlit as st
import os
import tempfile
from yt_dlp import YoutubeDL

st.set_page_config(page_title="YouTube to MP3", layout="centered")
st.title("🎵 YouTube to MP3 Downloader")

url = st.text_input("Enter a YouTube Video URL")

if st.button("Convert to MP3"):
    if not url:
        st.warning("Please enter a valid YouTube URL.")
    else:
        with st.spinner("Downloading and converting..."):
            try:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(tmp_dir, '%(title)s.%(ext)s'),
                        'ffmpeg_location': '/usr/bin/ffmpeg',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                        'prefer_ffmpeg': True,
                        'quiet': True,
                        'noplaylist': True,
                        'http_headers': {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
                        }
                    }

                    with YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=True)
                        title = info.get('title', 'audio')
                        filename = os.path.join(tmp_dir, f"{title}.mp3")

                    if os.path.exists(filename):
                        with open(filename, "rb") as f:
                            st.success(f"Download Ready: {title}.mp3")
                            st.download_button(
                                label="🎧 Download MP3",
                                data=f,
                                file_name=f"{title}.mp3",
                                mime="audio/mpeg"
                            )
                    else:
                        st.error("Something went wrong. File not found.")
            except Exception as e:
                st.error(f"Error: {e}")
