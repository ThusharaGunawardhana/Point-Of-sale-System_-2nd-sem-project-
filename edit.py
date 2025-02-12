import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from tkinter import *
mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
mycursor=mydb.cursor()

def GetValue(event):
   e1.delete(0, END)
   e2.delete(0, END)
   e3.delete(0, END)
   e4.delete(0, END)
   e5.delete(0, END)
   

   row_id = listBox.selection()[0]
   select = listBox.set(row_id)

   e1.insert(0,select['id'])
   e2.insert(0,select['Name'])
   e3.insert(0,select['size'])
   e4.insert(0,select['stock'])
   e5.insert(0,select['price'])
   

def Add():
    Id = e1.get()
    name = e2.get()
    Size = e3.get()
    Stock = e4.get()
    Price=e5.get()
    

    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
    mycursor=mydb.cursor()

    try:
       sql = "INSERT INTO  items (id,Name,size,stock,price) VALUES (%s, %s, %s, %s,%s)"
       val = (Id,name,Size,Stock,Price)
       mycursor.execute(sql, val)
       mydb.commit()
       lastid = mycursor.lastrowid
       messagebox.showinfo("information", " inserted successfully...")
       e1.delete(0, END)
       e2.delete(0, END)
       e3.delete(0, END)
       e4.delete(0, END)
       e5.delete(0,END)
       e1.focus_set()
    except Exception as e:
       print(e)
       mydb.rollback()
       mydb.close()


def update():
    Id = e1.get()
    name = e2.get()
    Size = e3.get()
    Stock = e4.get()
    Price=e5.get()
    
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
    mycursor=mydb.cursor()

    try:
       sql = "UPDATE  items SET Name= %s,size= %s,stock= %s,price=%s WHERE id= %s"
       val = (name,Size,Stock,Price,Id)
       mycursor.execute(sql, val)
       mydb.commit()
       lastid = mycursor.lastrowid
       messagebox.showinfo("information", "Record Updated successfully...")

       e1.delete(0, END)
       e2.delete(0, END)
       e3.delete(0, END)
       e4.delete(0, END)
       e5.delete(0,END)
       e1.focus_set()

    except Exception as e:

       print(e)
       mydb.rollback()
       mydb.close()

def delete():
    Id = e1.get()

    if not Id:  # Check if ID is entered
        messagebox.showwarning("Warning", "Please enter an ID to delete.")
        return

    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete record ID {Id}?")

    if confirm:  # Proceed only if the user clicks "Yes"
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
        mycursor = mydb.cursor()

        try:
            sql = "DELETE FROM items WHERE id = %s"
            val = (Id,)
            mycursor.execute(sql, val)
            mydb.commit()

            messagebox.showinfo("Information", "Record deleted successfully!")

            # Clear input fields
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
            e4.delete(0, END)
            e5.delete(0, END)
            e1.focus_set()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            mydb.rollback()
        
        finally:
            mydb.close()


def refresh():
    # Clear entries
    e1.delete(0, tk.END)
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)

    # Clear existing data in the Treeview widget
    for item in listBox.get_children():
        listBox.delete(item)

    # Show the latest data
    show()

def show():
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
        mycursor=mydb.cursor()
        mycursor.execute("SELECT id,Name,size,stock,price FROM items")
        records = mycursor.fetchall()
        print(records)

        for i, (id,Name,size,stock,price) in enumerate(records, start=1):
            listBox.insert("", "end", values=(id,Name,size,stock,price))
            mydb.close()

root = Tk()
root.geometry("1200x700")
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
global e5

tk.Label(root, text="Herath accessories DBMS", fg="red", font=("cambria", 30)).place(x=400, y=7)
tk.Label(root, text="Item Table", fg="red", font=("cambria", 25)).place(x=500, y=55)

tk.Label(root, text="Item id").place(x=10, y=10)
Label(root, text="item name ").place(x=10, y=40)
Label(root, text="item size").place(x=10, y=70)
Label(root, text="stock").place(x=10, y=100)
Label(root, text="price").place(x=10, y=130)


e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=40)

e3 = Entry(root)
e3.place(x=140, y=70)

e4 = Entry(root)
e4.place(x=140, y=100)

e5 = Entry(root)
e5.place(x=140, y=130)


round= PhotoImage(file="addbutton.png")
Button(root,image= round, command = Add,border=0).place(x=250, y=190)
round1= PhotoImage(file="updatebutton.png")
Button(root,image= round1 ,command = update,border=0).place(x=500, y=190)
round2= PhotoImage(file="Deletebutton.png")
Button(root,image= round2,command = delete,border=0).place(x=750, y=190)
round3= PhotoImage(file="refresh.png")
Button(root,image= round3,command = refresh,border=0).place(x=1000, y=190)

cols = ('id','Name','size','stock','price')
listBox = ttk.Treeview(root, columns=cols, show='headings' )

for col in cols:
    listBox.heading(col, text=col)
    listBox.grid(row=1, column=0, columnspan=2)
    listBox.column(col, width=150, anchor=tk.CENTER) #grid view size increase and decrease coloms and box
    listBox.place(x=100, y=300)

show()
listBox.bind('<Double-Button-1>',GetValue)
c.pack()
root.mainloop()