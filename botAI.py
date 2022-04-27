import os
import playsound
import speech_recognition as sr
import time
import sys
import json
import requests
from time import strftime
from gtts import gTTS
import threading
from tkinter import *
import main

def showResults(data):
    for widgets in main.frame4.winfo_children():
        widgets.destroy()
    temp = data['main']['temp']
    temp -= 273.15
    humid = data['main']['humidity']
    city = data['name']
    visibility = data['visibility']
    windSpeed = data['wind']['speed']
    lb1 = Label(main.frame4,text=f'Thành phố {city} ', font="Time 12 bold")
    lb3 = Label(main.frame4,text=f'Nhiệt độ {"%.2f"%temp} độ C', font="Time 12")
    lb4 = Label(main.frame4,text=f'Độ ẩm {humid}%', font="Time 12")
    lb5 = Label(main.frame4,text=f'Tầm nhìn xa {visibility}m/s', font="Time 12")
    lb6 = Label(main.frame4,text=f'Tốc độ gió {windSpeed}m/s', font="Time 12")
    lb1.pack()
    lb3.pack()
    lb4.pack()
    lb5.pack()
    lb6.pack()

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
    time.sleep(2)
    name = get_text()
    if name: 
        speak("Chào bạn {}".format(name))
        time.sleep(1)
        speak("Bạn muốn xem thời tiết về tỉnh thành phố nào?")
        time.sleep(3)
        while True:
            text = get_text()
            if not text: break
            elif "dừng" in text or "thôi" in text: 
                stop()
                time.sleep(3)
                break
            else :
                x = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={text}&appid=a7c7bb6f3e9b61aee6966b09d3e30214')
                data = json.loads(x.text)
                if(data['cod'] == '404'): speak('Bạn hãy nói đúng tên tỉnh thành phố')
                else :
                    showResults(data)
                    time.sleep(3)
                    temp = data['main']['temp']
                    temp -= 273.15
                    humid = data['main']['humidity']
                    visibility = data['visibility']
                    windSpeed = data['wind']['speed']
                    speak(f"{text}")
                    time.sleep(3)
                    speak(f'Nhiệt độ {"%.2f"%temp} độ C')
                    time.sleep(3)
                    speak(f'Độ ẩm {humid}%')
                    time.sleep(3)
                    speak(f'Tầm nhìn xa {visibility}m/s')
                    time.sleep(3)
                    speak(f'Tốc độ gió {windSpeed}m/s')
                    time.sleep(3)
                    stop()
                    break
