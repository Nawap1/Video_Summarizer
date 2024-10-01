# YouTube Summarizer

This project utilizes the lightweight LLM 'Phi-3.5-mini' to summarize YouTube videos. We employ a 4-bit quantized version of the model to optimize performance while maintaining accuracy. The app transcribes audio from YouTube videos using Whisper (or uses existing subtitles if available) and then generates a summary using the Phi-3 model.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the API](#running-the-api)
- [Hosting the YouTube Summarizer App](#hosting-the-youtube-summarizer-app)
- [Usage](#usage)
- [Demo](#demo)


## Features

- Transcribe YouTube video audio using Whisper
- Use existing subtitles if available
- Summarize transcribed text using Phi-3 model
- User-friendly web interface

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8+
- Node.js and npm
- Git

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/....................
```

### 2. Download the Quantized Model

- Navigate to [this link](https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_L.gguf?download=true) and download the **Phi-3.5-mini-instruct-Q4_K_L.gguf** model.
- Create a directory `/Model` in the project root and place the downloaded quantized model inside.

### 3. Install Ollama

- Download Ollama from [here](https://ollama.com/).
- Install Ollama following the provided instructions.

### 4. Prepare the Model

- Copy the downloaded model file into the project directory.
- Create a file named `Modelfile` in the same directory and paste the following content:

```text
FROM Phi-3.5-mini-instruct-Q4_K_L.gguf
SYSTEM You are a helpful AI assistant specialized in summarizing YouTube transcripts.
# Adjust model parameters
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.95
```

### 5. Create the Ollama Model

Open a terminal and run the following command:

```bash
ollama create quantphi -f Modelfile
```

### 6. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Running the API

1. Navigate to the API directory:

```bash
cd api
```

2. Start the API:

```bash
python api.py
```

The API should now be running on `http://localhost:5000`.

## Hosting the YouTube Summarizer App

1. Navigate to the app directory:

```bash
cd app
```

2. Install frontend dependencies:

```bash
npm install
```

3. Run the app:

```bash
npm run dev
```

The app should now be accessible at `http://localhost:3000`.

## Usage

1. Open your web browser and go to `http://localhost:3000`.
2. Paste a YouTube video URL into the input field.
3. Click the "Summarize" button.
4. Wait for the app to process the video and generate a summary.
5. Read the generated summary of the YouTube video content.

## Demo

A demo video showcasing the app's functionality is available below. In the demo, a YouTube video link (https://www.youtube.com/watch?v=NiKtZgImdlY) is pasted into the app, and after a brief processing time, a summary of the video content is generated.

This is the demo video.

https://github.com/user-attachments/assets/ac89f6f9-6ee6-40b8-b632-c0ab1cd7a372

