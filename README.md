# Video_Summarizer

mp4_donwloader  downloads YouTube videos and their audio tracks, then converts the downloaded audio from .webm format to .mp3

The script creates a directory structure based on the video ID with the following layout:

Saved_Media/
│
└── <video_id>/
    ├── Video/
    │   └── downloaded_video.<ext>
    ├── Audio/
    │   └── audio.<ext>
    └── MP3/
        └── audio.mp3

See the example on mp4_downloader_example.ipynb on how to run it in the ipynb file
