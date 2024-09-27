# Youtube Summarizer

This project utilizes the lightweight LLM 'Phi-3.5-mini' for the task of summarizing YouTube videos. We employ a 4-bit quantized version of the model to optimize performance while maintaining accuracy.

## Table of Contents
- [Setup](#setup)
- [Running the API](#running-the-api)
- [Hosting the Youtube Summarizer App](#hosting-the-youtube-summarizer-app)

---

## Setup

To set up the LLM, follow the instructions below:

### 1. Download the Quantized Model

- Navigate to this [link](https://huggingface.co/bartowski/Phi-3.5-mini-instruct-GGUF/resolve/main/Phi-3.5-mini-instruct-Q4_K_L.gguf?download=true) and download the **Phi-3.5-mini-instruct-Q4_K_L.gguf** model.

### 2. Install Ollama

- Download Ollama from [here](https://ollama.com/).
- After downloading, install Ollama following the provided instructions.

### 3. Prepare the Model

- Copy the downloaded model file into the project directory.
- Create a file named `Modelfile` in the same directory and paste the following content inside it:

```text
FROM Phi-3.5-mini-instruct-Q4_K_L.gguf
SYSTEM You are a helpful AI assistant specialized in summarizing YouTube transcripts.

# Adjust model parameters
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.95
```

### 4. Create the Ollama Model

- Open a terminal and run the following command to create the Ollama model:

```bash
ollama create quantphi -f Modelfile
```

---

## Running the API

To run the API for summarizing YouTube videos, follow these steps:

### 1. Clone the Repository

Clone this repository using the following command:

```bash
git clone <repo-url>
```

### 2. Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the API

Run the API using the following command:

```bash
python api.py
```

---

## Hosting the Youtube Summarizer App

To host the web app for summarizing YouTube videos, follow these instructions:

### 1. Navigate to the App Directory

Move to the `app` directory:

```bash
cd app
```

### 2. Install Frontend Dependencies

Install the necessary dependencies for the Next.js app:

```bash
npm install
```

### 3. Run the App

Host the app using the following command:

```bash
npx next dev
```

---
