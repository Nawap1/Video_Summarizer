import os
import shutil
import yt_dlp
from moviepy.editor import AudioFileClip

def download_youtube_content(url, base_dir='Saved_Media'):
    video_id = url.split('=')[-1]
    
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    video_opts = {
        'format': 'best',
        'outtmpl': os.path.join(base_dir, 'downloaded_video.%(ext)s'),
    }

    audio_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(base_dir, 'audio.%(ext)s'),
    }

    for opts in [video_opts, audio_opts]:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])

    print("Download completed!")

def convert_audio_to_mp3(input_file, output_file):
    audio_clip = AudioFileClip(input_file)
    audio_clip.write_audiofile(output_file)
    audio_clip.close()
    print("Conversion completed!")

def main(youtube_video_url):
    base_dir = 'Saved_Media'
    
    download_youtube_content(youtube_video_url, base_dir)
    
    input_file = os.path.join(base_dir, 'audio.webm')
    output_file = os.path.join(base_dir, 'conv_mp3_audio.mp3')
    
    convert_audio_to_mp3(input_file, output_file)

if __name__ == "__main__":
    youtube_video_url = "https://www.youtube.com/watch?v=y4zdDXPYo0I"
    main(youtube_video_url)