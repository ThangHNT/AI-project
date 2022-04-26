# import geocoder
import requests
import json
# g = geocoder.ip('me')
# print(g.state)
# print(g.json)

# x = requests.get('https://api.openweathermap.org/data/2.5/weather?q=thành phố nam định&appid=a7c7bb6f3e9b61aee6966b09d3e30214')
# k = json.loads(x.text)
# print(k['weather'][0]['main'] + k['weather'][0]['description'])
x = requests.get('https://provinces.open-api.vn/api/?depth=3')
k = json.loads(x.text)
i = 0
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
