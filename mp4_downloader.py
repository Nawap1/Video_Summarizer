import os
import yt_dlp
from moviepy.editor import AudioFileClip

class YouTubeURL:
    def __init__(self, url):
        self.url = url
        self.video_id = self._extract_video_id()

    def _extract_video_id(self):
        return self.url.split('=')[-1]

class MediaDirectory:
    def __init__(self, base_dir, video_id):
        self.base_dir = os.path.join(base_dir, video_id)
        self.video_dir = os.path.join(self.base_dir, 'Video')
        self.audio_dir = os.path.join(self.base_dir, 'Audio')
        self.mp3_dir = os.path.join(self.base_dir, 'MP3')
        self._create_directories()

    def _create_directories(self):
        os.makedirs(self.video_dir, exist_ok=True)
        os.makedirs(self.audio_dir, exist_ok=True)
        os.makedirs(self.mp3_dir, exist_ok=True)

class MediaDownloader:
    def __init__(self, media_directory):
        self.media_directory = media_directory

    def download_video(self, youtube_url):
        opts = {
            'format': 'best',
            'outtmpl': os.path.join(self.media_directory.video_dir, 'downloaded_video.%(ext)s'),
        }
        self._download(youtube_url.url, opts)

    def download_audio(self, youtube_url):
        opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.media_directory.audio_dir, 'audio.%(ext)s'),
        }
        self._download(youtube_url.url, opts)

    def _download(self, url, opts):
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        

class AudioConverter:
    @staticmethod
    def webm_to_mp3(input_file, output_file):
        audio_clip = AudioFileClip(input_file)
        audio_clip.write_audiofile(output_file)
        audio_clip.close()

class YouTubeDownloadManager:
    def __init__(self, youtube_url):
        self.youtube_url = YouTubeURL(youtube_url)
        self.media_directory = MediaDirectory('Saved_Media', self.youtube_url.video_id)
        self.downloader = MediaDownloader(self.media_directory)
        self.converter = AudioConverter()

    def process(self):
        self.download_media()
        self.convert_audio()

    def download_media(self):
        self.downloader.download_video(self.youtube_url)
        self.downloader.download_audio(self.youtube_url)
        print("Download completed!")

    def convert_audio(self):
        input_file = os.path.join(self.media_directory.audio_dir, 'audio.webm')
        output_file = os.path.join(self.media_directory.mp3_dir, 'audio.mp3')
        self.converter.webm_to_mp3(input_file, output_file)
        print("Conversion completed!")

def mp4_mp3_webm_retreiver(link):
    youtube_video_url = link
    manager = YouTubeDownloadManager(youtube_video_url)
    manager.process()

if __name__ == "__main__":
    # Change the link to the video you want to download
    mp4_mp3_webm_retreiver("https://www.youtube.com/watch?v=y4zdDXPYo0I")