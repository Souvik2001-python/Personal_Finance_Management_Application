import customtkinter as ctk
from tkinter import messagebox
import sqlite3
from PIL import Image as PilImage
from customtkinter import CTkImage
from function import *

# Set appearance mode and theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

f = ('Times', 14)

# DB setup
con = sqlite3.connect('authentication.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS record(
                    name text, 
                    email text, 
                    contact number, 
                    gender text, 
                    country text,
                    password text
                )''')
con.commit()

# Insert function
def insert_record():
    check_counter = 0
    warn = ""
    if register_name.get() == "": warn = "Name can't be empty"
    else: check_counter += 1
    if register_email.get() == "": warn = "Email can't be empty"
    else: check_counter += 1
    if register_mobile.get() == "": warn = "Contact can't be empty"
    else: check_counter += 1
    if var.get() == "": warn = "Select Gender"
    else: check_counter += 1
    if variable.get() == "": warn = "Select Country"
    else: check_counter += 1
    if register_pwd.get() == "": warn = "Password can't be empty"
    else: check_counter += 1
    if pwd_again.get() == "": warn = "Re-enter password can't be empty"
    else: check_counter += 1
    if register_pwd.get() != pwd_again.get(): warn = "Passwords didn't match!"
    else: check_counter += 1

    if check_counter == 8:
        try:
            con = sqlite3.connect('authentication.db')
            cur = con.cursor()
            cur.execute("INSERT INTO record VALUES (:name, :email, :contact, :gender, :country, :password)", {
                'name': register_name.get(),
                'email': register_email.get(),
                'contact': register_mobile.get(),
                'gender': var.get(),
                'country': variable.get(),
                'password': register_pwd.get()
            })
            con.commit()
            messagebox.showinfo('confirmation', 'Record Saved')
        except Exception as ep:
            messagebox.showerror('', ep)
    else:
        messagebox.showerror('Error', warn)

# Login function
def login_response():
    try:
        con = sqlite3.connect('authentication.db')
        c = con.cursor()
        for row in c.execute("SELECT * FROM record"):
            username = row[1]
            pwd = row[5]
    except Exception as ep:
        messagebox.showerror('', ep)
        return

    uname = email_tf.get()
    upwd = pwd_tf.get()
    check_counter = 0
    if uname == "": warn = "Username can't be empty"
    else: check_counter += 1
    if upwd == "": warn = "Password can't be empty"
    else: check_counter += 1

    if check_counter == 2:
        if uname == username and upwd == pwd:
            root.withdraw()  # Hide main login window
            return open_the_app()  # Opens new GUI
            
        else:
            messagebox.showerror('Login Status', 'Invalid username or password')
    else:
        messagebox.showerror('', warn)

# Main window
root = ctk.CTk()
root.title('Login | Sign Up Page')
root.geometry('950x600')
root.maxsize(950,600)
root.minsize(950,600)




# Background
original_bg = PilImage.open("background.jpg")
bg_image = CTkImage(dark_image=original_bg, light_image=original_bg, size=original_bg.size)

# Background label setup
bg_label = ctk.CTkLabel(root, image=bg_image, text="")
bg_label.image = bg_image  # Prevent image garbage collection
bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

# Resize image on window resize
def resize_bg(event):
    new_width, new_height = event.width, event.height
    resized = original_bg.resize((new_width, new_height), PilImage.LANCZOS)
    new_bg = CTkImage(dark_image=resized, light_image=resized, size=(new_width, new_height))
    bg_label.configure(image=new_bg)
    bg_label.image = new_bg  # Update reference to prevent garbage collection

root.bind('<Configure>', resize_bg)


# Upper note
ctk.CTkLabel(
    root,
    text=" Don't Have Any Account ?? Sign Up First ",
    text_color="white",
    font=('Times', 16, 'bold'),
    fg_color="black"
).place(relx=0.5, rely=0.05, anchor='n')



# Variables
var = ctk.StringVar(value='male')
countries = []
variable = ctk.StringVar()
with open('countries.txt', 'r') as world:
    for country in world:
        countries.append(country.strip())
variable.set(countries[22] if len(countries) > 22 else countries[0])

# Left Frame (Login)
left_frame = ctk.CTkFrame(root, width=400, height=200,fg_color='white', border_color="White", border_width=1)
left_frame.place(x=100, y=100)

ctk.CTkLabel(left_frame, text="Login", text_color="black", font=('Times', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10, padx=10)
ctk.CTkLabel(left_frame, text="Enter Email", text_color="black", font=f).grid(row=1, column=0, sticky='w', pady=10, padx=10)
ctk.CTkLabel(left_frame, text="Enter Password", text_color="black", font=f).grid(row=2, column=0, pady=10, padx=10)

email_tf = ctk.CTkEntry(left_frame, font=f, corner_radius=10)
pwd_tf = ctk.CTkEntry(left_frame, font=f, show='*', corner_radius=10)
login_btn = ctk.CTkButton(left_frame, text='Login', font=f, corner_radius=10, fg_color="#007BFF", command=login_response)

email_tf.grid(row=1, column=1, pady=10, padx=10)
pwd_tf.grid(row=2, column=1, pady=10, padx=10)
login_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

# Right Frame (Register)
right_frame = ctk.CTkFrame(root, width=450, height=400,fg_color='white', border_color="#999", border_width=1)
right_frame.place(x=500, y=100)

ctk.CTkLabel(right_frame, text="Sign Up", text_color="black", font=('Times', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10, padx=10)
ctk.CTkLabel(right_frame, text="Enter Name", text_color="black", font=f).grid(row=1, column=0, sticky='w', pady=10, padx=15)
ctk.CTkLabel(right_frame, text="Enter Email", text_color="black", font=f).grid(row=2, column=0, sticky='w', pady=10, padx=15)
ctk.CTkLabel(right_frame, text="Contact Number", text_color="black", font=f).grid(row=3, column=0, sticky='w', pady=10, padx=15)
ctk.CTkLabel(right_frame, text="Select Gender", text_color="black", font=f).grid(row=4, column=0, sticky='w',padx=15)
ctk.CTkLabel(right_frame, text="Select Country", text_color="black", font=f).grid(row=7, column=0, sticky='w', pady=10, padx=15)
ctk.CTkLabel(right_frame, text="Enter Password", text_color="black", font=f).grid(row=8, column=0, sticky='w', pady=10, padx=15)
ctk.CTkLabel(right_frame, text="Re-Enter Password", text_color="black", font=f).grid(row=9, column=0, sticky='w', pady=10, padx=15)

register_name = ctk.CTkEntry(right_frame, font=f, corner_radius=10)
register_email = ctk.CTkEntry(right_frame, font=f, corner_radius=10)
register_mobile = ctk.CTkEntry(right_frame, font=f, corner_radius=10)
register_pwd = ctk.CTkEntry(right_frame, font=f, show='*', corner_radius=10)
pwd_again = ctk.CTkEntry(right_frame, font=f, show='*', corner_radius=10)
register_country = ctk.CTkOptionMenu(right_frame, variable=variable, values=countries, font=('Times', 12), corner_radius=10)

register_btn = ctk.CTkButton(right_frame, text='Sign Up', font=f, corner_radius=10, fg_color="#28A745", command=insert_record)

# Gender Buttons
male_rb = ctk.CTkRadioButton(right_frame, text='Male', variable=var, value='male', font=('Times', 10))
female_rb = ctk.CTkRadioButton(right_frame, text='Female', variable=var, value='female', font=('Times', 10))
others_rb = ctk.CTkRadioButton(right_frame, text='Others', variable=var, value='others', font=('Times', 10))

# Layout
register_name.grid(row=1, column=1, pady=10, padx=10)
register_email.grid(row=2, column=1, pady=10, padx=10)
register_mobile.grid(row=3, column=1, pady=10, padx=10)
male_rb.grid(row=4, column=1)
female_rb.grid(row=5,column=1)
others_rb.grid(row=6, column=1)
register_country.grid(row=7, column=1, pady=10, padx=10)
register_pwd.grid(row=8, column=1, pady=10, padx=10)
pwd_again.grid(row=9, column=1, pady=10, padx=10)
register_btn.grid(row=10, column=0, columnspan=2, pady=10, padx=10)

root.mainloop()
