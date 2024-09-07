import os
import torch
import librosa
import numpy as np
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from typing import List, Tuple



class WhisperTranscriber:
    def __init__(self, model_name: str = "openai/whisper-tiny"):
        """
        Initialize the WhisperTranscriber with a specified model.

        Args:
            model_name (str): The name of the Whisper model to use.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        self.processor = WhisperProcessor.from_pretrained(model_name)
        self.model = WhisperForConditionalGeneration.from_pretrained(model_name).to(self.device)
        self.model.eval()

    @staticmethod
    def load_audio(file_path: str, target_sampling_rate: int = 16000) -> Tuple[np.ndarray, int]:
        """
        Load and resample audio to 16kHz if necessary using librosa.

        Args:
            file_path (str): Path to the audio file.
            target_sampling_rate (int): Target sampling rate (default: 16000).

        Returns:
            Tuple[np.ndarray, int]: Resampled audio array and sampling rate.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        try:
            audio, sr = librosa.load(file_path, sr=target_sampling_rate, mono=True)
            return audio, sr
        except Exception as e:
            raise RuntimeError(f"Error loading audio file: {e}. Make sure the file format is supported by librosa.")

    @staticmethod
    def chunk_audio(audio: np.ndarray, chunk_length: int = 30, sampling_rate: int = 16000) -> List[np.ndarray]:
        """
        Split audio into chunks for long transcriptions.

        Args:
            audio (np.ndarray): The audio array.
            chunk_length (int): Length of each chunk in seconds (default: 30).
            sampling_rate (int): Sampling rate of the audio (default: 16000).

        Returns:
            List[np.ndarray]: List of audio chunks.
        """
        chunk_size = chunk_length * sampling_rate
        return [audio[i:i+chunk_size] for i in range(0, len(audio), chunk_size)]

    def transcribe_chunk(self, chunk: np.ndarray, sampling_rate: int = 16000) -> str:
        """
        Transcribe a single audio chunk.

        Args:
            chunk (np.ndarray): Audio chunk to transcribe.
            sampling_rate (int): Sampling rate of the audio (default: 16000).

        Returns:
            str: Transcribed text.
        """
        input_features = self.processor(chunk, sampling_rate=sampling_rate, return_tensors="pt").input_features
        input_features = input_features.to(self.device)

        with torch.no_grad():
            predicted_ids = self.model.generate(input_features)

        return self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

    def transcribe(self, file_path: str, chunk_length: int = 30) -> str:
        """
        Transcribe long audio by chunking.

        Args:
            file_path (str): Path to the audio file.
            chunk_length (int): Length of each chunk in seconds (default: 30).

        Returns:
            str: Full transcription of the audio.
        """
        audio, sampling_rate = self.load_audio(file_path)
        chunks = self.chunk_audio(audio, chunk_length, sampling_rate)
        
        transcriptions = [self.transcribe_chunk(chunk, sampling_rate) for chunk in chunks]
        return " ".join(transcriptions)

def main():
    try:
        transcriber = WhisperTranscriber()
        audio_file = "sample_audio.mp3"
        
        # Check if the file exists
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")
        
        # Check if the file is empty
        if os.path.getsize(audio_file) == 0:
            raise ValueError(f"Audio file is empty: {audio_file}")
        
        transcription = transcriber.transcribe(audio_file, chunk_length=30)
        print(transcription)
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except ValueError as e:
        print(f"Invalid file error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()