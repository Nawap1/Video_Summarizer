from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.llms import Ollama
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import TokenTextSplitter
from langchain.schema import Document
from mp4_downloader import *
from transcribe import WhisperTranscriber
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with specific domains to restrict access if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allow specific HTTP methods or all
    allow_headers=["*"],  # Allow specific headers or all
)
class YouTubeURL(BaseModel):
    url: str

def initialize_llm():
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    return Ollama(base_url="http://localhost:11434", model="quantphi", callback_manager=callback_manager)

llm = initialize_llm()
text_splitter = TokenTextSplitter(chunk_size=10000, chunk_overlap=200)

map_template = """<|system|>
You are an AI assistant specialized in understanding and concisely describing video content.
<|end|>
<|user|>
Please describe the main ideas in the following content:
{text}
Provide a brief description of the key points.
<|end|>
<|assistant|>
"""
map_prompt = ChatPromptTemplate.from_template(map_template)

refine_template = """<|system|>
You are an AI assistant specialized in creating concise descriptions of video content.
<|end|>
<|user|>
Here's what we know about a video so far:
{existing_answer}
We have some new information to add:
{text}
Please incorporate this new information and create a single, concise paragraph that captures the main ideas of the entire video. Follow these guidelines:

1. Focus on the most important information and key takeaways.
2. Keep the paragraph brief, ideally 3-4 sentences.
3. Present the information directly without mentioning that it's from a video or a description.
4. Write in a clear, straightforward style.
5. Avoid using meta-language or referring to the writing process.

<|end|>
<|assistant|>
"""
refine_prompt = ChatPromptTemplate.from_template(refine_template)
summarize_chain = load_summarize_chain(
    llm,
    chain_type="refine",
    question_prompt=map_prompt,
    refine_prompt=refine_prompt,
    return_intermediate_steps=True,
    input_key="input_documents",
    output_key="output_text",
    verbose=True
)

def summarize_transcript(transcript):
    chunks = text_splitter.split_text(transcript)
    docs = [Document(page_content=chunk) for chunk in chunks]
    result = summarize_chain({"input_documents": docs})
    return result["output_text"]

@app.post("/summarize")
async def summarize_youtube_video(youtube_url: YouTubeURL):
    try:

        existing_subtitles = extract_subtitles(youtube_url.url)
        if existing_subtitles:
            print("Subtitles found ... Extracted Subtitles from YouTube Video...")
            transcribed_text = existing_subtitles
        else:

            print("Getting YouTube Video's Audio...")
            process_youtube_video(youtube_url.url)
            audio_file = r"Saved_Media\audio.mp3"
            if not os.path.exists(audio_file):
                raise FileNotFoundError(f"Audio file not found: {audio_file}")
            
            print("Transcribing Audio...")

            transcriber = WhisperTranscriber()
            transcribed_text = transcriber.transcribe(audio_file)
        
        print("Summarizing YouTube transcript...")
        summary = summarize_transcript(transcribed_text)
        
        return {"summary": summary}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)