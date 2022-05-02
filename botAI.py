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
# import main
import unidecode
import webbrowser as wb
import datetime
import string_comparison_algorithm as sca
from bs4 import BeautifulSoup
import urllib.request
import re


language = 'vi'
def speak(text):
    print("Bot: {}".format(text))
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
    speak("Chúc bạn 1 ngày tốt lành!")

def get_text():
    for i in range(3):
        text = get_voice()
        if text:
            return text.lower()
        elif i < 2:
            speak("Bot không nghe rõ, bạn có thể nói lại không ?")
    time.sleep(3)
    stop()
    return 0


def getCity(y):
    if 'thời tiết' not in y and 'nắng' not in y and 'mưa' not in y  and 'nhiệt độ' not in y: return ''
    else: 
        listCity = []
        with open('cities.txt','r', encoding ='UTF-8') as file_object:
            ds = file_object.readlines()
        for city in ds:
            city = city.replace('\n','')
            sca.search(city,y,listCity)
        if len(listCity) > 0: return listCity[0]
        return ''

def remove_accent(text):
    return unidecode.unidecode(text)

def visitWebPage(location):
    city = remove_accent(location).replace(' ','-')
    url = f'https://thoitiet.vn/{city}'
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    return soup

def getCurrentWeather(location):  # xem thời tiết hiện tại
    soup = visitWebPage(location)
    status = soup.find('p',{'class': 'overview-caption-item-detail'}).text.strip()
    curTemp = soup.find('span',{'class': 'current-temperature'}).text.strip()
    curTemp += 'C'
    weatherDetail = soup.find('div',{'class': 'd-flex flex-wrap justify-content-between weather-detail mt-2'})
    ds = weatherDetail.find_all('div',{'class': 'd-flex ml-auto align-items-center'})
    tempRangeHtml = ds[0].find('span',{'class': 'text-white op-8 fw-bold'}).text.strip()
    tempRange = tempRangeHtml.replace('/','-')
    tempRange += 'C'
    humid = ds[1].find('span',{'class': 'text-white op-8 fw-bold'}).text.strip()
    visibility = ds[2].find('span',{'class': 'text-white op-8 fw-bold'}).text.strip()
    UV_index = ds[5].find('span',{'class': 'text-white op-8 fw-bold'}).text.strip()
    speak(f'{location} hiện tại {status}')
    time.sleep(2)
    speak(f'Nhiệt độ hiện tại {curTemp}')
    time.sleep(3)
    speak(f'nhiệt độ trong ngày từ {tempRange}')
    time.sleep(4)
    speak(f'Độ ẩm {humid}')
    time.sleep(3)
    speak(f'Tầm nhìn xa {visibility}')
    time.sleep(3)
    speak(f'chỉ số tia UV {UV_index}')
    time.sleep(3)

def getWeatherOtherDay(location,count,text): # xem thời tiết vào 1 ngày nào đó
    soup = visitWebPage(location)
    weatherDaily = soup.find_all('div', attrs = {'class': 'carousel-inner row w-100 mx-auto'})
    eachDay = weatherDaily[1].find_all('div', {'class':'location-wheather'})
    status = eachDay[count].find('p',{'class':'mb-0'}).text.strip()
    possibilityOfRain = eachDay[count].find('div',{'class':'precipitation'}).text.strip()
    tempMin = eachDay[count].find('p',{'title':'Thấp nhất'}).text.strip()
    tempMax = eachDay[count].find('p',{'title':'Cao nhất'}).text.strip()
    speak(text)
    time.sleep(3)
    speak(f'{status}')
    time.sleep(2)
    speak(f'khả năng mưa {possibilityOfRain}')
    time.sleep(3)
    speak(f'nhiệt độ từ {tempMin} đến {tempMax}')
    time.sleep(4)

def checkRainOrSunny(location,number,type): # kiểm tra trog n ngày tới có mưa/nắng không
    soup = visitWebPage(location)
    rain = []
    sunny = []
    number = int(number)
    weatherDaily = soup.find_all('div', attrs = {'class': 'carousel-inner row w-100 mx-auto'})
    eachDay = weatherDaily[1].find_all('div', {'class':'location-wheather'})
    
    for i in range(1,number+1):
        status = eachDay[i].find('p',{'class':'mb-0'}).text.strip().lower()
        date = eachDay[i].find('span').text.strip()
        date = date.replace('T', 'thứ ')
        if 'CN' in date: date = date.replace('CN', 'chủ nhật')
        if 'mưa' in status: rain.append(date)
        else : sunny.append(date)
    if (len(rain) == 0 and type == 'mưa'):
        speak(f'trong {number} ngày tới không có {type}')
        time.sleep(3)
    elif (len(sunny) == 0 and type == 'nắng'):
        speak(f'trong {number} ngày tới không có {type}')
        time.sleep(3)
    else:
        speak(f'những ngày {type} trong {number} ngày tới')
        time.sleep(3)
        if type == 'mưa':
            for k in rain:
                speak(k)
                time.sleep(2)
        else: 
            for k in sunny:
                speak(k)
                time.sleep(2)

def weatherOfTheFollowingDay(location,number):
    soup = visitWebPage(location)
    weatherDaily = soup.find_all('div', attrs = {'class': 'carousel-inner row w-100 mx-auto'})
    number = int(number)
    speak(f'thời tiết trong {number} ngày tới')
    time.sleep(3)
    eachDay = weatherDaily[1].find_all('div', {'class':'location-wheather'})
    for i in range(1,number+1):
        date = eachDay[i].find('span').text.strip()
        date = date.replace('T', 'thứ ')
        if 'CN' in date: date = date.replace('CN', 'chủ nhật')
        speak(date)
        time.sleep(3)
        status = eachDay[i].find('p',{'class':'mb-0'}).text.strip()
        speak(status)
        time.sleep(2)
        
def weatherHourly(location,number):
    soup = visitWebPage(location)
    number = int(number)
    weatherDaily = soup.find_all('div', attrs = {'class': 'carousel-inner row w-100 mx-auto'})
    hourly = weatherDaily[0]
    item = hourly.find_all('div',{'class':'location-wheather'})
    l = int(len(item)/2 + 1)
    for x in range(0,l):
        gethour = item[x].find('span').text.strip()
        hour = 0
        now = datetime.datetime.now().hour
        if(gethour == 'Hiện tại') : hour = now
        else: hour = int(gethour.replace(':00',''))
        if hour == 0: break
        if now + number > 23: 
            speak('Có phải bạn muốn xem thời tiết ngày mai?')
            time.sleep(3)
        else:
            if now + number == hour:
                status = item[number].find('p',{'class':'mb-0'}).text.strip()
                temp = item[number].find('div',{'class':'card-city-footer'})
                tempAvg = temp.find('p',{'title':'Nhiệt độ trung bình'}).text.strip()
                speak(f'{location} trong {number} giờ tới')
                time.sleep(3)
                speak(f'{status}')
                time.sleep(3)
                speak(f'Nhiệt độ trung bình: {tempAvg}')
                time.sleep(3)

def checkRainSunnyToday(location,number,mess):
    soup = visitWebPage(location)
    number = int(number)
    weatherDaily = soup.find_all('div', attrs = {'class': 'carousel-inner row w-100 mx-auto'})
    hourly = weatherDaily[0]
    item = hourly.find_all('div',{'class':'location-wheather'})
    l = int(len(item)/2 + 1)
    for x in range(0,l):
        gethour = item[x].find('span').text.strip()
        hour = 0
        now = datetime.datetime.now().hour
        if(gethour == 'Hiện tại') : hour = now
        else: hour = int(gethour.replace(':00',''))
        if hour == 0: break
        status = item[x].find('p',{'class':'mb-0'}).text.strip()
        checkRain = False
        checkSunny = False
        if mess == 'mưa':
            if mess in status:
                speak(f'trong {number} giờ tới có mưa')
                time.sleep(3)
                checkRain = True
                break
        else :
            if 'mưa' not in status:
                speak(f'trong {number} giờ tới có nắng')
                time.sleep(3)
                checkSunny = True
                break
    if checkRain == False and mess == 'mưa': 
        speak(f'trong {number} giờ tới không có mưa')
        time.sleep(3)
    elif checkSunny == False and mess == 'nắng':
        speak(f'trong {number} giờ tới có mưa')
        time.sleep(3)

def run():
    while True:
        speak('Tôi có thể giúp gì cho bạn')
        time.sleep(2)
        text = get_text()
        city = getCity(text)
        if not text: break
        elif "dừng" in text or "thôi" in text or "kết thúc" in text or "thoát" in text: 
            stop()
            time.sleep(3)
            break
        elif(city == '') : 
            speak('bạn hãy đưa ra câu hỏi về thời tiết')
            time.sleep(2)
        else : 
            checkNumber = re.findall("[0-9]", text)
            if 'có mưa' in text and 'ngày mai' in text :
                checkRainOrSunny(city,1,'mưa')
            elif 'có mưa' in text and 'ngày kia' in text :
                checkRainOrSunny(city,2,'mưa')
            elif 'có nắng' in text and 'ngày mai' in text :
                checkRainOrSunny(city,1,'nắng')
            elif 'có nắng' in text and 'ngày kia' in text :
                checkRainOrSunny(city,2,'nắng')
            elif 'có mưa' in text and len(checkNumber) > 0 and 'ngày tới' in text:
                checkRainOrSunny(city,checkNumber[0],'mưa')
            elif 'có nắng' in text and len(checkNumber) > 0 and 'ngày tới' in text:
                checkRainOrSunny(city,checkNumber[0],'nắng')
            elif 'ngày tới' in text and len(checkNumber) > 0 :
                weatherOfTheFollowingDay(city,checkNumber[0])
            elif 'ngày mai' in text or 'ngày hôm sau' in text :
                getWeatherOtherDay(city,1,text)
            elif 'ngày kia' in text :
                getWeatherOtherDay(city,2,text)
            elif 'giờ tới' in text and 'có mưa' in text:
                checkRainSunnyToday(city,checkNumber[0],'mưa')
            elif 'giờ tới' in text and 'có nắng' in text:
                checkRainSunnyToday(city,checkNumber[0],'nắng')
            elif 'giờ tới' in text or 'giờ sau' in text:
                weatherHourly(city,checkNumber[0])
            else: getCurrentWeather(city)
        
# run()
