import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pickle

# Data storage
class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.balance = 0
        self.transactions = []

# User Authentication
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username].password == password:
        current_user.set(username)
        main_screen()
    else:
        messagebox.showerror("Login Error", "Invalid credentials")

def register():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showerror("Registration Error", "Username and password cannot be empty")
        return

    if username in users:
        messagebox.showerror("Registration Error", "User already exists")
    else:
        users[username] = User(username, password)
        save_data()
        messagebox.showinfo("Registration Successful", "User registered successfully")

def logout():
    current_user.set("")
    login_screen()

def show_user_details():
    user = users[current_user.get()]
    show_edit_user_window(user)

def show_edit_user_window(user):
    def save_changes():
        new_username = username_entry.get()
        new_password = password_entry.get()

        if not new_username or not new_password:
            messagebox.showerror("Error", "Username and password cannot be empty")
            return

        if new_username != user.username and new_username in users:
            messagebox.showerror("Error", "Username already exists")
            return

        # Remove old user data
        del users[user.username]

        # Update user details
        user.username = new_username
        user.password = new_password
        users[new_username] = user
        save_data()
        messagebox.showinfo("Success", "User details updated successfully")
        edit_window.destroy()

    edit_window = tk.Toplevel(window)
    edit_window.title("Edit User Details")

    tk.Label(edit_window, text="Username").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    username_entry = tk.Entry(edit_window)
    username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
    username_entry.insert(0, user.username)

    tk.Label(edit_window, text="Password").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    password_entry = tk.Entry(edit_window, show="*")
    password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
    password_entry.insert(0, user.password)

    tk.Button(edit_window, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2, pady=10)

# Account Management
def deposit():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError("The amount must be positive")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive amount")
        return

    users[current_user.get()].balance += amount
    users[current_user.get()].transactions.append(f"Deposited: ${amount}")
    save_data()
    amount_entry.delete(0, tk.END)
    messagebox.showinfo("Success", "Amount deposited successfully")

def withdraw():
    try:
        amount = float(amount_entry.get())
        if amount <= 0:
            raise ValueError("The amount must be positive")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid positive amount")
        return

    if amount > users[current_user.get()].balance:
        messagebox.showerror("Error", "Insufficient funds")
    else:
        users[current_user.get()].balance -= amount
        users[current_user.get()].transactions.append(f"Withdrew: ${amount}")
        save_data()
        amount_entry.delete(0, tk.END)
        messagebox.showinfo("Success", "Amount withdrawn successfully")

def toggle_balance():
    if balance_label.cget("text") == "":
        balance_label.config(text=f"Balance: ${users[current_user.get()].balance}")
        check_balance_button.config(text="Hide Balance")
    else:
        balance_label.config(text="")
        check_balance_button.config(text="Check Balance")

def show_transactions():
    transactions_text.delete(1.0, tk.END)
    for transaction in users[current_user.get()].transactions:
        transactions_text.insert(tk.END, transaction + "\n")

# Saving and loading data
def save_data():
    with open("users.pkl", "wb") as f:
        pickle.dump(users, f)

def load_data():
    try:
        with open("users.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

# User Interface
def login_screen():
    global username_entry, password_entry

    for widget in window.winfo_children():
        widget.destroy()

    frame = ttk.Frame(window, padding="20")
    frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    title_label = ttk.Label(frame, text="Online Banking System", font=("Arial", 20, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    ttk.Label(frame, text="Username").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    username_entry = ttk.Entry(frame)
    username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    ttk.Label(frame, text="Password").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    password_entry = ttk.Entry(frame, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    buttons_frame = ttk.Frame(frame)
    buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

    ttk.Button(buttons_frame, text="Login", command=login).grid(row=0, column=0, padx=10)
    ttk.Button(buttons_frame, text="Register", command=register).grid(row=0, column=1, padx=10)

def main_screen():
    global amount_entry, balance_label, transactions_text, check_balance_button

    for widget in window.winfo_children():
        widget.destroy()

    top_frame = ttk.Frame(window, padding="10")
    top_frame.pack(side=tk.TOP, fill=tk.X, anchor=tk.NE)

    user_details_button = ttk.Button(top_frame, text="User Details", command=show_user_details)
    user_details_button.pack(side=tk.RIGHT, padx=5, pady=5)

    logout_button = ttk.Button(top_frame, text="Logout", command=logout)
    logout_button.pack(side=tk.RIGHT, padx=5, pady=5)

    main_frame = ttk.Frame(window, padding="20")
    main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=(0, 20))

    title_label = ttk.Label(main_frame, text="Account Dashboard", font=("Arial", 20, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=10)

    balance_label = ttk.Label(main_frame, text="")
    balance_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10)

    ttk.Label(main_frame, text="Amount").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    amount_entry = ttk.Entry(main_frame)
    amount_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    buttons_frame = ttk.Frame(main_frame)
    buttons_frame.grid(row=3, column=0, columnspan=2, pady=10)

    ttk.Button(buttons_frame, text="Deposit", command=deposit).grid(row=0, column=0, padx=5, pady=5)
    ttk.Button(buttons_frame, text="Withdraw", command=withdraw).grid(row=0, column=1, padx=5, pady=5)
    check_balance_button = ttk.Button(buttons_frame, text="Check Balance", command=toggle_balance)
    check_balance_button.grid(row=1, column=0, padx=5, pady=5)
    ttk.Button(buttons_frame, text="Show Transactions", command=show_transactions).grid(row=1, column=1, padx=5, pady=5)

    transactions_text = tk.Text(main_frame, height=10, width=50)
    transactions_text.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky="n")

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Online Banking System")
    window.geometry("450x500")

    style = ttk.Style()
    style.configure("TLabel",font=("Arial", 12))
    style.configure("TButton", font=("Arial", 12))
    style.configure("TEntry", font=("Arial", 12))
    
    users = load_data()
    current_user = tk.StringVar()

    login_screen()
    window.mainloop()