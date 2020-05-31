# importing libraries
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
import sqlite3
from pandas import DataFrame
from functools import partial
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


con = sqlite3.connect('cruddb.sqlite')
cursor = con.cursor()

# Make some fresh tables using executescript()
cursor.executescript('''

CREATE TABLE IF NOT EXISTS students (
    roll INTEGER NOT NULL PRIMARY KEY,
    name TEXT,
    marks INTEGER
);
''')
# LogIn
# LogIn
root = Tk()
root.title("Log-In")
root.geometry("500x500+500+200")


def f0():
    if enlogin.get() == "KJSCE" and enpassword.get() == "password":
        root.withdraw()
        mainMenu.deiconify()
        return
    else:
        messagebox.showerror('Error !', "Invalid Credentials !")
        enlogin.focus()


btnLogin = Button(root, text='Log-In',
                  font=('Times New Roman', 16, 'bold'), width=10, command=f0)
btnLogin.pack(pady=10)

enlogin = Entry(root, bd=5, font=('Times New Roman', 16))
enpassword = Entry(root, bd=5, font=('Times New Roman', 16))

lbllogin = Label(root, text="Id", font=('Times New Roman', 16, 'bold'))
lblpassword = Label(root, text="Password", font=(
    'Times New Roman', 16, 'bold'))

lbllogin.pack(pady=10)
enlogin.pack(pady=10)

lblpassword.pack(pady=10)
enpassword.pack(pady=10)

# Main Menu
mainMenu = Toplevel(root)
mainMenu.title("SMS")
mainMenu.geometry("500x500+500+200")


def f1():
    mainMenu.withdraw()
    addStu.deiconify()


def f2():
    stdData.delete(1.0, END)
    mainMenu.withdraw()
    # con=None
    try:
        con = sqlite3.connect('cruddb.sqlite')
        cursor = con.cursor()
        sql = "select roll, name, marks from students"
        cursor.execute(sql)
        data = cursor.fetchall()
        result = ''
        for d in data:
            result += "Roll Number: " + \
                str(d[0])+" Name: "+str(d[1])+" Marks: "+str(d[2])+"\n"
        stdData.insert(INSERT, result)
    except sqlite3.Error:
        messagebox.showerror('Error!', "Records not found !")
    finally:
        if con is not None:
            con.close()

    viewStu.deiconify()


def f3():
    mainMenu.withdraw()
    updStu.deiconify()


def f4():
    mainMenu.withdraw()
    delStu.deiconify()


btnAdd = Button(mainMenu, text='Add', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f1)
btnView = Button(mainMenu, text='View', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f2)
btnUpdate = Button(mainMenu, text='Update', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f3)
btnDelete = Button(mainMenu, text='Delete', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f4)


btnAdd.pack(pady=10)
btnView.pack(pady=10)
btnUpdate.pack(pady=10)
btnDelete.pack(pady=10)

# Quote of the day:

try:
    socket.create_connection(("www.google.com", 80))
    res = requests.get('https://www.brainyquote.com/quotes_of_the_day.html')
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    quote = soup.find('img', {"class": "p-qotd"})
    msg1 = quote['alt']
    lblQuote = Label(mainMenu, text='Quote of the day:\n' +
                     msg1, font=('Comic Sans MS', 16, 'italic'))
    res = requests.get("https://ipinfo.io")
    dataip = res.json()
    city = dataip['city']
    a1 = 'https://api.openweathermap.org/data/2.5/weather?units=metric'
    a2 = '&q='+city
    a3 = '&appid=c6e315d09197cec231495138183954bd'
    api_address = a1+a2+a3
    res = requests.get(api_address)
    # print(res)
    weather_data = res.json()
    # print(weather_data)
    # ain = weather_data['main'] #Can also be written as: temp = data['main']['temp']
    #temp = main['temp']
    res1 = requests.get(api_address)
    dataw = res1.json()
    main = dataw['main']
    temp = main['temp']
    msg2 = 'City: ' + city + '\tTemperature: '+str(temp)
    date = datetime.datetime.now()
    msg3 = "Date: " + date.strftime("%x")
    lblDate = Label(mainMenu, text=msg2, font=('Comic Sans MS', 13))

    lblTempandCity = Label(mainMenu, text=msg3, font=('Comic Sans MS', 13))
    lblTempandCity.pack(pady=20)
    lblDate.pack(pady=10)
    lblQuote.pack(pady=10)

except OSError as e:
    lblError = Label(mainMenu, text='Can\'t connect to internet !!',
                     font=('Times New Roman', 16, 'bold'))
    lblError.pack(pady=15)

# --------------------------------------------------------------------------------------------------------------
# Add Student

addStu = Toplevel(mainMenu)
addStu.title("Add Student Details")
addStu.geometry("500x500+500+200")


def f6():
    addStu.withdraw()
    mainMenu.deiconify()


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
    if len(enName.get()) < 2:
        messagebox.showerror(
            'Error !', "Name must contain atleast two characters !")
        enName.focus()
        return
    if not enName.get().isalpha():
        messagebox.showerror('Error !', "Invalid Name !")
        enName.focus()
        return
    if not enMarks.get().isdigit():
        messagebox.showerror(
            'Error !', "Marks must be numeric value between 0 to 100 !")
        enMarks.focus()
        return
    if int(enMarks.get()) < 0 or int(enMarks.get()) > 100:
        messagebox.showerror('Error !', "Marks must lie within 0 to 100 !")
        enMarks.focus()
        return
    try:
        con = sqlite3.connect('cruddb.sqlite')
        rno = int(enRoll.get())
        name = enName.get()
        marks = int(enMarks.get())
        cursor = con.cursor()
        sql = "insert into students values(?, ?, ?)"
        args = (rno, name, marks)
        cursor.execute(sql, args)
        con.commit()
        messagebox.showinfo('Success !', 'Recored inserted successfully')
        enRoll.delete(0, END)
        enName.delete(0, END)
        enMarks.delete(0, END)
        enRoll.focus()
    except sqlite3.Error as e:
        print(e)
        con.rollback()
        msg = "Record could not be inserted !"
        messagebox.showerror('Error !', msg)
    finally:
        if con is not None:
            con.close()


lblRoll = Label(addStu, text="Enter Roll Number",
                font=('Times New Roman', 16, 'bold'))
lblName = Label(addStu, text="Enter Name",
                font=('Times New Roman', 16, 'bold'))
lblMarks = Label(addStu, text="Enter Marks",
                 font=('Times New Roman', 16, 'bold'))

enRoll = Entry(addStu, bd=5, font=('Times New Roman', 16))
enName = Entry(addStu, bd=5, font=('Times New Roman', 16))
enMarks = Entry(addStu, bd=5, font=('Times New Roman', 16))

btnSave = Button(addStu, text='Save', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f5)
btnaBack1 = Button(addStu, text='Back', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f6)

lblRoll.pack(pady=10)
enRoll.pack(pady=10)

lblName.pack(pady=10)
enName.pack(pady=10)

lblMarks.pack(pady=10)
enMarks.pack(pady=10)

btnSave.pack(pady=10)
btnaBack1.pack(pady=10)
addStu.withdraw()

# --------------------------------------------------------------------------------------------------------------
# View Data

viewStu = Toplevel(mainMenu)
viewStu.title("View Student Details")
viewStu.geometry("500x500+500+200")


def f7():
    viewStu.withdraw()
    mainMenu.deiconify()


def f12():
    con = None
    try:
        con = sqlite3.connect('cruddb.sqlite')
        cursor = con.cursor()
        sql = "select roll, name, marks from students"
        cursor.execute(sql)
        data = cursor.fetchall()
        import operator
        sortedlist = sorted(data, key=operator.itemgetter(2), reverse=True)
        dname = []
        droll = []
        for i in sortedlist:
            dname.append(i[1])
            droll.append(i[2])
        dname = dname[:5]
        droll = droll[:5]
        x = np.arange(len(dname))
        data = {'Name': x,
         'Marks': droll
        }
        df = DataFrame(data1,columns=['Name','Marks'])
        figure = plt.Figure(figsize=(6,5), dpi=100)
        ax = figure.add_subplot(111)
        chart_type = FigureCanvasTkAgg(figure, root)
        chart_type.get_tk_widget().pack()
        df = df[['Name','Marks']].groupby('Name').sum()
        df.plot(kind='Chart Type such as bar', legend=True, ax=ax)
        ax.set_title('Performance')
    except sqlite3.Error:
        messagebox.showerror('Error!', "Records not found !")
    finally:
        if con is not None:
            con.close()


btnBack2 = Button(viewStu, text='Back', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f7)
btnGraph = Button(viewStu, text='Graph', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f12)
stdData = scrolledtext.ScrolledText(viewStu, width=50, height=20)

stdData.pack(pady=10)
btnBack2.pack(pady=10)
btnGraph.pack(pady=10)
viewStu.withdraw()

# --------------------------------------------------------------------------------------------------------------
# Update Data
updStu = Toplevel(mainMenu)
updStu.title("Update Student Details")
updStu.geometry("500x500+500+200")


def f8():
    updStu.withdraw()
    mainMenu.deiconify()


def f10():
    con = None
    if len(enuRoll.get()) == 0:
        messagebox.showerror('Error !', "Roll Number can\'t be empty !")
        enuRoll.focus()
        return
    if not enuRoll.get().isdigit():
        messagebox.showerror('Error !', "Roll number must be integer !")
        enuRoll.focus()
        return
    if len(enuName.get()) < 2:
        messagebox.showerror(
            'Error !', "Name must contain atleast two characters !")
        enuName.focus()
        return
    if not enuName.get().isalpha():
        messagebox.showerror('Error !', "Invalid Name !")
        enuName.focus()
        return
    if not enuMarks.get().isdigit():
        messagebox.showerror(
            'Error !', "Marks must be numeric value between 0 to 100 !")
        enuMarks.focus()
        return
    if int(enuMarks.get()) < 0 or int(enuMarks.get()) > 100:
        messagebox.showerror('Error !', "Marks must lie within 0 to 100 !")
        enuMarks.focus()
        return
    try:
        con = sqlite3.connect('cruddb.sqlite')
        rno = int(enuRoll.get())
        name = enuName.get()
        marks = int(enuMarks.get())
        cursor = con.cursor()
        sql = "select roll from students"
        cursor.execute(sql)
        data1 = cursor.fetchall()
        present = False
        for d in data1:
            if d[0] == rno:
                present = True
                break
        if not present:
            messagebox.showerror("Error!", "Roll Number not found !")
            enuRoll.focus()
            return
        else:
            sql = "update students set name= ?, marks=? where roll=?"
            args = (name, marks, rno)
            cursor.execute(sql, args)
            con.commit()
            messagebox.showinfo('Success !', 'Recored updated successfully')
            enuRoll.delete(0, END)
            enuName.delete(0, END)
            enuMarks.delete(0, END)
            enuRoll.focus()
    except sql3lite.Error:
        con.rollback()
        msg = "Record could not be updated !"
        messagebox.showerror('Error !', msg)
    finally:
        if con is not None:
            con.close()


lbluRoll = Label(updStu, text="Enter Roll Number",
                 font=('Times New Roman', 16, 'bold'))
lbluName = Label(updStu, text="Enter Name",
                 font=('Times New Roman', 16, 'bold'))
lbluMarks = Label(updStu, text="Enter Marks",
                  font=('Times New Roman', 16, 'bold'))
enuRoll = Entry(updStu, bd=5, font=('Times New Roman', 16))
enuName = Entry(updStu, bd=5, font=('Times New Roman', 16))
enuMarks = Entry(updStu, bd=5, font=('Times New Roman', 16))
btnuSave = Button(updStu, text='Update', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f10)
btnuBack1 = Button(updStu, text='Back', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f8)

lbluRoll.pack(pady=10)
enuRoll.pack(pady=10)

lbluName.pack(pady=10)
enuName.pack(pady=10)

lbluMarks.pack(pady=10)
enuMarks.pack(pady=10)

btnuSave.pack(pady=10)
btnuBack1.pack(pady=10)
updStu.withdraw()


# --------------------------------------------------------------------------------------------------------------
# Delete Student
delStu = Toplevel(mainMenu)
delStu.title("Delete Student Record")
delStu.geometry("500x500+500+200")


def f9():
    delStu.withdraw()
    mainMenu.deiconify()


def f11():
    if len(endRoll.get()) == 0:
        messagebox.showerror('Error !', "Roll Number can\'t be empty !")
        endRoll.focus()
        return
    if not endRoll.get().isdigit():
        messagebox.showerror('Error !', "Roll number must be integer !")
        endRoll.focus()
        return
    try:
        con = sqlite3.connect('cruddb.sqlite')
        rno = int(endRoll.get())
        cursor = con.cursor()
        sql = "select roll from students"
        cursor.execute(sql)
        data4 = cursor.fetchall()
        present = False
        for d in data4:
            if d[0] == rno:
                present = True
                break
        if not present:
            messagebox.showerror("Error!", "Roll Number not found !")
            endRoll.focus()
            return
        else:
            sql = "delete from students where roll=?"
            args = (rno)
            cursor.execute(sql, args)
            con.commit()
            messagebox.showinfo('Success !', 'Recored deleted successfully')
            endRoll.delete(0, END)
            endRoll.focus()
    except sql3lite.Error:
        con.rollback()
        msg = "Record could not be deleted !"
        messagebox.showerror('Error !', msg)
    finally:
        if con is not None:
            con.close()


lbldRoll = Label(delStu, text="Enter Roll Number",
                 font=('Times New Roman', 16, 'bold'))
endRoll = Entry(delStu, bd=5, font=('Times New Roman', 16))
btndDelete = Button(delStu, text='Delete', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f11)
btndBack1 = Button(delStu, text='Back', font=(
    'Times New Roman', 16, 'bold'), width=10, command=f9)

lbldRoll.pack(pady=10)
endRoll.pack(pady=10)

btndDelete.pack(pady=10)
btndBack1.pack(pady=10)
delStu.withdraw()
mainMenu.mainloop()
