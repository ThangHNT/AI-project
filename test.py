# import geocoder
import requests
import json
import pymongo
import webbrowser as wb
import re
from bs4 import BeautifulSoup
import urllib.request
import datetime

# g = geocoder.ip('me')
# print(g.state)
# print(g.json)

# x = requests.get('https://api.openweathermap.org/data/2.5/weather?q=thành phố nam định&appid=a7c7bb6f3e9b61aee6966b09d3e30214')
# k = json.loads(x.text)
# print(k['weather'][0]['main'] + k['weather'][0]['description'])
# x = requests.get('https://provinces.open-api.vn/api/?depth=3')
# k = json.loads(x.text)
# i = 0
# print(type(k[i]['name']))

# with open('cities.txt', 'a') as file_object:
#     for i in range(0,63):
#         file_object.write(k[i]['name'])
    

# ---------------------------------------------------------------------------------------

# from tkinter import *
# win = Tk()
# win.title('Weather')
# # win.configure(width=400, height=200)
# screenWidth = win.winfo_screenwidth()
# screenHeight = win.winfo_screenheight()
# consoleWidth = 500
# consoleHeight = 500
# win.geometry(f'{consoleWidth}x{consoleHeight}+%d+%d' %(screenWidth/2 - consoleWidth/2, screenHeight/2 - consoleHeight/2 - 80))
# lb1 = Label(win, text = 'hello')
# lb1.pack()
# def setText():
#     lb1.config(text = "xin chao")
#     lb1.pack()
# win.after(1000,setText)

# def display():
#     print(textInput.get())
# def show(e):
#     print('hello')
    
# textInput = Entry(win, font='Times 20 bold')
# textInput.pack()
# btn = Button(win,text='tim kiem', font='Times 10 bold', command=display)
# btn.pack()
# win.resizable(width=False, height=False)
# frame = Frame(win)
# frame.pack()
# def xuat():
#     print('xin chao')
# button = Button(frame, text='click me', command = xuat)
# button.pack()

# Label(win, text='xin chao').grid(row=0,column=0)
# Label(win, text='hello').grid(row=0,column=1)

# win.mainloop()

# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["AI"]
# mycollection = mydb["cities"]
# for city in mycollection.find():
#     cityName = city["name"].lower()
#     with open('cities.txt', 'a',encoding='UTF-8') as file_object:
#         file_object.write(f'{cityName}\n')


# url = 'https://google.com/search?q=thoi tiet ha noi'
# wb.get().open(url)


# x = input('xau can tim: ')
# y = input('xau mau: ')

def preKMP(x):
    kmpNext = [0]*(len(x) +1)
    i = 0
    j = -1
    kmpNext[0] = -1
    while(i < len(x) -1):
        while j > -1 and x[i] != x[j]:
            j = kmpNext[j]
        i +=1 
        j += 1
        if x[i] == x[j]:
            kmpNext[i] = kmpNext[j]
        else: kmpNext[i] = j
    return kmpNext
    
def search(x,y,listCity):
    kmpNext = preKMP(x)
    i = 0
    m = 0
    while m <= len(y) - len(x):
        if x[i] == y[m+i]:
            i += 1
            if i == len(x):
                listCity.append(x)
                m += i - kmpNext[i]
                i = kmpNext[i]
        else:
            m += i - kmpNext[i]
            i = 0
    return 0



# y = input('xau mau: ')
def getCity(y):
    listCity = []
    with open('cities.txt','r', encoding ='UTF-8') as file_object:
        ds = file_object.readlines()
    for city in ds:
        city = city.replace('\n','')
        search(city,y,listCity)
    if len(listCity) > 0: return listCity[0]
    return ''
# getCity(y)


url =  'https://thoitiet.vn/ha-noi' 
page = urllib.request.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
weatherDaily = soup.find_all('div', attrs = {'class': 'carousel-inner row w-100 mx-auto'})
# eachDay = weatherDaily[1].find_all('div', {'class':'location-wheather'})
# amountOfRain = eachDay[1].find('div',{'class':'precipitation'}).text.strip()
# status = eachDay[1].find('p',{'class':'mb-0'}).text.strip()
# tempMin = eachDay[1].find('p',{'title':'Thấp nhất'}).text.strip()
# tempMax = eachDay[1].find('p',{'title':'Cao nhất'}).text.strip()
# date = eachDay[1].find('span').text.strip()

t = int(input("thoi tiet sau: "))

hourly = weatherDaily[0]
k = hourly.find_all('div',{'class':'location-wheather'})
status = k[0].find('p',{'class':'mb-0'})
gethour = k[0].find('span').text.strip()
temp = k[0].find('div',{'class':'card-city-footer'})
tempAvg = temp.find('p',{'title':'Nhiệt độ trung bình'}).text.strip()

l = int(len(k)/2 + 1)

for x in range(0,l):
    gethour = k[x].find('span').text.strip()
    hour = 0
    now = datetime.datetime.now().hour
    if(gethour == 'Hiện tại') : hour = now
    else: hour = int(gethour.replace(':00',''))
    if hour == 0: break
    print(hour)
    if now + t > 23: print('ban muon xem thoi tiet ngay mai')
    else:
        if now + t == hour:
            status = k[t].find('p',{'class':'mb-0'}).text.strip()
            temp = k[t].find('div',{'class':'card-city-footer'})
            tempAvg = temp.find('p',{'title':'Nhiệt độ trung bình'}).text.strip()
            # print(f'{status} {tempAvg}')
    

# print(tempAvg)
time = datetime.datetime.now()




# curTemp = soup.find('span',{'class': 'current-temperature'}).text.strip()
# print(curTemp)
# status = soup.find('p',{'class': 'overview-caption-item-detail'}).text.strip()
# print(status)

# weatherDetail = soup.find('div',{'class': 'd-flex flex-wrap justify-content-between weather-detail mt-2'})
# ds = weatherDetail.find_all('div',{'class': 'd-flex ml-auto align-items-center'})
# weatherDetailItem = ds[2].find('span',{'class': 'text-white op-8 fw-bold'}).text.strip()

# txt = 'thời tiết hà nội trong 7 ngày tới'
# x = re.findall("[0-9]", txt)
# print(x)


