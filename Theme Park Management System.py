#!/usr/bin/env python
# coding: utf-8

# In[32]:


import tkinter as tk
from tkinter import messagebox, ttk
import pickle
import os
import datetime


# User Class
class User:
    def __init__(self, user_id, name, email, password):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.password = password
        self.bought_tickets = []  # Track bought tickets


# System Class
class System:
    def __init__(self):
        self.users = []
        self.admin_credentials = {"admin": "admin123"}  # Fixed admin credentials
        self.ticket_sales = {}  # To track total tickets sold per day
        self.discount_info = {}  # To store discount information

    def load_data(self):
        try:
            with open('data/users.pkl', 'rb') as f:
                self.users = pickle.load(f)
        except FileNotFoundError:
            pass

        try:
            with open('data/ticket_sales.pkl', 'rb') as f:
                self.ticket_sales = pickle.load(f)
        except FileNotFoundError:
            pass

        try:
            with open('data/discount_info.pkl', 'rb') as f:
                self.discount_info = pickle.load(f)
        except FileNotFoundError:
            pass

    def store_data(self):
        # Ensure the data directory exists
        if not os.path.exists('data'):
            os.makedirs('data')
        
        with open('data/users.pkl', 'wb') as f:
            pickle.dump(self.users, f)

        with open('data/ticket_sales.pkl', 'wb') as f:
            pickle.dump(self.ticket_sales, f)

        with open('data/discount_info.pkl', 'wb') as f:
            pickle.dump(self.discount_info, f)

    def create_user(self, name, email, password):
        if any(user.email == email for user in self.users):
            return False, "Email already exists!"
        user_id = len(self.users) + 1
        new_user = User(user_id, name, email, password)
        self.users.append(new_user)
        self.store_data()
        return True, "Account created successfully!"

    def validate_user_login(self, email, password):
        user = next((u for u in self.users if u.email == email and u.password == password), None)
        if user:
            return True, user
        return False, None

    def modify_user(self, user, name, email, password):
        if any(u.email == email and u.user_id != user.user_id for u in self.users):
            return False, "Email already exists!"
        user.name = name
        user.email = email
        user.password = password
        self.store_data()
        return True, "Account modified successfully!"

    def delete_user(self, user):
        self.users.remove(user)
        self.store_data()
        return True, "Account deleted successfully!"

    def update_ticket_sales(self, date, num_tickets):
        if date in self.ticket_sales:
            self.ticket_sales[date] += num_tickets
        else:
            self.ticket_sales[date] = num_tickets
        self.store_data()

    def get_ticket_sales(self, date):
        return self.ticket_sales.get(date, 0)

    def set_discount(self, ticket_type, discount_percentage):
        self.discount_info[ticket_type] = discount_percentage
        self.store_data()

    def get_discount(self, ticket_type):
        return self.discount_info.get(ticket_type, 0)


# Ticket Information
ticket_types = [
    ("Single-Day Pass", "Access to the park for one day", 275, "1 Day", "None", "Valid only on selected date"),
    ("Two-Day Pass", "Access to the park for two consecutive days", 480, "2 Days", "10% discount for online purchase", "Cannot be split over multiple trips"),
    ("Annual Membership", "Unlimited access for one year", 1840, "1 Year", "15% discount on renewal", "Must be used by the same person"),
    ("Child Ticket", "Discounted ticket for children (ages 3-12)", 185, "1 Day", "None", "Valid only on selected date must be accompanied by an adult"),
    ("Group Ticket (10+)", "Special rate for groups of 10 or more", 220, "1 Day", "20% off for groups of 20 or more", "Must be booked in advance"),
    ("VIP Experience Pass", "Includes expedited access and reserved seating for shows", 550, "1 Day", "None", "Limited availability must be purchased in advance")
]


# Tkinter GUI Implementation
def main_screen(system):
    def create_account_screen():
        def create_account():
            name = name_entry.get()
            email = email_entry.get()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()

            # Input validation
            if not name or not email or not password:
                messagebox.showerror("Error", "All fields are required!")
                return
            if password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match!")
                return
            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "Invalid email format!")
                return

            success, message = system.create_user(name, email, password)
            if success:
                messagebox.showinfo("Success", message)
                create_window.destroy()
               
            else:
                messagebox.showerror("Error", message)

        create_window = tk.Toplevel(root)
        create_window.title("Create Account")
        create_window.geometry("400x400")
        create_window.configure(bg="#f0f4f7")

        tk.Label(create_window, text="Create Account", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)

        tk.Label(create_window, text="Name:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        name_entry = tk.Entry(create_window, width=30)
        name_entry.pack()

        tk.Label(create_window, text="Email:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        email_entry = tk.Entry(create_window, width=30)
        email_entry.pack()

        tk.Label(create_window, text="Password:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        password_entry = tk.Entry(create_window, show="*", width=30)
        password_entry.pack()

        tk.Label(create_window, text="Confirm Password:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        confirm_password_entry = tk.Entry(create_window, show="*", width=30)
        confirm_password_entry.pack()

        tk.Button(create_window, text="Create Account", bg="#4CAF50", fg="white", font=("Arial", 12), 
                  command=create_account).pack(pady=15)

    def user_login_screen():
        def validate_login():
            email = email_entry.get()
            password = password_entry.get()
            success, user = system.validate_user_login(email, password)
            if success:
                messagebox.showinfo("Success", f"Welcome, {user.name}!")
                login_window.destroy()
                user_dashboard(user)
            else:
                messagebox.showerror("Error", "Invalid email or password!")

        login_window = tk.Toplevel(root)
        login_window.title("User Login")
        login_window.geometry("400x300")
        login_window.configure(bg="#f0f4f7")

        tk.Label(login_window, text="User Login", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)

        tk.Label(login_window, text="Email:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        email_entry = tk.Entry(login_window, width=30)
        email_entry.pack()

        tk.Label(login_window, text="Password:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        password_entry = tk.Entry(login_window, show="*", width=30)
        password_entry.pack()

        tk.Button(login_window, text="Login", bg="#2196F3", fg="white", font=("Arial", 12), 
                  command=validate_login).pack(pady=15)

    def admin_login_screen():
        def validate_admin_login():
            username = username_entry.get()
            password = password_entry.get()
            if username in system.admin_credentials and system.admin_credentials[username] == password:
                messagebox.showinfo("Success", "Welcome, Admin!")
                admin_window.destroy()
                admin_dashboard()
            else:
                messagebox.showerror("Error", "Invalid admin credentials!")

        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Login")
        admin_window.geometry("400x300")
        admin_window.configure(bg="#f0f4f7")

        tk.Label(admin_window, text="Admin Login", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)

        tk.Label(admin_window, text="Username:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        username_entry = tk.Entry(admin_window, width=30)
        username_entry.pack()

        tk.Label(admin_window, text="Password:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        password_entry = tk.Entry(admin_window, show="*", width=30)
        password_entry.pack()

        tk.Button(admin_window, text="Login", bg="#FF5722", fg="white", font=("Arial", 12), 
                  command=validate_admin_login).pack(pady=15)

    def manage_tickets_screen(user):
        def buy_ticket():
            def calculate_price():
                ticket_type = ticket_type_combobox.get()
                num_people = num_people_entry.get()
                visit_date = visit_date_entry.get()
                payment_method = payment_method_var.get()

                # Input validation
                if not visit_date or not ticket_type or not num_people or not payment_method:
                    messagebox.showerror("Error", "All fields are required!")
                    return

                try:
                    num_people = int(num_people)
                    if num_people <= 0:
                        messagebox.showerror("Error", "Number of people must be greater than zero!")
                        return
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid number for people!")
                    return

                # Check if visit date format is MM/DD/YYYY
                try:
                    datetime.datetime.strptime(visit_date, "%m/%d/%Y")
                except ValueError:
                    messagebox.showerror("Error", "Invalid date format! Please use MM/DD/YYYY.")
                    return

                # Find ticket details
                ticket_info = next(t for t in ticket_types if t[0] == ticket_type)
                price_per_ticket = ticket_info[2]

                # Apply discount
                discount = system.get_discount(ticket_type)
                total_price = price_per_ticket * num_people * (1 - discount / 100)

                # Process payment based on selected method
                if payment_method == "Credit Card":
                    validate_credit_card_payment(total_price)
                elif payment_method == "PayPal":
                    validate_paypal_payment(total_price)
                else:
                    messagebox.showerror("Error", "Invalid payment method selected.")

            def validate_credit_card_payment(total_price):
                card_number = card_number_entry.get()
                expiry_date = expiry_date_entry.get()
                cvv = cvv_entry.get()

                # Credit Card Validation
                if len(card_number) != 16 or not card_number.isdigit():
                    messagebox.showerror("Error", "Card number must be 16 digits.")
                    return
                try:
                    datetime.datetime.strptime(expiry_date, "%m/%y")
                except ValueError:
                    messagebox.showerror("Error", "Expiry date must be in MM/YY format.")
                    return
                if len(cvv) != 3 or not cvv.isdigit():
                    messagebox.showerror("Error", "CVV must be 3 digits.")
                    return
                
                # If validation is successful
                messagebox.showinfo("Success", f"Payment of {total_price:.2f} USD via Credit Card was successful!")
                ticket_window.destroy()

            def validate_paypal_payment(total_price):
                paypal_email = paypal_email_entry.get()
                paypal_password = paypal_password_entry.get()

                if "@" not in paypal_email or "." not in paypal_email:
                    messagebox.showerror("Error", "Invalid PayPal email format!")
                    return
                if not paypal_password:
                    messagebox.showerror("Error", "PayPal password cannot be empty!")
                    return

                # If validation is successful
                messagebox.showinfo("Success", f"Payment of {total_price:.2f} USD via PayPal was successful!")
                ticket_window.destroy()

            ticket_window = tk.Toplevel(root)
            ticket_window.title("Manage Tickets")
            ticket_window.geometry("400x500")
            ticket_window.configure(bg="#f0f4f7")

            tk.Label(ticket_window, text="Manage Tickets", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)

            tk.Label(ticket_window, text="Ticket Type:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            ticket_type_combobox = ttk.Combobox(ticket_window, values=[t[0] for t in ticket_types])
            ticket_type_combobox.pack()

            tk.Label(ticket_window, text="Number of People:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            num_people_entry = tk.Entry(ticket_window)
            num_people_entry.pack()

            tk.Label(ticket_window, text="Visit Date (MM/DD/YYYY):", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            visit_date_entry = tk.Entry(ticket_window)
            visit_date_entry.pack()

            tk.Label(ticket_window, text="Payment Method:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            payment_method_var = tk.StringVar()
            ttk.Radiobutton(ticket_window, text="Credit Card", variable=payment_method_var, value="Credit Card").pack()
            ttk.Radiobutton(ticket_window, text="PayPal", variable=payment_method_var, value="PayPal").pack()

            # Credit Card Payment Details
            tk.Label(ticket_window, text="Card Number (16 digits):", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            card_number_entry = tk.Entry(ticket_window, width=30)
            card_number_entry.pack()

            tk.Label(ticket_window, text="Expiry Date (MM/YY):", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            expiry_date_entry = tk.Entry(ticket_window, width=30)
            expiry_date_entry.pack()

            tk.Label(ticket_window, text="CVV (3 digits):", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            cvv_entry = tk.Entry(ticket_window, width=30, show="*")
            cvv_entry.pack()

            # PayPal Payment Details
            tk.Label(ticket_window, text="PayPal Email:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            paypal_email_entry = tk.Entry(ticket_window, width=30)
            paypal_email_entry.pack()

            tk.Label(ticket_window, text="PayPal Password:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
            paypal_password_entry = tk.Entry(ticket_window, width=30, show="*")
            paypal_password_entry.pack()

            tk.Button(ticket_window, text="Purchase Tickets", bg="#4CAF50", fg="white", font=("Arial", 12), 
                      command=calculate_price).pack(pady=15)

        manage_window = tk.Toplevel(root)
        manage_window.title("Manage Tickets")
        manage_window.geometry("400x300")
        manage_window.configure(bg="#f0f4f7")

        tk.Label(manage_window, text="Manage Tickets", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)

        tk.Button(manage_window, text="Buy Ticket", bg="#4CAF50", fg="white", font=("Arial", 12), 
                  command=buy_ticket).pack(pady=20)

    def user_dashboard(user):
        def account_management():
            def view_account_details():
                view_window = tk.Toplevel(dashboard)
                view_window.title("View Account Details")
                view_window.geometry("400x300")
                view_window.configure(bg="#f0f4f7")
                
                tk.Label(view_window, text="Account Details", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)
                tk.Label(view_window, text=f"Name: {user.name}", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
                tk.Label(view_window, text=f"Email: {user.email}", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
                tk.Label(view_window, text=f"Password: {user.password}", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)

            def modify_account():
                def modify():
                    new_name = name_entry.get()
                    new_email = email_entry.get()
                    new_password = password_entry.get()
                    success, message = system.modify_user(user, new_name, new_email, new_password)
                    if success:
                        messagebox.showinfo("Success", message)
                        modify_window.destroy()
                    else:
                        messagebox.showerror("Error", message)

                modify_window = tk.Toplevel(dashboard)
                modify_window.title("Modify Account")
                modify_window.geometry("400x400")
                modify_window.configure(bg="#f0f4f7")

                tk.Label(modify_window, text="Modify Account", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)
                
                tk.Label(modify_window, text="New Name:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
                name_entry = tk.Entry(modify_window, width=30)
                name_entry.insert(0, user.name)
                name_entry.pack()

                tk.Label(modify_window, text="New Email:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
                email_entry = tk.Entry(modify_window, width=30)
                email_entry.insert(0, user.email)
                email_entry.pack()

                tk.Label(modify_window, text="New Password:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
                password_entry = tk.Entry(modify_window, show="*", width=30)
                password_entry.insert(0, user.password)
                password_entry.pack()

                tk.Button(modify_window, text="Modify Account", bg="#4CAF50", fg="white", font=("Arial", 12), 
                          command=modify).pack(pady=15)

            def delete_account():
                confirm = messagebox.askyesno("Delete Account", "Are you sure you want to delete your account?")
                if confirm:
                    success, message = system.delete_user(user)
                    if success:
                        messagebox.showinfo("Success", message)
                        dashboard.destroy()  # Destroy the current dashboard window
                        main_screen(system)  # Call the main screen function to show the main screen


            dashboard = tk.Toplevel()
            dashboard.title(f"Welcome {user.name}")
            dashboard.geometry("500x400")
            dashboard.configure(bg="#ffffff")

            tk.Button(dashboard, text="View Account Details", bg="#4CAF50", fg="white", font=("Arial", 12), 
                      command=view_account_details).pack(pady=10)
            tk.Button(dashboard, text="Modify Account", bg="#2196F3", fg="white", font=("Arial", 12), 
                      command=modify_account).pack(pady=10)
            tk.Button(dashboard, text="Delete Account", bg="#FF5722", fg="white", font=("Arial", 12), 
                      command=delete_account).pack(pady=10)

        dashboard = tk.Tk()
        dashboard.title(f"Welcome {user.name}")
        dashboard.geometry("500x400")
        dashboard.configure(bg="#ffffff")

        tk.Label(dashboard, text="User Dashboard", font=("Arial", 18), bg="#ffffff").pack(pady=20)

        tk.Button(dashboard, text="Account Management", bg="#2196F3", fg="white", font=("Arial", 12), 
                  command=account_management).pack(pady=10)

        tk.Button(dashboard, text="Manage Tickets", bg="#4CAF50", fg="white", font=("Arial", 12), 
                  command=lambda: manage_tickets_screen(user)).pack(pady=20)

    def admin_dashboard():
        def view_ticket_sales():
            date = date_entry.get()
            if date:
                sales = system.get_ticket_sales(date)
                messagebox.showinfo("Ticket Sales", f"Total tickets sold on {date}: {sales}")
            else:
                messagebox.showerror("Error", "Please enter a valid date.")

        def update_discount():
            ticket_type = ticket_type_combobox.get()
            discount_percentage = discount_entry.get()
            if ticket_type and discount_percentage:
                try:
                    discount_percentage = float(discount_percentage)
                    system.set_discount(ticket_type, discount_percentage)
                    messagebox.showinfo("Success", f"Discount for {ticket_type} updated to {discount_percentage}%")
                except ValueError:
                    messagebox.showerror("Error", "Invalid discount value.")
            else:
                messagebox.showerror("Error", "Please fill out all fields.")

        admin_window = tk.Toplevel(root)
        admin_window.title("Admin Dashboard")
        admin_window.geometry("400x400")
        admin_window.configure(bg="#f0f4f7")

        tk.Label(admin_window, text="Admin Dashboard", font=("Arial", 16), bg="#f0f4f7").pack(pady=10)

        # View Ticket Sales
        tk.Label(admin_window, text="View Ticket Sales (Date: MM/DD/YYYY):", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        date_entry = tk.Entry(admin_window, width=30)
        date_entry.pack()
        tk.Button(admin_window, text="View Sales", bg="#4CAF50", fg="white", font=("Arial", 12), 
                  command=view_ticket_sales).pack(pady=10)

        # Update Discount
        tk.Label(admin_window, text="Update Discount for Ticket Type:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        ticket_type_combobox = ttk.Combobox(admin_window, values=[t[0] for t in ticket_types])
        ticket_type_combobox.pack()
        tk.Label(admin_window, text="Discount Percentage:", font=("Arial", 12), bg="#f0f4f7").pack(pady=5)
        discount_entry = tk.Entry(admin_window, width=30)
        discount_entry.pack()
        tk.Button(admin_window, text="Update Discount", bg="#4CAF50", fg="white", font=("Arial", 12), 
                  command=update_discount).pack(pady=10)

    root = tk.Tk()
    root.title("Theme Park Management System")
    root.geometry("600x400")
    root.configure(bg="#f0f4f7")

    tk.Label(root, text="Theme Park Management System", font=("Arial", 20), bg="#f0f4f7").pack(pady=20)

    tk.Button(root, text="Create Account", bg="#4CAF50", fg="white", font=("Arial", 12), command=create_account_screen).pack(pady=10)
    tk.Button(root, text="User Login", bg="#2196F3", fg="white", font=("Arial", 12), command=user_login_screen).pack(pady=10)
    tk.Button(root, text="Admin Login", bg="#FF5722", fg="white", font=("Arial", 12), command=admin_login_screen).pack(pady=10)

    root.mainloop()


# Initialize System
system = System()
system.load_data()
main_screen(system)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




