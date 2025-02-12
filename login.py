from tkinter import * #import all in tkinter
from tkinter import messagebox
from subprocess import call
from PIL import ImageTk,Image
import mysql.connector
mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
mycursor=mydb.cursor()

def login():
    username=entry1.get()
    password=entry2.get()
    #data = {}
    #data["email"] =entry1.get()
    #data["password"] =entry2.get()
    if len(password)>8 or len(password)<8:
        messagebox.showinfo("Loging",'Password Must Be 8 Characters')
        
        

    elif (username==""and password==""):
        messagebox.showinfo("Loging",'Blank not allowed')
    else:
        # Check if the username and password match in the database
        mycursor.execute("SELECT * FROM employee WHERE email = %s AND password = %s", (username, password))
        user = mycursor.fetchone()
        if user:
            messagebox.showinfo("Login", 'Employee Login Success')
            root.destroy()
            call(["python", "POS 2.py"])
        elif username == "admin" and password == "87654321":
            messagebox.showinfo("Login", 'Admin Login Success')
            root.destroy()
            call(["python", "pos.py"])
        else:
            messagebox.showinfo("Login", 'Invalid username or password')





def add():
    root.destroy()
    call(["python","track.py"])           #create acc


root=Tk()
filename=PhotoImage(file="loginbg.png")
root.iconbitmap(r'mosaic.ico')

label=Label(root, image=filename)
label.place(x=0,y=0,relwidth=1,relheight=1 )
bgc='black'
fgc='white'
root.configure(bg=bgc)#box colour
#root.iconbitmap(r'')
root.title('Herath accessories')
root.geometry("500x400")
global entry1
global entry2
Label(root,text="Username",bg="white").place(x=100,y=200)

Label(root,text="Password",bg="white").place(x=100,y=250)
pwd=StringVar()

#username entry
entry1=Entry(root,bd=5)
entry1.place(x=200,y=200)
#password entry
entry2=Entry(root,textvariable=pwd,show='*',bd=5)
entry2.place(x=200,y=250)
#loging button
round= PhotoImage(file="login button.png")
Button(root,image=round,command=login,border=0,bg="white").place(x=210,y=300)

round1= PhotoImage(file="createacc.png")
Button(image=round1,command=add,border=0,bg="white").place(x=198,y=350)





    





   









mydb.commit()
root.mainloop()#end of tkinter