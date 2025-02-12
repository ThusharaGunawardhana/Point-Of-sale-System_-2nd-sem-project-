import tkinter as tk
from tkinter import ttk
import random,os
from tkinter import messagebox
import mysql.connector
from tkinter import *
from PIL import Image, ImageTk 
import tempfile
from time import strftime
import subprocess 

class Bill_App:
    def __init__(self, root):
        self.root = root 
        self.root.geometry("1300x800+0+0")
        self.root.title("Herath Tile Billing System")
        self.l=[]  #This line appends the calculated total cost
        self.Tax = 10 

        #============Variables=============
        self.c_name=StringVar()
        self.c_phone=StringVar()
        self.bill_no=StringVar()
        
        # New instance variable to store the generated bill number
        self.generated_bill_number = random.randint(1000, 9999)
        self.bill_no.set(self.generated_bill_number)

        self.search_bill=StringVar()
        self.product=StringVar()
        self.prices=IntVar()
        self.qty=IntVar()
        self.sub_total=StringVar()
        self.tax_input=StringVar()
        self.total = StringVar()

        Ibl_title = Label(self.root, text="HERATH TILES & ACCESSORIES", font=("times new roman", 28), bg="black", fg="white")
        Ibl_title.place(x=-100, y=10, width=1530, height=45)

        def time():
            string=strftime('%H:%M:%S %p')
            lbl.config(text= string)
            lbl.after(1000,time)

        lbl=Label(Ibl_title,font=("times new roman", 12, "bold"),bg="white",fg="blue")
        lbl.place(x=100,y=0,width=120,height=45)
        time()

        Main_Frame = Frame(self.root, bd=5, relief=GROOVE, bg="white")
        Main_Frame.place(x=0, y=100, width=1530, height=620)


        # Customer label frame
        Cust_Frame = LabelFrame(Main_Frame, text="Customer", font=("times new roman", 12, "bold"), bg="white", fg="red")
        Cust_Frame.place(x=10, y=5, width=300, height=140)

        self.Ibl_mob = Label(Cust_Frame, text="Mobile No", font=("times new roman", 12, "bold"), bg="white", fg="black")
        self.Ibl_mob.grid(row=0, column=0, sticky=W, padx=5, pady=2)

        self.entry_mob = ttk.Entry(Cust_Frame,textvariable=self.c_phone, font=("times new roman", 12, "bold"), width=24)
        self.entry_mob.grid(row=0, column=1)

        self.Ibl_cus = Label(Cust_Frame, text="Name", font=("times new roman", 12, "bold"), bg="white", fg="black")
        self.Ibl_cus.grid(row=1, column=0, sticky=W, padx=5, pady=2)

        self.entry_cus = ttk.Entry(Cust_Frame,textvariable=self.c_name, font=("times new roman", 12, "bold"), width=24)
        self.entry_cus.grid(row=1, column=1)



        # Product label
        Product_Frame = LabelFrame(Main_Frame, text="Product", font=("times new roman", 12, "bold"), bg="white", fg="red")
        Product_Frame.place(x=315, y=5, width=590, height=140)
        
        # Category combobox
        self.IblCategory = Label(Product_Frame, text="Tile Name", font=("arial", 10, "bold"), bg="white", fg="black")
        self.IblCategory.grid(row=0, column=0, sticky=W, padx=5, pady=2)
       
        self.combo_category = ttk.Combobox(Product_Frame,textvariable=self.product, font=("arial", 10, "bold"), width=24,state="readonly")
        #self.combo_category.current(0)
        self.combo_category.grid(row=0, column=1, sticky=W, padx=5, pady=2)
        #self.combo_category.bind("<<ComboboxSelected>>",self.Categories)
        
        # Subcategory combobox
        self.IblSubCategory = Label(Product_Frame, text="Tile Size", font=("arial", 10, "bold"), bg="white", fg="black")
        self.IblSubCategory.grid(row=1, column=0, sticky=W, padx=5, pady=2)
       
        self.combo_subcategory = ttk.Combobox(Product_Frame,values=[""], font=("arial", 10, "bold"), width=24)
        self.combo_subcategory.grid(row=1, column=1, sticky=W, padx=5, pady=2)
        #self.combo_subcategory.bind("<<ComboboxSelected>>",self.product_add)

        # Product qty label
        self.Iblproduct = Label(Product_Frame, text="Stock Qty", font=("arial", 10, "bold"), bg="white", fg="black")
        self.Iblproduct.grid(row=2, column=0, sticky=W, padx=5, pady=2)

        # Product qty combobox
        self.combo_product = ttk.Combobox(Product_Frame, font=("arial", 10, "bold"), width=24)
        self.combo_product.grid(row=2, column=1, sticky=W, padx=5, pady=2)
        #self.combo_product.bind("<<ComboboxSelected>>",self.price)

        # Price label
        self.Iblprice = Label(Product_Frame, text="Price", font=("arial", 10, "bold"), bg="white", fg="black")
        self.Iblprice.grid(row=3, column=0, sticky=W, padx=5, pady=2)

        # Price combobox
        self.combo_price = ttk.Combobox(Product_Frame,textvariable=self.prices, font=("arial", 10, "bold"), width=24)
        self.combo_price.grid(row=3, column=1, sticky=W, padx=5, pady=2)

        # Quantity label
        self.IblQty = Label(Product_Frame, text="QTY", font=("arial", 10, "bold"), bg="white", fg="black")
        self.IblQty.grid(row=3, column=2, sticky=W, padx=5, pady=2)

        # Quantity entry
        self.entry_qty = ttk.Entry(Product_Frame,textvariable=self.qty, font=("arial", 10, "bold"), width=24)
        self.entry_qty.grid(row=3, column=3, sticky=W, padx=5, pady=2)

        # Create the MiddleFrame
        MiddleFrame = Frame(Main_Frame, bd=5, bg="white")
        MiddleFrame.place(x=20, y=200, width=980, height=340)

        # Create the Treeview widget to display data
        cols = ('ID', 'Name', 'Size', 'Stock Qty', 'Price')
        self.listBox = ttk.Treeview(MiddleFrame, columns=cols, show='headings')

        for col in cols:
            self.listBox.heading(col, text=col)
            self.listBox.grid(row=1, column=0, columnspan=2)
            self.listBox.column(col, width=150, anchor=tk.CENTER)
            self.listBox.place(x=0, y=0)  # Adjust the coordinates as needed

         # Create a Scrollbar
        self.scrollbar = Scrollbar(MiddleFrame, orient=VERTICAL, command=self.listBox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Attach the scrollbar to the listbox
        self.listBox.config(yscrollcommand=self.scrollbar.set)
        

        # Search Frame
        search_Frame = Frame(Main_Frame, bd=2, bg="white")
        search_Frame.place(x=800, y=11, width=500, height=40)

        self.IblBill = Label(search_Frame, font=('arial', 12, 'bold'), fg="white", bg="white", text="Bill Number")
        self.IblBill.grid(row=0, column=0, sticky=W, padx=1)

        self.SearchEntry = ttk.Entry(search_Frame,textvariable=self.search_bill, font=("arial", 10, "bold"), width=24)
        self.SearchEntry.grid(row=0, column=2, sticky=W, padx=5, pady=2)

        self.BtnSearch = Button(search_Frame, text="Bill Number", font=("arial", 10, "bold"), bg="red", fg="white", bd=2)
        self.BtnSearch.grid(row=0, column=1, padx=5, pady=2)

        self.Btnser = Button(search_Frame,command=self.find_bill, cursor="hand2", text="search", font=('arial', 15, 'bold'), bg="red", fg="white")
        self.Btnser.grid(row=0, column=3)


        # Right_fraime_bill
        RightLabelFrame = LabelFrame(Main_Frame, text="Your BILL", font=("times new roman", 12, "bold"), bg="white", fg="red")
        RightLabelFrame.place(x=900, y=50, width=370, height=430)


        scroll_y = Scrollbar(RightLabelFrame, orient=VERTICAL)
        self.textarea = Text(RightLabelFrame, yscrollcommand=scroll_y.set, bg="white", fg="blue", font=("times new roman", 12, "bold"))
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.config(command=self.textarea.yview)
        self.textarea.pack(fill=BOTH, expand=1)

        # Product label
        Bottom_Frame = LabelFrame(Main_Frame, text="Bill counter", font=("times new roman", 12, "bold"), bg="white", fg="red")
        Bottom_Frame.place(x=0, y=485, width=1520, height=140)

        self.IblsubTotal = Label(Bottom_Frame, text="Sub Total", font=("arial", 12, "bold"), bg="white", fg="black", bd=4)
        self.IblsubTotal.grid(row=0, column=0, sticky=W, padx=5, pady=2)
       
        self.EntysubTotal = ttk.Entry(Bottom_Frame,textvariable=self.sub_total, font=("arial", 10, "bold"), width=24)
        self.EntysubTotal.grid(row=0, column=1, sticky=W, padx=5, pady=2)

        self.Ibl_tax = Label(Bottom_Frame, text="GOV Tax", font=("arial", 12, "bold"), bg="white", fg="black", bd=4)
        self.Ibl_tax.grid(row=1, column=0, sticky=W, padx=5, pady=2)
       
        self.txt_tax = ttk.Entry(Bottom_Frame,textvariable=self.tax_input, font=("arial", 10, "bold"), width=24)
        self.txt_tax.grid(row=1, column=1, sticky=W, padx=5, pady=2)

        self.IblAmountTotal = Label(Bottom_Frame, text="Total", font=("arial", 12, "bold"), bg="white", fg="black", bd=4)
        self.IblAmountTotal.grid(row=2, column=0, sticky=W, padx=5, pady=2)
       
        self.txtAmountTotal = ttk.Entry(Bottom_Frame,textvariable=self.total, font=("arial", 10, "bold"), width=24)
        self.txtAmountTotal.grid(row=2, column=1, sticky=W, padx=5, pady=2)

        self.cart = []
        # Button Frame
        Btn_Frame = Frame(Bottom_Frame, bd=2, bg="white")
        Btn_Frame.place(x=320, y=0)

        self.BtnAddToCartImage1 = PhotoImage(file="pos buttons\\addtocart.png")
        self.BtnAddToCart = Button(Btn_Frame, image=self.BtnAddToCartImage1, command=self.AddItem, cursor="hand2", bg="white", bd=0)
        self.BtnAddToCart.grid(row=0, column=0)

        self.BtnAddToCartImage2 = PhotoImage(file="pos buttons\\generatebill.png")
        self.Btngenerate_bill = Button(Btn_Frame,image=self.BtnAddToCartImage2,command=self.gen_bill, cursor="hand2", bg="white", bd=0)
        self.Btngenerate_bill.grid(row=0, column=1)

        #self.BtnAddToCartImage3 = PhotoImage(file="C:\\Users\\Thushara\\Desktop\\2nd sem project\\pos buttons\\savebill.png")
        #self.Btnsavebill = Button(Btn_Frame,image=self.BtnAddToCartImage3,command=self.save_bill, cursor="hand2", bg="white", bd=0)
        #self.Btnsavebill.grid(row=0, column=2)

        self.BtnAddToCartImage4 = PhotoImage(file="pos buttons\\print.png")
        self.Btnprint = Button(Btn_Frame,image=self.BtnAddToCartImage4,command=self.iprint, cursor="hand2", bg="white", bd=0)
        self.Btnprint.grid(row=0, column=3)

        self.BtnAddToCartImage5 = PhotoImage(file="pos buttons\\clear.png")
        self.Btnclear = Button(Btn_Frame,image=self.BtnAddToCartImage5,command=self.clear, cursor="hand2", bg="white", bd=0)
        self.Btnclear.grid(row=0, column=4)

        self.BtnAddToCartImage6 = PhotoImage(file="pos buttons\\exit.png")        
        self.Btnexit = Button(Btn_Frame,image=self.BtnAddToCartImage6,command=self.root.destroy,cursor="hand2", bg="white", bd=0)
        self.Btnexit.grid(row=0, column=5)

        self.BtnAdditemImage7 = PhotoImage(file="pos buttons\\edit.png")        
        self.Btnadd = Button(Btn_Frame,image=self.BtnAdditemImage7,command=self.additem,cursor="hand2", bg="white", bd=0)
        self.Btnadd.grid(row=0, column=7)
        self.welcome()


        self.l=[]
    #=======================function declaration ===========================

    def welcome(self):
        self.textarea.delete(1.0, END)
        current_datetime = strftime('%Y-%m-%d | %H:%M:%S %p')
        self.textarea.insert(END, f"\tWelcome to Herath Tiles & Accessories\n")
        self.textarea.insert(END, f"\nBill Number: {self.generated_bill_number}")
        self.textarea.insert(END, f"\nCustomer Name: {self.c_name.get()}")
        self.textarea.insert(END, f"\nPhone Number: {self.c_phone.get()}")
        self.textarea.insert(END, f"\nDate and Time: {current_datetime}")
        self.textarea.insert(END, "\n=====================================")
        self.textarea.insert(END, f"\nProducts\t\t\tQTY\t Price")
        self.textarea.insert(END, "\n=====================================")


    def AddItem(self):
        Tax = 0
        self.n = float(self.prices.get())
        self.m = self.qty.get() * self.n
        self.l.append(self.m) #This line appends the calculated total cost

        if self.product.get() == "":
            messagebox.showerror("Error", "Please select the product name")
        else:
            # Append the item to the cart list
            self.cart.append({
                'product': self.product.get(),
                'qty': self.qty.get(),
                'total': self.m,
            })

            self.textarea.insert(END, f"\n{self.product.get()}\t\t\t{self.qty.get()}\t{self.m}")
            self.sub_total.set(str('Rs.%.2f' % sum(self.l)))
            self.tax_input.set(str('Rs.%.2f' % ((((sum(self.l)) - (self.prices.get())) * Tax) / 100)))
            self.total.set(str('Rs.%.2f' % (((sum(self.l)) + ((((sum(self.l)) - (self.prices.get())) * Tax) / 100)))))


    def gen_bill(self):
        if not self.cart:
            messagebox.showerror("ERROR", "Please add products to the cart.")
            return

        text = self.textarea.get(1.0, END)
        self.welcome()

        for item in self.cart:
            self.textarea.insert(END, f"\n{item['product']}\t\t\t{item['qty']}\t{item['total']}")

        self.textarea.insert(END, "\n======================================")
        self.textarea.insert(END, f"\n Sub amount:\t\t\t{self.sub_total.get()}")
        self.textarea.insert(END, f"\n Tax amount:\t\t\t{self.tax_input.get()}")
        self.textarea.insert(END, f"\n Total amount:\t\t\t{self.total.get()}")
        self.textarea.insert(END, "\n======================================")
         # Call save_bill function to automatically save the bill
        self.save_bill()

    def save_bill(self):
        # Get the phone number from the input field
        phone_number = self.c_phone.get()

        if not phone_number:
            messagebox.showerror("Error", "Please enter a valid phone number.")
            return

        # Save the bill with phone number and generated bill number as filename
        filename = f'bills/{phone_number}_{self.generated_bill_number}.txt'
        with open(filename, 'w') as f1:
            f1.write(self.textarea.get(1.0, END))

        messagebox.showinfo("Saved", f"Bill No: {self.generated_bill_number} saved successfully")


    def iprint(self):
        q=self.textarea.get(0.1,"end-1c")
        filename=tempfile.mktemp('.txt')
        open(filename,'w').write(q)
        os.startfile(filename,"print")

    mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
    mycursor = mydb.cursor()

    def find_bill(self):
        # Get the search term (phone number or bill number) from the input field
        search_term = self.search_bill.get()

        # Extract phone number and bill number from the search term
        try:
            phone_number, bill_number = search_term.split(',')
            bill_number = int(bill_number)
        except ValueError:
            messagebox.showerror("ERROR", "Invalid search term format. Use phone_number,bill_number.")
            return

        # Search for the corresponding bill file
        found = "no"
        for file in os.listdir("bills/"):
            if file.startswith(f'{phone_number}_{bill_number}'):
                with open(f'bills/{file}', 'r') as f1:
                    self.textarea.delete(1.0, END)
                    for line in f1:
                        self.textarea.insert(END, line)
                    found = "yes"
        if found == "no":
            messagebox.showerror("ERROR", "No matching bill found.")    

    def clear(self):
        # Generate a new random bill number
        new_bill_number = random.randint(1000, 9999)
        self.generated_bill_number = new_bill_number  # Update the bill number attribute

        # Clear the entire content of the textarea
        self.textarea.delete(1.0, END)
        
        # Reset the cart list
        self.cart = []
        
        # Clear combo boxes in the Product_Frame
        self.product.set("")  # Clear product combo box
        self.combo_subcategory.set("")  # Clear subcategory combo box
        self.combo_product.set("")  # Clear stock qty combo box
        self.combo_price.set("")  # Clear price combo box
        self.entry_qty.delete(0, END)  # Clear quantity entry field

        # Reset other variables and rewrite the welcome message and header lines
        self.c_name.set("")
        self.c_phone.set("")
        self.sub_total.set("")
        self.tax_input.set("")
        self.total.set("")
        self.l = []  # Reset the list used for calculations
        
        # Rewrite the welcome message and header lines with the new bill number
        self.welcome()

    def GetValue(self, event):
        # Clear existing data in combo boxes and entry fields
        self.combo_category.set('')
        self.combo_subcategory.set('')
        self.combo_product.set('')
        self.combo_price.set('')
        self.entry_qty.delete(0, END)

        # Get the selected item from the listbox
        selected_item = self.listBox.item(self.listBox.selection())['values']

        if selected_item:
            name, size, stock, price = selected_item[1], selected_item[2], selected_item[3], selected_item[4]
            self.combo_category.set(name)
            self.combo_subcategory.set(size)
            self.combo_product.set(stock)
            self.combo_price.set(price)

    def additem(self):
        subprocess.Popen(["python", "edit.py"])

    

    def show_data(self):
        mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="2nd")
        mycursor = mydb.cursor()
        mycursor.execute("SELECT id, Name, size, stock, price FROM items")
        records = mycursor.fetchall()
        print(records)

        # Clear existing data
        for item in self.listBox.get_children():
            self.listBox.delete(item)

        for i, (id, Name, size, stock, price) in enumerate(records, start=1):
            self.listBox.insert("", "end", values=(id, Name, size, stock, price))
        # Double-click event on the listbox
        self.listBox.bind('<Double-Button-1>', self.GetValue)
        mydb.close()

if __name__ == '__main__':
    root = Tk()
    obj = Bill_App(root)
    
    obj.show_data()  # Call show_data method on the object
    root.mainloop()
