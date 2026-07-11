# ====================== PERSONAL CONTACT MANAGER =============================

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import datetime

# ====================== VARIABLES ===============================

contacts_list = []       
selected_index = -1      
file_name = "contacts.json"


name_var = None
phone_var = None
email_var = None
address_var = None
search_var = None
status_var = None

# widgets
contact_listbox = None


# ========================= FILE HANDLING ===========================

def load_contacts():
    global contacts_list

    if not os.path.exists(file_name):
        contacts_list = []
        return

    try:
        with open(file_name, "r") as file:
            data = json.load(file)
            contacts_list = data.get("contacts", [])
    except Exception as e:
        print("Error loading file:", e)
        contacts_list = []


def save_contacts():
    try:
        data = {"contacts": contacts_list}
        with open(file_name, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        print("Error saving file:", e)


# =============================== CREATING BACKEND FUNCTIONS ==============================

def update_status(message):
    time_now = datetime.datetime.now().strftime("%H:%M:%S")
    status_var.set(f"[{time_now}] {message}")


def clear_fields():
    name_var.set("")
    phone_var.set("")
    email_var.set("")
    address_var.set("")


def get_form_data():
    return {
        "name": name_var.get().strip(),
        "phone": phone_var.get().strip(),
        "email": email_var.get().strip(),
        "address": address_var.get().strip()
    }


def set_form_data(contact):
    name_var.set(contact.get("name", ""))
    phone_var.set(contact.get("phone", ""))
    email_var.set(contact.get("email", ""))
    address_var.set(contact.get("address", ""))


def validate_input():
    data = get_form_data()

    
    if data["name"] == "":
        messagebox.showerror("Error", "Name is required")
        return False

    
    if data["phone"] == "":
        messagebox.showerror("Error", "Phone is required")
        return False

    if not data["phone"].isdigit():
        messagebox.showerror("Error", "Phone must contain only digits")
        return False

    if len(data["phone"]) != 10:
        messagebox.showerror("Error", "Phone must be 10 digits")
        return False


    for i, contact in enumerate(contacts_list):
        if contact["phone"] == data["phone"] and i != selected_index:
            messagebox.showerror("Error", "Duplicate phone number")
            return False

    
    if data["email"]:
        if "@" not in data["email"] or "." not in data["email"]:
            messagebox.showerror("Error", "Invalid email format")
            return False

    return True



def refresh_listbox():
    contact_listbox.delete(0, tk.END)

    for contact in contacts_list:
        text = f"{contact['name']} - {contact['phone']}"
        contact_listbox.insert(tk.END, text)

    update_status(f"Total Contacts: {len(contacts_list)}")


def on_select_contact(event):
    global selected_index

    try:
        index = contact_listbox.curselection()[0]
        selected_index = index
        contact = contacts_list[index]
        set_form_data(contact)
        update_status(f"Selected: {contact['name']}")
    except:
        pass


def clear_selection():
    global selected_index
    selected_index = -1
    contact_listbox.selection_clear(0, tk.END)



def add_contact():
    if not validate_input():
        return

    data = get_form_data()

    contacts_list.append(data)
    save_contacts()
    refresh_listbox()
    clear_fields()

    update_status("Contact added successfully")


def update_contact():
    global selected_index

    if selected_index == -1:
        messagebox.showerror("Error", "Please select a contact")
        return

    if not validate_input():
        return

    contacts_list[selected_index] = get_form_data()
    save_contacts()
    refresh_listbox()
    clear_fields()
    clear_selection()

    update_status("Contact updated")


def delete_contact():
    global selected_index

    if selected_index == -1:
        messagebox.showerror("Error", "Select a contact first")
        return

    confirm = messagebox.askyesno("Confirm", "Are you sure?")
    if not confirm:
        return

    contacts_list.pop(selected_index)
    save_contacts()
    refresh_listbox()
    clear_fields()
    clear_selection()

    update_status("Contact deleted")


def search_contacts():
    text = search_var.get().strip().lower()

    contact_listbox.delete(0, tk.END)

    for contact in contacts_list:
        name_match = text in contact["name"].lower()
        phone_match = text in contact["phone"]

        if name_match or phone_match:
            display = f"{contact['name']} - {contact['phone']}"
            contact_listbox.insert(tk.END, display)

    update_status("Search completed")


def show_all_contacts():
    refresh_listbox()
    update_status("Showing all contacts")


def sort_contacts_by_name():
    contacts_list.sort(key=lambda x: x["name"].lower())
    refresh_listbox()
    update_status("Sorted by name")


def sort_contacts_by_phone():
    contacts_list.sort(key=lambda x: x["phone"])
    refresh_listbox()
    update_status("Sorted by phone")


def count_contacts():
    total = len(contacts_list)
    messagebox.showinfo("Info", f"Total Contacts: {total}")


def export_contacts():
    try:
        with open("backup_contacts.json", "w") as file:
            json.dump({"contacts": contacts_list}, file, indent=4)
        messagebox.showinfo("Success", "Backup created")
    except:
        messagebox.showerror("Error", "Failed to export")


def clear_all_contacts():
    confirm = messagebox.askyesno("Warning", "Delete ALL contacts?")
    if confirm:
        contacts_list.clear()
        save_contacts()
        refresh_listbox()
        update_status("All contacts cleared")

# ============================================= CREATING FRONTEND ================================================

def create_main_window():
    global name_var, phone_var, email_var, address_var
    global search_var, status_var, contact_listbox

    root = tk.Tk()
    root.title("Contact Manager ")
    root.geometry("700x600")

   
    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    address_var = tk.StringVar()
    search_var = tk.StringVar()
    status_var = tk.StringVar()

    
    frame_list = ttk.LabelFrame(root, text="Contacts")
    frame_list.pack(fill="both", padx=10, pady=5)

    contact_listbox = tk.Listbox(frame_list, height=10)
    contact_listbox.pack(side=tk.LEFT, fill="both", expand=True)
    contact_listbox.bind("<<ListboxSelect>>", on_select_contact)

    scrollbar = ttk.Scrollbar(frame_list, command=contact_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    contact_listbox.config(yscrollcommand=scrollbar.set)

    
    frame_search = ttk.Frame(root)
    frame_search.pack(fill="x", padx=10)

    ttk.Entry(frame_search, textvariable=search_var).pack(side=tk.LEFT, padx=5)
    ttk.Button(frame_search, text="Search", command=search_contacts).pack(side=tk.LEFT)
    ttk.Button(frame_search, text="Show All", command=show_all_contacts).pack(side=tk.LEFT)

   
    frame_details = ttk.LabelFrame(root, text="Details")
    frame_details.pack(fill="x", padx=10, pady=5)

    ttk.Label(frame_details, text="Name").grid(row=0, column=0)
    ttk.Entry(frame_details, textvariable=name_var, width=40).grid(row=0, column=1)

    ttk.Label(frame_details, text="Phone").grid(row=1, column=0)
    ttk.Entry(frame_details, textvariable=phone_var, width=40).grid(row=1, column=1)

    ttk.Label(frame_details, text="Email").grid(row=2, column=0)
    ttk.Entry(frame_details, textvariable=email_var, width=40).grid(row=2, column=1)

    ttk.Label(frame_details, text="Address").grid(row=3, column=0)
    ttk.Entry(frame_details, textvariable=address_var, width=40).grid(row=3, column=1)

    
    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(pady=10)

    ttk.Button(frame_buttons, text="Add", command=add_contact).grid(row=0, column=0, padx=5)
    ttk.Button(frame_buttons, text="Update", command=update_contact).grid(row=0, column=1, padx=5)
    ttk.Button(frame_buttons, text="Delete", command=delete_contact).grid(row=0, column=2, padx=5)
    ttk.Button(frame_buttons, text="Clear", command=clear_fields).grid(row=0, column=3, padx=5)
    ttk.Button(frame_buttons, text="Exit", command=root.quit).grid(row=0, column=4, padx=5)


    frame_extra = ttk.Frame(root)
    frame_extra.pack(pady=5)

    ttk.Button(frame_extra, text="Sort Name", command=sort_contacts_by_name).grid(row=0, column=0, padx=5)
    ttk.Button(frame_extra, text="Sort Phone", command=sort_contacts_by_phone).grid(row=0, column=1, padx=5)
    ttk.Button(frame_extra, text="Count", command=count_contacts).grid(row=0, column=2, padx=5)
    ttk.Button(frame_extra, text="Backup", command=export_contacts).grid(row=0, column=3, padx=5)
    ttk.Button(frame_extra, text="Clear All", command=clear_all_contacts).grid(row=0, column=4, padx=5)

    
    status_label = ttk.Label(root, textvariable=status_var, relief="sunken")
    status_label.pack(side=tk.BOTTOM, fill="x")

    return root


def main():
    root = create_main_window()
    load_contacts()
    refresh_listbox()
    update_status("Application started")
    root.mainloop()


if __name__ == "__main__":
    main()