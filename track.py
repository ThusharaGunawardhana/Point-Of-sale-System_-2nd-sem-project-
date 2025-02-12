import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *
from subprocess import call
mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
mycursor=mydb.cursor()

def GetValue(event):
   e1.delete(0, END)
   e2.delete(0, END)
   e3.delete(0, END)
   e4.delete(0, END)
   
  

def login(mycursor, data):
   mycursor.execute(f"""SELECT * FROM employee WHERE email = '{data["email"]}' 
                     AND password = '{data["password"]}' """)
     
   if mycursor.fetchone() != None:
        return True
   return False

   


def Add():
    f_name = e1.get()
    l_name = e2.get()
    email = e3.get()
    password=e4.get()
   

    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
    mycursor=mydb.cursor()

    try:
       sql = "INSERT INTO  employee (F_name,L_name,email,password) VALUES (%s, %s, %s,%s)"
       val = (f_name,l_name,email,password)
       mycursor.execute(sql, val)
       mydb.commit()
       lastid = mycursor.lastrowid
       messagebox.showinfo("information", "employee inserted successfully...")
       e1.delete(0, END)
       e2.delete(0, END)
       e3.delete(0, END)
       e4.delete(0, END)
       e1.focus_set()
    except Exception as e:
       print(e)
       mydb.rollback()
       mydb.close()


def back():
   root.destroy()
   call(["python","login.py"])



root = Tk()
root.geometry("600x500")
root.title("Herath accessories")
c=Canvas(root,bg="gray16")
root.iconbitmap(r'mosaic.ico')
filename=PhotoImage(file="")
label=Label(root, image=filename)
label.place(x=0,y=0,relwidth=1,relheight=1 )

global e1
global e2
global e3
global e4

tk.Label(root, text="employee Registation", fg="Black", font=("cambria", 25)).place(x=150, y=10)
#tk.Label(root, text="track Table", fg="red", font=("cambria", 25)).place(x=400, y=55)

tk.Label(root, text="First name:").place(x=100, y=145)
Label(root, text="Last name:").place(x=100, y=200)
Label(root, text="email:").place(x=100, y=250)
Label(root, text="Password:").place(x=100, y=300)


e1 = Entry(root)
e1.place(x=180, y=145)

e2 = Entry(root)
e2.place(x=180, y=200)

e3 = Entry(root)
e3.place(x=180, y=250)

e4 = Entry(root)
e4.place(x=180, y=300)



round= PhotoImage(file="addbt.png")
Button(root,image= round, command = Add,border=0).place(x=180, y=350)

round1= PhotoImage(file="backbt.png")
Button(root,image= round1, command = back,border=0).place(x=300, y=350)



c.pack()
root.mainloop()