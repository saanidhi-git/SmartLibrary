# Note: Revised to remove image upload and enable directed application system.

import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import TkinterDnD
import os
import json
from datetime import date, timedelta
import matplotlib.pyplot as plt

BOOK_FILE = "books.json"
APP_FILE = "applications.json"

staff_data = {
    "LIB_LD": {"name": "Mrs Lily D'souza", "password": "libLD", "post": "Librarian"},
    "LIB_RS": {"name": "Mr RamSingh Shekhar", "password": "libRS", "post": "Co-Librarian (Accountant)"},
}

books = json.load(open(BOOK_FILE)) if os.path.exists(BOOK_FILE) else {}
applications = json.load(open(APP_FILE)) if os.path.exists(APP_FILE) else []

def save_books():
    with open(BOOK_FILE, "w") as f:
        json.dump(books, f, indent=4)

def save_apps():
    with open(APP_FILE, "w") as f:
        json.dump(applications, f, indent=4)

def show_analytics():
    issued_books = [b['issued_to'] for b in books.values() if b['issued_to']]
    student_counts = {}
    for sid in issued_books:
        student_counts[sid] = student_counts.get(sid, 0) + 1

    plt.figure(figsize=(7, 4))
    plt.bar(student_counts.keys(), student_counts.values(), color='green')
    plt.title("Defaulter Students (Issued Books Count)")
    plt.xlabel("Student ID")
    plt.ylabel("Books Issued")
    plt.grid(axis='y', linestyle='--')
    plt.show()

    title_counts = {}
    for title in books:
        count = title_counts.get(title, 0)
        if books[title]['issued_to']:
            title_counts[title] = count + 1
    plt.figure(figsize=(7, 4))
    plt.bar(title_counts.keys(), title_counts.values(), color='darkgreen')
    plt.title("Most Read Books")
    plt.xticks(rotation=45)
    plt.ylabel("Issue Frequency")
    plt.tight_layout()
    plt.grid(axis='y', linestyle='--')
    plt.show()

def book_status(title):
    if books[title]['issued_to']:
        return f"Issued to {books[title]['issued_to']} till {books[title]['return_date']}"
    return "Available"

def open_add_remove(parent):
    def save_details():
        title = entry_title.get()
        if not title:
            messagebox.showwarning("Required", "Book title required")
            return
        books[title] = {
            "book_id": entry_id.get(), "category": entry_cat.get(), "author": entry_author.get(),
            "quality": entry_quality.get(), "image": None,
            "issued_to": None, "issue_date": None, "return_date": None
        }
        save_books()
        messagebox.showinfo("Saved", f"Book '{title}' saved!")

    def remove():
        title = entry_title.get()
        if title in books:
            del books[title]
            save_books()
            messagebox.showinfo("Removed", f"Book '{title}' deleted!")

    win = tk.Toplevel(parent)
    win.title("Add/Remove Book")
    win.geometry("500x500")
    win.configure(bg="#1e2f1e")

    tk.Label(win, text="Book Entry", font=("Arial", 16), bg="#1e2f1e", fg="lightgreen").pack(pady=10)

    def add_field(lbl):
        tk.Label(win, text=lbl, bg="#1e2f1e", fg="white", anchor="w").pack()
        ent = tk.Entry(win, width=40, bg="#283d28", fg="white", insertbackground='white')
        ent.pack(pady=3)
        return ent

    entry_title = add_field("Book Title")
    entry_id = add_field("Book ID")
    entry_cat = add_field("Category")
    entry_author = add_field("Author")
    entry_quality = add_field("Quality (1-5)")

    tk.Button(win, text="Save Details", command=save_details, bg="darkgreen", fg="white").pack(pady=5)
    tk.Button(win, text="Remove Book", command=remove, bg="red", fg="white").pack(pady=5)

def write_application(parent, sender_id):
    def submit():
        recipient_id = entry_to.get().strip()
        msg = txt.get("1.0", tk.END).strip()
        if recipient_id in staff_data and msg:
            applications.append({
                "from": sender_id,
                "to": recipient_id,
                "message": msg,
                "date": str(date.today())
            })
            save_apps()
            messagebox.showinfo("Sent", f"Application sent to {staff_data[recipient_id]['name']}.")
            win.destroy()
        else:
            messagebox.showerror("Error", "Invalid recipient ID or message empty.")

    win = tk.Toplevel(parent)
    win.title("Write Application")
    win.geometry("400x350")
    win.configure(bg="#1e2f1e")

    tk.Label(win, text="To (Staff ID):", fg="white", bg="#1e2f1e").pack(pady=5)
    entry_to = tk.Entry(win, width=30)
    entry_to.pack(pady=5)

    tk.Label(win, text="Application Message:", fg="white", bg="#1e2f1e").pack()
    txt = tk.Text(win, height=10, width=40)
    txt.pack(pady=10)
    tk.Button(win, text="Submit", command=submit, bg="darkgreen", fg="white").pack()

def view_applications(parent, viewer_id):
    win = tk.Toplevel(parent)
    win.title("Applications")
    win.geometry("500x300")
    win.configure(bg="#1e2f1e")
    for app in applications:
        if app['to'] == viewer_id:
            tk.Label(win, text=f"From {app['from']} on {app['date']}\n{app['message']}", wraplength=480, justify="left",
                     fg="lightgreen", bg="#1e2f1e").pack(anchor='w', padx=10, pady=5)

def load_dashboard(staff_id):
    user = staff_data[staff_id]
    dash = tk.Toplevel()
    dash.title("Dashboard")
    dash.geometry("600x600")
    dash.configure(bg="#1e2f1e")

    tk.Label(dash, text=f"Welcome {user['name']}", font=("Arial", 14, "bold"), bg="#1e2f1e", fg="lightgreen").pack(pady=10)

    tk.Button(dash, text="Add/Remove Book", width=25, bg="darkgreen", fg="white", command=lambda: open_add_remove(dash)).pack(pady=5)
    tk.Button(dash, text="Book Status", width=25, bg="darkgreen", fg="white", command=lambda: view_books(dash)).pack(pady=5)
    tk.Button(dash, text="Analytics", width=25, bg="darkgreen", fg="white", command=show_analytics).pack(pady=5)
    tk.Button(dash, text="Write Application", width=25, bg="darkgreen", fg="white", command=lambda: write_application(dash, staff_id)).pack(pady=5)
    if staff_id == "LIB_LD":
        tk.Button(dash, text="View Applications", width=25, bg="darkgreen", fg="white", command=lambda: view_applications(dash, staff_id)).pack(pady=5)
    if staff_id == "LIB_RS":
        tk.Button(dash, text="Assign Book", width=25, bg="darkgreen", fg="white", command=lambda: assign_book_to_student(dash)).pack(pady=5)
        tk.Button(dash, text="Return Book", width=25, bg="darkgreen", fg="white", command=lambda: return_book(dash)).pack(pady=5)

    tk.Button(dash, text="Exit", width=25, bg="red", fg="white", command=dash.destroy).pack(pady=20)

def view_books(parent):
    win = tk.Toplevel(parent)
    win.title("Books Status")
    win.geometry("600x400")
    win.configure(bg="#1e2f1e")
    for title, data in books.items():
        status = book_status(title)
        tk.Label(win, text=f"{title} | ID: {data['book_id']} | {status}", fg="lightgreen", bg="#1e2f1e").pack(anchor="w")

def assign_book_to_student(parent):
    def assign():
        title = entry_title.get()
        student_id = entry_student.get()
        if title in books and books[title]['issued_to'] is None:
            books[title]['issued_to'] = student_id
            books[title]['issue_date'] = str(date.today())
            books[title]['return_date'] = str(date.today() + timedelta(days=7))
            save_books()
            messagebox.showinfo("Assigned", f"Book '{title}' assigned to {student_id}")
            win.destroy()
        else:
            messagebox.showerror("Error", "Book not found or already issued")

    win = tk.Toplevel(parent)
    win.title("Assign Book")
    win.geometry("400x250")
    win.configure(bg="#1e2f1e")
    entry_title = tk.Entry(win, width=30)
    entry_student = tk.Entry(win, width=30)
    tk.Label(win, text="Book Title:", bg="#1e2f1e", fg="white").pack()
    entry_title.pack(pady=5)
    tk.Label(win, text="Student ID:", bg="#1e2f1e", fg="white").pack()
    entry_student.pack(pady=5)
    tk.Button(win, text="Assign", command=assign, bg="darkgreen", fg="white").pack(pady=10)

def return_book(parent):
    def process_return():
        title = entry_title.get()
        if title in books and books[title]['issued_to']:
            books[title]['return_date'] = str(date.today())
            books[title]['issued_to'] = None
            books[title]['issue_date'] = None
            save_books()
            messagebox.showinfo("Returned", f"Book '{title}' returned")
            win.destroy()
        else:
            messagebox.showerror("Error", "Book not found or not issued")

    win = tk.Toplevel(parent)
    win.title("Return Book")
    win.geometry("400x200")
    win.configure(bg="#1e2f1e")
    entry_title = tk.Entry(win, width=30)
    tk.Label(win, text="Book Title:", bg="#1e2f1e", fg="white").pack()
    entry_title.pack(pady=5)
    tk.Button(win, text="Return", command=process_return, bg="darkgreen", fg="white").pack(pady=10)

def start_login():
    def login():
        staff_id = entry_id.get().strip()
        password = entry_pw.get().strip()
        if staff_id in staff_data and staff_data[staff_id]["password"] == password:
            messagebox.showinfo("Login Success", f"Welcome {staff_data[staff_id]['name']}")
            root.destroy()
            load_dashboard(staff_id)
        else:
            messagebox.showerror("Login Failed", "Invalid ID or Password.")

    global root
    root = TkinterDnD.Tk()
    root.title("Librarian Login")
    root.geometry("400x300")
    root.configure(bg="#1e2f1e")

    tk.Label(root, text="Library Staff Login", font=("Helvetica", 18, "bold"), bg="#1e2f1e", fg="lightgreen").pack(pady=20)
    tk.Label(root, text="Staff ID:", font=("Arial", 12), bg="#1e2f1e", fg="white").pack()
    entry_id = tk.Entry(root, font=("Arial", 12), bg="#283d28", fg="white")
    entry_id.pack(pady=5)
    tk.Label(root, text="Password:", font=("Arial", 12), bg="#1e2f1e", fg="white").pack()
    entry_pw = tk.Entry(root, font=("Arial", 12), show="*", bg="#283d28", fg="white")
    entry_pw.pack(pady=5)
    tk.Button(root, text="Login", font=("Arial", 12), bg="darkgreen", fg="white", command=login).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    start_login()
