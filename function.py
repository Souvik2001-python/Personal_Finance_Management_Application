# import modules
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox
import customtkinter as ctk
from graph import *
from tkinter import Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



# object for database
data = Database(db='myexpense.db')

# global variables
count = 0
selected_rowid = 0
refresh_id = None  # ← Add this near your global variables

# functions
def open_the_app():
    # to save records
    def saveSalary():
        global data
        data.insertSalary(amount=salary.get(),credit_date=transaction_date.get())
    def saveRecord():
        global data
        data.insertRecord(item_name= item_name.get(),item_price=item_amt.get(),purchase_date=transaction_date.get())

    # to set date
    def setDate():
        date = dt.datetime.now()
        dopvar.set(f'{date:%d %B %Y}')

    # to clear entries
    def clearEntries():
        salary.delete(0,'end')
        item_name.delete(0,'end')
        item_amt.delete(0,'end')
        transaction_date.delete(0,'end')

    # to fetch and show the data
    def fetch_records():
        f = data.fetchRecord('select rowid, * from expense_record')
        global count, refresh_id
        for rec in f:
            tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
            count += 1
        refresh_id = tv.after(400, refreshData)  # ← Store after() ID

    # to select records
    def select_record(event):
        global selected_rowid
        selected = tv.focus()
        val = tv.item(selected,'values')

        try:
            selected_rowid = val[0]
            d = val[3]
            namevar.set(val[1])
            amtvar.set(val[2])
            dopvar.set(str(d))
        except Exception as ep:
            pass
        
    # update the records
    def update_record():
        global selected_rowid
        selected = tv.focus()

        try :
            data.updateRecord(namevar.get(),amtvar.get(),dopvar.get(),selected_rowid)
            tv.item(selected,text="",values=(namevar.get(),amtvar.get(),dopvar.get()))
        except Exception as ep:
            messagebox.showerror('Error',ep)
        
        # clear entry boxes
        item_name.delete(0,END)
        item_amt.delete(0,END)
        transaction_date.delete(0,END)
        tv.after(400,refreshData)

    # function for total balance
    def totalBalance():
        sal_data = data.fetchSalary(query="SELECT SUM(amount) FROM salary")
        sal_data = float(sal_data)
        f = data.fetchRecord(query="SELECT sum(item_price) from expense_record")

        for i in f :
            for j in i :
                if j == None:
                    messagebox.showinfo('Salary status : ',f"Total Salary : {sal_data} /-\nTotal Expense : {0} \nBalance Remaining(savings) : {sal_data}")
                else :
                    messagebox.showinfo('Salary status : ',f"Total Salary : {sal_data} /-\nTotal Expense : {j} \nBalance Remaining(savings) : {sal_data - j}")

    # to refresh all the datas
    def refreshData():
        global count
        count = 0
        for item in tv.get_children():
            tv.delete(item)
        fetch_records()


    # delete data
    def deleteRow():
        global selected_rowid
        data.removeRecord(selected_rowid)
        refreshData()

    # function to plot graph 

    def plotGraph():
        graphplot = Toplevel(ws)
        graphplot.title("Graph Plot - Income vs Expense vs Savings")
        graphplot.geometry("900x780")

        # Get the figure and embed into the GUI
        fig = plot_daily_income_expense_savings()
        canvas = FigureCanvasTkAgg(fig, master=graphplot)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)


    def close_app():
        if refresh_id:
            tv.after_cancel(refresh_id)  # Cancel the scheduled callback
        ws.destroy()



    # create tkinter object (Main GUI Part)
    ws = Tk()
    ws.geometry("720x420")
    # ws.maxsize(720,420)
    # ws.minsize(720,420)
    ws.configure(bg="black")
    ws.title("Personal Finance Management Application")

    #variables type
    f = ('Times new roman',14)
    salvar = IntVar()
    namevar = StringVar()
    amtvar = IntVar()
    dopvar = StringVar()

    # frame widget
    f2 = Frame(ws)
    f2.pack()

    f1 = Frame(ws,padx = 10,pady = 10,borderwidth=6,bg="black")
    f1.pack(expand=True,fill = BOTH)

    # Label widget
    Label(f1,text='Enter the Salary',font=f,bg="black",fg="white").grid(row=0,column=0,sticky=W)
    Label(f1,text='Transaction type',font=f,bg="black",fg="white").grid(row=1,column=0,sticky=W)
    Label(f1,text='Amount',font=f,bg="black",fg="white").grid(row=2,column=0,sticky=W)
    Label(f1,text='Current DATE',font=f,bg="black",fg="white").grid(row=3,column=0,sticky=W)

    # Entry widget
    salary = Entry(f1,font=f,textvariable=salvar)
    item_name = Entry(f1,font=f,textvariable=namevar)
    item_amt = Entry(f1,font=f,textvariable=amtvar)
    transaction_date = Entry(f1,font=f,textvariable=dopvar)

    # Entry grid placement
    salary.grid(row=0,column=1,sticky=EW,padx=(10,10))
    item_name.grid(row=1,column=1,sticky=EW,padx=(10,10))
    item_amt.grid(row=2,column=1,sticky=EW,padx=(10,10))
    transaction_date.grid(row=3,column=1,sticky=EW,padx=(10,10))

    # Action Buttons
    salary_btn = ctk.CTkButton(f1,text='Save Salary',font = ("Times new roman",17,"bold"),text_color="black",fg_color='#ffff33',command=saveSalary,height= 35, width=10,corner_radius=5)
    plot_btn = ctk.CTkButton(f1,text='Generate Graph',font = ("Times new roman",17,"bold"),text_color="black",fg_color='#8e44ad',command=plotGraph,height= 35, width=10,corner_radius=5)
    cur_date = ctk.CTkButton(f1,text='Current Date',font = ("Times new roman",17,"bold"),text_color="black",fg_color='#27ae60',command=setDate,height= 35, width=10,corner_radius=10)
    submit_btn = ctk.CTkButton(f1,text='Save Record',font = ("Times new roman",16,"bold"),text_color="white",fg_color='#2980b9',command=saveRecord,height= 35, width=10,corner_radius=5)
    clr_btn = ctk.CTkButton(f1,text='Clear Entry',font = ("Times new roman",16,"bold"),text_color="white",fg_color='#f39c12',command=clearEntries,height= 35, width=10,corner_radius=5)
    quit_btn = ctk.CTkButton(f1,text='Exit',font = ("Times new roman",16,"bold"),text_color="white",fg_color='#e74c3c',command=close_app,height= 35, width=10,corner_radius=5)
    total_bal = ctk.CTkButton(f1,text='Total Balance',font = ("Times new roman",16,"bold"),text_color="white",fg_color='#16a085',command=totalBalance,height= 35, width=10,corner_radius=5)
    update_btn = ctk.CTkButton(f1,text='Update',font = ("Times new roman",16,"bold"),text_color="white",fg_color='#34495e',command=update_record,height= 35, width=10,corner_radius=5)
    del_btn = ctk.CTkButton(f1,text='Delete',font = ("Times new roman",16,"bold"),text_color="white",fg_color='#c0392b',command=deleteRow,height= 35, width=10,corner_radius=5)


    # Action button placement
    salary_btn.grid(row=0,column=2,sticky=EW,padx=(10,10),pady=3)
    plot_btn.grid(row=0,column=3,sticky=EW,padx=(10,10),pady=3)
    cur_date.grid(row=4,column=1,sticky=EW,padx=(10,10),pady=3)
    submit_btn.grid(row=1,column=2,sticky=EW,padx=(10,10),pady = 3)
    clr_btn.grid(row=2,column=2,sticky=EW,padx=(10,10),pady = 3)
    quit_btn.grid(row=3,column=2,sticky=EW,padx=(10,10),pady = 3)
    total_bal.grid(row=1,column=3,sticky=EW,padx=(10,10),pady = 3)
    update_btn.grid(row=2,column=3,sticky=EW,padx=(10,10),pady = 3)
    del_btn.grid(row=3,column=3,sticky=EW,padx=(10,10),pady = 3)

    # Treeview widget
    tv = ttk.Treeview(f2,columns=(1,2,3,4),show = 'headings',height=8)
    tv.pack(side = "left")

    # add heading to treeview
    tv.column(1,anchor=CENTER,stretch=NO,width=70)
    tv.column(2,anchor=CENTER)
    tv.column(3,anchor=CENTER)
    tv.column(4,anchor=CENTER)

    tv.heading(1,text="Serial no")
    tv.heading(2,text="Item Name")
    tv.heading(3,text="Item Price")
    tv.heading(4,text="Purchase Date")

    # binding treeview
    tv.bind("<ButtonRelease-1>",select_record)

    # style for treeview
    style = ttk.Style()
    style.theme_use("default")
    style.map("Treeview")

    # Vertical Scrollbar
    scrollbar = Scrollbar(f2,orient='vertical')
    scrollbar.configure(command=tv.yview)
    scrollbar.pack(side="right",fill="y")
    tv.config(yscrollcommand=scrollbar.set)

    # calling function to show all records
    fetch_records()


    ws.mainloop()

