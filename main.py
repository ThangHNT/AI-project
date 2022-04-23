import requests
import json
import pymongo
import time
from win10toast import ToastNotifier
from geopy.geocoders import Nominatim
import geocoder
from tkinter import *
import threading
from PIL import ImageTk, Image

win = Tk()
win.title('Weather')

g = geocoder.ip('me')
myLocation = g.city     # lấy tên thành phố

def theWeatherNow():
    data = resultOfSearch(myLocation)
    text = f'main: {data["main"]} \n'
    # print(data['main']["humidity"])
    # while True:
    #     t = ToastNotifier()
    #     t.show_toast(f"Weather of {myLocation} today:",text,duration = 5)
    #     # print('ok')
    #     break
def show_weather_here():
    show_weather = threading.Thread(target = theWeatherNow)
    show_weather.start()

def resultOfSearch(location):
    x = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid=a7c7bb6f3e9b61aee6966b09d3e30214')
    data = json.loads(x.text)
    return data


def weatherOfCity(city):
    data = resultOfSearch(city)
    temp = data['main']['temp']
    humid = data['main']['humidity']
    for widgets in frame4.winfo_children():
        widgets.destroy()
    lb1 = Label(frame4,text=f'Thành phố {city} ', font="Time 12 bold")
    lb2 = Label(frame4,text=f'Nhiệt độ {temp} độ K', font="Time 12")
    lb3 = Label(frame4,text=f'Độ ẩm {humid}%', font="Time 12")
    lb1.pack()
    lb2.pack()
    lb3.pack()
    
def closeSearchFunction():
    frame3.pack_forget()
    frame4.pack_forget()

def searchFunction():
    textInput = Entry(frame3, font='Times 15')
    textInput.grid(row =4, column =0,pady= 20)
    def thirdThread():
        k = threading.Thread(target = weatherOfCity(textInput.get()))
        k.start()
    btn = Button(frame3, text="search" ,font='Times 12', command=thirdThread)
    btn.grid(row =4, column = 1)
    btn2 = Button(frame3, text="Cancel", font='Times 12', command=closeSearchFunction)
    btn2.grid(row =4, column = 3)
    frame3.pack()
    frame4.pack()



screenWidth = win.winfo_screenwidth()
screenHeight = win.winfo_screenheight()
consoleWidth = 500
consoleHeight = 500
win.geometry(f'{consoleWidth}x{consoleHeight}+%d+%d' %(screenWidth/2 - consoleWidth/2, screenHeight/2 - consoleHeight/2 - 80))
frame1 = Frame(win)
frame2 = Frame(win)
frame3 = Frame(win)
frame4 = Frame(win)
frame5 = Frame(win)
frame5.place(anchor='center', relx=0.5, rely=0.5)
lb1 = Label(frame1, text="Chọn chức năng", font="Times 14 bold")
lb2 = Label(frame2, text="Xem thời tiết chỗ bạn", font="Times 14")
lb3 = Label(frame2, text="Xem thời tiết tỉnh thành khác", font="Times 14")
lb4 = Label(frame2, text="Tỉnh thành phố có thời tiết đẹp", font="Times 14")
btn1 = Button(frame2, text="Chọn", command=show_weather_here)
btn2 = Button(frame2, text="Nhập", command=searchFunction)
btn3 = Button(frame2, text="Chọn")
lb1.pack()
lb2.grid(row=0, column=0,sticky=W)
lb3.grid(row=1, column=0,sticky=W)
lb4.grid(row=2, column=0,sticky=W)
btn1.grid(row=0, column=1)
btn2.grid(row=1, column=1)
btn3.grid(row=2, column=1)
frame5.pack()
frame1.pack()
frame2.pack()
frame3.pack()
frame4.pack()

# thêm hình ảnh
imgae = Image.open('images/weather.jpg')
resizeImg = imgae.resize((300,120))
img = ImageTk.PhotoImage(resizeImg)
lb5 = Label(frame5,image=img)
lb5.pack()

# -------------------------------------------------------------------------------------------------------------------


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["AI"]
# mycollection = mydb["cities"]





show_weather_here()
win.mainloop()

