import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
import datetime
import json
import re
import requests
from time import strftime
from gtts import gTTS

language = 'vi'

def speak(text):
    print("Bot: {}".format(text))
    #truyen vao text de doc len
    tts = gTTS(text=text, lang=language, slow = False)
    tts.save("sound.mp3")
    playsound.playsound("sound.mp3", False)
    os.remove("sound.mp3")

def get_voice():
     r = sr.Recognizer()
     with sr.Microphone() as source:
        print("Me: ", end = '')
        audio = r.record(source, duration=5)
        try:
            text = r.recognize_google(audio, language="vi-VN")
            print(text)
            return text
        except:
            print("...")
            return 0

def stop():
    speak("Hẹn gặp lại bạn nhé!")


def get_text():
    for i in range(3):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ, bạn có thể nói lại không ?")
    time.sleep(5)
    stop()
    return 0

def run():
    speak("Xin chào bạn, hãy cho tôi biết tên của bạn")
    time.sleep(3)
    name = get_text()
    if name: 
        speak("Chào bạn {}".format(name))
        time.sleep(3)
        speak("Bạn muốn xem thời tiết về tỉnh thành phố nào?")
        time.sleep(3)
        while True:
            text = get_text()
            if not text: break
            elif "dừng" in text or "thôi" in text: 
                stop()
                time.sleep(3)
                break

run()