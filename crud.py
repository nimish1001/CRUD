#importing libraries
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import requests
import pandas as pd
import cx_Oracle   
import socket
import datetime
import bs4

#Main Menu
root = Tk()
root.title("SMS")
root.geometry("500x500+500+200")

def f1():
        root.withdraw()
        addStu.deiconify()
def f2():
        stdData.delete(1.0, END)
        root.withdraw()
        con=None
        try:
            con = cx_Oracle.connect('system/abc123')
            cursor = con.cursor()
            sql = "select roll, name, marks from students"
            cursor.execute(sql)
            data = cursor.fetchall()
            result = ''
            for d in data:
                result+="Roll Number: "+str(d[0])+" Name: "+str(d[1])+" Marks: "+str(d[2])+"\n"    
            stdData.insert(INSERT, result)
        except cx_Oracle.DatabaseError:
            messagebox.showerror('Error!', "Records not found !")
        finally:
            if con is not None:
                con.close()        

        viewStu.deiconify()
def f3():
        root.withdraw()
        updStu.deiconify() 
def f4():
        root.withdraw()
        delStu.deiconify()               


btnAdd = Button(root, text='Add', font=('Times New Roman', 16, 'bold'), width=10, command=f1)
btnView = Button(root, text='View', font=('Times New Roman', 16, 'bold'), width=10, command=f2)
btnUpdate = Button(root, text='Update', font=('Times New Roman', 16, 'bold'), width=10, command=f3)
btnDelete = Button(root, text='Delete', font=('Times New Roman', 16, 'bold'), width=10, command=f4)


btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)

#Quote of the day:

try:
	socket.create_connection(("www.google.com", 80))
	res= requests.get('https://www.brainyquote.com/quotes_of_the_day.html')
	soup = bs4.BeautifulSoup(res.text, 'lxml')
	quote = soup.find('img', {"class":"p-qotd"})	
	msg1 = quote['alt']
	lblQuote = Label(root, text='Quote of the day:\n'+msg1, font=('Comic Sans MS', 16, 'italic'))
	res=requests.get("https://ipinfo.io")
	dataip = res.json()
	city = dataip['city']
	a1='https://api.openweathermap.org/data/2.5/weather?units=metric'
	a2='&q='+city
	a3='&appid=c6e315d09197cec231495138183954bd'
	api_address = a1+a2+a3
	res = requests.get(api_address)	
	#print(res)	
	weather_data = res.json()
	#print(weather_data)
	#ain = weather_data['main'] #Can also be written as: temp = data['main']['temp']
	#temp = main['temp']
	res1 = requests.get(api_address)
	dataw = res1.json()
	main = dataw['main']
	temp = main['temp']
	msg2 = 'City: '+ city + '\tTemperature: '+str(temp)
	date = datetime.datetime.now()
	msg3 = "Date: " + date.strftime("%x")
	lblDate = Label(root, text=msg2, font=('Comic Sans MS', 13))
	
	lblTempandCity = Label(root, text=msg3, font=('Comic Sans MS', 13))
	lblTempandCity.pack(pady=20)
	lblDate.pack(pady=10)
	lblQuote.pack(pady=10)

except OSError as e:
    lblError = Label(root, text='Can\'t connect to internet !!', font=('Times New Roman', 16, 'bold'))
    lblError.pack(pady=15)

#--------------------------------------------------------------------------------------------------------------
#Add Student

addStu = Toplevel(root)
addStu.title("Add Student Details")
addStu.geometry("500x500+500+200")

def f6():
        addStu.withdraw()
        root.deiconify()
def f5():
        con = None
        if len(enRoll.get()) == 0:
            messagebox.showerror('Error !', "Roll Number can\'t be empty !")
            enRoll.focus()
            return  
        if not enRoll.get().isdigit():
            messagebox.showerror('Error !', "Roll number must be integer !")
            enRoll.focus()
            return
        if len(enName.get()) <2:
            messagebox.showerror('Error !', "Name must contain atleast two characters !")
            enName.focus()
            return
        if not enName.get().isalpha():
            messagebox.showerror('Error !', "Invalid Name !")
            enName.focus()
            return
        if  not enMarks.get().isdigit():
            messagebox.showerror('Error !', "Marks must be numeric value between 0 to 100 !")
            enMarks.focus()
            return  
        if int(enMarks.get()) <0 or int(enMarks.get())>100:
            messagebox.showerror('Error !', "Marks must lie within 0 to 100 !")
            enMarks.focus()
            return                       
        try:
            con = cx_Oracle.connect('system/abc123')
            rno = int(enRoll.get())
            name = enName.get()
            marks = int(enMarks.get())
            cursor = con.cursor()
            sql = "insert into students values('%d', '%s', '%d')"
            args = (rno, name, marks)
            cursor.execute(sql%args)
            con.commit()
            messagebox.showinfo('Success !', 'Recored inserted successfully')
            enRoll.delete(0, END)
            enName.delete(0, END)
            enMarks.delete(0, END)
            enRoll.focus()
        except cx_Oracle.DatabaseError as e:
            print(e)
            con.rollback()
            msg = "Record could not be inserted !"
            messagebox.showerror('Error !', msg)
        finally:
            if con is not None:
                con.close()        

lblRoll = Label(addStu, text = "Enter Roll Number",font=('Times New Roman', 16, 'bold'))
lblName = Label(addStu, text = "Enter Name",font=('Times New Roman', 16, 'bold'))
lblMarks = Label(addStu, text = "Enter Marks",font=('Times New Roman', 16, 'bold'))

enRoll = Entry(addStu, bd=5, font=('Times New Roman', 16))
enName = Entry(addStu, bd=5, font=('Times New Roman', 16))
enMarks = Entry(addStu, bd=5, font=('Times New Roman', 16))

btnSave = Button(addStu, text='Save', font=('Times New Roman', 16, 'bold'), width=10, command=f5)
btnaBack1 = Button(addStu, text='Back', font=('Times New Roman', 16, 'bold'), width=10, command=f6)

lblRoll.pack(pady=10)
enRoll.pack(pady=10)

lblName.pack(pady=10)
enName.pack(pady=10)

lblMarks.pack(pady=10)
enMarks.pack(pady=10)

btnSave.pack(pady=10)
btnaBack1.pack(pady=10)
addStu.withdraw()