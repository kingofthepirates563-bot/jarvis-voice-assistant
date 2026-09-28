# Jarvis - Voice Assistant

A Python voice assistant that listens for the wake word "Jarvis", understands speech, answers questions using Google Gemini AI, speaks back, and performs laptop tasks.

## Features
- Wake word detection ("Jarvis")
- Speech-to-text (SpeechRecognition)
- AI answers (Google Gemini API)
- Text-to-speech replies (pyttsx3)
- Voice commands: open YouTube, open Google, open Notepad, tell time, search Google

## Tech Used
Python, SpeechRecognition, pyttsx3, Google Gemini API, python-dotenv

## How to Run
1. Install Python 3.11
2. Install libraries: python -m pip install -r requirements.txt
3. Get a free API key from https://aistudio.google.com/
4. Copy .env.example to .env and paste your key
5. Run: python jarvis.py

## Challenges I Solved
- pyaudio failed to install on Python 3.14, fixed by switching to Python 3.11
- Fixed the voice engine going silent in a loop by re-creating it on each reply
- Added retry logic for when the Gemini API is busy
- Added a wake word so it ignores background noise

## Demo
(Demo video link coming soon)