from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_file(data):
    with open("data.json", "w") as data_file:
        json.dump(data, data_file, indent=4)

def find_password():
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            search_keyword = website_input.get()

            if not search_keyword:
                raise ValueError('Empty String')

            data_dict = data[search_keyword]

            messagebox.showinfo(title=search_keyword, message=f"E-mail: {data_dict['email']}\nPassword: {data_dict['password']}")

    except KeyError:
        messagebox.showerror(title=f"No entry for {search_keyword}", message=f"The website {search_keyword} doesn't exists")
    except FileNotFoundError:
        messagebox.showerror(title="File not found", message="File was not found, please restart the application")
    except ValueError:
        messagebox.showerror(title="Field error", message="Field Website must contain a keyword")

def save():
    website = website_input.get()
    email_username = email_username_input.get()
    password = password_input.get()
    formated_credentials = f"{website} | {email_username} | {password}"
    
    new_data = {
        website: {
        "email": email_username,
        "password": password
        }
    }

    if len(website) == 0 or len(email_username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oopss", message="Don't let any input empty")
    else:
        try: 
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            save_file(new_data)
        else:
            data.update(new_data)
            save_file(data)
        finally:
            website_input.delete(0, END)
            email_username_input.delete(0, END)
            password_input.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.resizable(False, False)

# CANVAS
canvas = Canvas(height=200, width=200, highlightthickness=0)

logo = PhotoImage(file="logo.png")

canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# WEBSITE LABEL ----------------------------
website_label = Label(text="Website:")
website_label.grid(column="0", row=1)

# WEBSITE INPUT
website_input = Entry()
website_input.config(width=35)
website_input.grid(column=1, row=1, columnspan=2)
website_input.focus()

# SEARCH BUTTON
def search(): 
    print("search")
    find_password()

search_button = Button(text="Search", width=10)
search_button.config(command=search)
search_button.grid(column=2, row=1)


# EMAIL / USERNAME LABEL ----------------------------
email_username_label = Label(text="Email/Username:")
email_username_label.grid(column=0, row=2)

# EMAIL / USERNAME INPUT
email_username_input = Entry()
email_username_input.config(width=35)
email_username_input.grid(column=1, row=2, columnspan=2)

# PASSWORD LABEL ----------------------------
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# PASSWORD INPUT
password_input = Entry()
password_input.config(width=35)
password_input.grid(column=1, row=3, columnspan=2)

# GENERATE PASSWORD BUTTON ----------------------------
def generate_password_click():
    generate_password()

generate_password_button = Button(text="Generate Password", width=10)
generate_password_button.config(command=generate_password_click)
generate_password_button.grid(column=2, row=3)

# ADD CREDENTIALS ----------------------------
def add_credentials():
    save()

add_credentials_button = Button(text="Add")
add_credentials_button.config(width=33, command=add_credentials)
add_credentials_button.grid(column=1, row=4, columnspan=2)




window.mainloop()