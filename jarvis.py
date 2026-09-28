import speech_recognition as sr
import pyttsx3
from google import genai
from dotenv import load_dotenv
import os
import webbrowser
import datetime
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

recognizer = sr.Recognizer()
recognizer.pause_threshold = 1.0

WAKE_WORDS = ["hey jarvis", "jarvis", "jar vis", "jarves"]

def speak(text):
    print("Jarvis:", text)
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()
    time.sleep(0.5)

def ask_gemini(question):
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents="Answer in 2 or 3 short sentences: " + question
            )
            return response.text.replace("*", "")
        except Exception as e:
            print("Gemini error:", e)
            time.sleep(2)
    return "Sorry, my brain is busy right now. Please try again in a moment."

def listen():
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""
    try:
        text = recognizer.recognize_google(audio)
        print("Heard:", text)
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Internet problem. Check your connection.")
        return ""

def handle_command(command):
    if "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
        return True

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
        return True

    if "what time" in command or "the time" in command or "current time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak("The time is " + now)
        return True

    if "search for" in command:
        query = command.replace("search for", "").strip()
        speak("Searching for " + query)
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return True

    if "open notepad" in command:
        speak("Opening Notepad")
        os.system("notepad")
        return True

    return False

def find_wake_word(text):
    for word in WAKE_WORDS:
        if word in text:
            return word
    return None

print("Adjusting to room noise, stay quiet for 2 seconds...")
with sr.Microphone() as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)
recognizer.energy_threshold = max(recognizer.energy_threshold, 300)
recognizer.dynamic_energy_threshold = False

speak("Jarvis is online. Say Jarvis when you need me.")

while True:
    heard = listen()

    if heard == "":
        continue

    wake = find_wake_word(heard)
    if wake is None:
        continue   # not meant for Jarvis, ignore

    command = heard.split(wake, 1)[1].strip()

    if command == "":
        speak("Yes?")
        command = listen()
        if command == "":
            continue

    if "stop" in command or "exit" in command or "goodbye" in command or "quit" in command:
        speak("Goodbye!")
        break

    if not handle_command(command):
        reply = ask_gemini(command)
        speak(reply)