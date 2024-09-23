import os
import shutil
import yt_dlp
from moviepy.editor import AudioFileClip

def setup_output_directory(output_dir):
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def download_youtube_video_and_audio(video_url, output_dir='Saved_Media'):
    setup_output_directory(output_dir)

    video_options = {
        'format': 'best',
        'outtmpl': os.path.join(output_dir, 'video.%(ext)s'),
    }
    audio_options = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, 'audio.%(ext)s'),
    }

    for download_options in [video_options, audio_options]:
        with yt_dlp.YoutubeDL(download_options) as youtube_downloader:
            youtube_downloader.download([video_url])

    print("Video and audio download completed!")

def convert_audio_to_mp3(input_audio_path, output_mp3_path):
    audio = AudioFileClip(input_audio_path)
    audio.write_audiofile(output_mp3_path)
    audio.close()
    print("Audio conversion to MP3 completed!")

def process_youtube_video(video_url):
    output_dir = 'Saved_Media'
    
    download_youtube_video_and_audio(video_url, output_dir)
    
    input_audio_path = os.path.join(output_dir, 'audio.webm')
    output_mp3_path = os.path.join(output_dir, 'audio.mp3')
    
    convert_audio_to_mp3(input_audio_path, output_mp3_path)

if __name__ == "__main__":
    youtube_video_url = "https://www.youtube.com/watch?v=y4zdDXPYo0I"
    process_youtube_video(youtube_video_url)