import os
import shutil
from typing import Optional
from pytubefix import YouTube
import speech_recognition as sr
from pydub import AudioSegment
from pydub.utils import make_chunks

class YouTubeAudioManager:
    """Manages YouTube video audio download and transcription."""
    
    TEMP_FOLDER = "temp"
    
    @classmethod
    def clear_temp(cls) -> None:
        """Clear temporary files and folders"""
        if os.path.exists(cls.TEMP_FOLDER):
            shutil.rmtree(cls.TEMP_FOLDER)
            os.makedirs(cls.TEMP_FOLDER)
        else:
            os.makedirs(cls.TEMP_FOLDER)

    @classmethod
    def get_youtube_audio(cls, url: str) -> AudioSegment:
        """
        Download and extract audio from YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            AudioSegment: Audio data from the video
        """
        print("Downloading Youtube Audio...")
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        filename = 'sound.mp4'

        if not os.path.exists(cls.TEMP_FOLDER):
            os.makedirs(cls.TEMP_FOLDER)
        
        audio_stream.download(output_path=cls.TEMP_FOLDER, filename=filename)
        audio = AudioSegment.from_file(f"{cls.TEMP_FOLDER}/{filename}")

        print("Download Complete.")
        return audio

    @classmethod
    def transcribe_audio(cls, audio: AudioSegment) -> str:
        """
        Transcribe audio using Google Speech Recognition.
        
        Args:
            audio: AudioSegment object containing the audio to transcribe
            
        Returns:
            str: Transcribed text
        """
        print("Transcribing Audio...")
        r = sr.Recognizer()

        # Break the audio into chunks of 1 minute each (60000 ms)
        chunk_length_ms = 60000
        chunks = make_chunks(audio, chunk_length_ms)
        transcript = ""

        for i, chunk in enumerate(chunks):
            print(f"Chunk: {i + 1}/{len(chunks)}")
            chunk_filename = f"{cls.TEMP_FOLDER}/chunk{i}.wav"
            chunk.export(chunk_filename, format="wav")
            
            with sr.AudioFile(chunk_filename) as source:
                audio_data = r.record(source)
                try:
                    transcript += r.recognize_google(audio_data) + " "
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")

        print("Transcription complete.")
        return transcript.strip()
