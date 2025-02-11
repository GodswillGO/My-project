import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


class BankAccount:
    def __init__(self, account_number, account_holder, initial_balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = initial_balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False


class BankingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Banking App")

        # Dictionary to store accounts
        self.accounts = {}

        # Initialize welcome page
        self.create_welcome_page()

    def create_welcome_page(self):
        self.welcome_frame = tk.Frame(self.root, width=500, height=400)
        self.welcome_frame.pack(fill="both", expand=True)

        # Background image
        self.bg_image = ImageTk.PhotoImage(Image.open("bankapp.jpg"))
        bg_label = tk.Label(self.welcome_frame, image=self.bg_image)
        bg_label.place(relwidth=1, relheight=1)

        # Welcome text
        welcome_label = tk.Label(self.welcome_frame, text="Welcome to GTWorld Banking App", font=("Sanserif", 16), bg="#DD4F05", fg='white')
        welcome_label.place(relx=0.5, rely=0.3, anchor="center")

        # Start button
        start_button = tk.Button(self.welcome_frame, text="Start", command=self.show_main_interface, font=("Arial", 14), bg="#DD4F05", fg="white")
        start_button.place(relx=0.5, rely=0.5, anchor="center")

    def show_main_interface(self):
        self.welcome_frame.destroy()
        self.create_main_interface()

    def create_main_interface(self):
        # Main interface
        self.canvas = tk.Canvas(self.root, width=500, height=400)
        self.canvas.pack(fill="both", expand=True)

        # Load and display the background image
        self.bg_image = ImageTk.PhotoImage(Image.open("bankapp.jpg"))
        self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

        # UI elements
        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account_window)
        self.canvas.create_window(200, 50, anchor="nw", window=self.create_account_button)

        self.deposit_button = tk.Button(self.root, text="Deposit", command=self.deposit_window, state=tk.DISABLED)
        self.canvas.create_window(200, 100, anchor="nw", window=self.deposit_button)

        self.withdraw_button = tk.Button(self.root, text="Withdraw", command=self.withdraw_window, state=tk.DISABLED)
        self.canvas.create_window(200, 150, anchor="nw", window=self.withdraw_button)

        self.check_balance_button = tk.Button(self.root, text="Check Balance", command=self.check_balance_window, state=tk.DISABLED)
        self.canvas.create_window(200, 200, anchor="nw", window=self.check_balance_button)

    def create_account_window(self):
        self.create_dialog("Create Account", self.create_account_logic, include_balance=True)

    def create_account_logic(self, account_holder, account_number, initial_balance):
        if account_holder and account_number and initial_balance is not None:
            if account_number not in self.accounts:
                self.accounts[account_number] = BankAccount(account_number, account_holder, initial_balance)
                messagebox.showinfo("Success", "Account created successfully!")
                self.enable_buttons()
            else:
                messagebox.showwarning("Error", "Account number already exists.")

    def deposit_window(self):
        self.create_dialog("Deposit", self.deposit_logic, include_balance=False)

    def deposit_logic(self, account_holder, account_number, amount):
        account = self.accounts.get(account_number)
        if account:
            if account.deposit(amount):
                messagebox.showinfo("Success", f"${amount} deposited successfully.")
            else:
                messagebox.showwarning("Error", "Invalid deposit amount.")
        else:
            messagebox.showwarning("Error", "Account not found.")

    def withdraw_window(self):
        self.create_dialog("Withdraw", self.withdraw_logic, include_balance=False)

    def withdraw_logic(self, account_holder, account_number, amount):
        account = self.accounts.get(account_number)
        if account:
            if account.withdraw(amount):
                messagebox.showinfo("Success", f"${amount} withdrawn successfully.")
            else:
                messagebox.showwarning("Error", "Insufficient funds or invalid amount.")
        else:
            messagebox.showwarning("Error", "Account not found.")

    def check_balance_window(self):
        self.create_dialog("Check Balance", self.check_balance_logic, include_balance=False)

    def check_balance_logic(self, account_holder, account_number, amount):
        account = self.accounts.get(account_number)
        if account:
            messagebox.showinfo("Balance", f"Account Holder: {account.account_holder}\nBalance: ${account.balance}")
        else:
            messagebox.showwarning("Error", "Account not found.")

    def create_dialog(self, title, logic_callback, include_balance):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x250")

        bg_image = ImageTk.PhotoImage(Image.open('bankapp.jpg'))
        bg_label = tk.Label(dialog, image=bg_image)
        bg_label.image = bg_image
        bg_label.place(relwidth=1, relheight=1)

        tk.Label(dialog, text="Account Holder", bg='#DD4F05', fg='white').pack(pady=5)
        account_holder_entry = tk.Entry(dialog)
        account_holder_entry.pack()

        tk.Label(dialog, text="Account Number", bg='#DD4F05', fg='white').pack(pady=5)
        account_number_entry = tk.Entry(dialog)
        account_number_entry.pack()

        if include_balance:
            tk.Label(dialog, text="Initial Balance / Amount", bg='#DD4F05', fg='white').pack(pady=5)
        else:
            tk.Label(dialog, text="Amount", bg='#DD4F05', fg='white').pack(pady=5)
        amount_entry = tk.Entry(dialog)
        amount_entry.pack()
        dialog.resizable(0,0)

        def on_submit():
            try:
                account_holder = account_holder_entry.get()
                account_number = int(account_number_entry.get()) if account_number_entry.get() else None
                amount = float(amount_entry.get()) if amount_entry.get() else None
                logic_callback(account_holder, account_number, amount)
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers.")

        tk.Button(dialog, text="Submit", command=on_submit).pack(pady=10)
        tk.Button(dialog, text="Cancel", command=dialog.destroy).pack(pady=5)

    def enable_buttons(self):
        self.deposit_button["state"] = tk.NORMAL
        self.withdraw_button["state"] = tk.NORMAL
        self.check_balance_button["state"] = tk.NORMAL


if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.geometry("500x400")
    root.resizable(0, 0)
    root.mainloop()
