import os
import playsound
import speech_recognition as sr
import time
import sys
import ctypes
# import wikipedia
import datetime
import json
import re
# import webbrowser
# import smtplib
import requests
# import urllib
# import urllib.request as urllib2
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
from time import strftime
from gtts import gTTS
# from youtube_search import YoutubeSearch

language = 'vi'
# path = ChromeDriverManager().install()

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
        audio = r.listen(source, phrase_time_limit=5)
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
    time.sleep(10)
    stop()
    return 0

def talk(name):
    day_time = int(strftime('%H'))
    if day_time < 12:
        speak("Chào buổi sáng {}. Chúc bạn ngày mới tốt lành!".format(name))
    elif day_time < 18:
        speak("Chào buổi chiều {}!".format(name))
    else:
        speak("Chào buổi tối {}!".format(name))
    time.sleep(5)
    speak("Bạn có khỏe không ?")
    time.sleep(3)
    ans = get_voice()
    if ans:
        if "có" in ans:
            speak("Thật là tốt!")
        else:
            speak("Vậy à, bạn nên nghỉ ngơi đi!")

def run():
    speak("Xin chao ban")
    time.sleep(3)
    name = get_text()
    if name: 
        speak("chao ban {}".format(name))
        time.sleep(3)
        speak("ban can giup gi ko")
        time.sleep(3)
        while True:
            text = get_text()
            if not text: break
            elif  "trò chuyện" in text or "nói chuyện" in text:
                talk(name)
            elif "dừng" in text or "thôi" in text: 
                stop()
                break

run()