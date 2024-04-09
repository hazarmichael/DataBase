from tkinter import messagebox, font, ttk
from database import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
import re
matplotlib.use("TkAgg")
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

def center_window(root, width, height):
   screen_width = root.winfo_screenwidth()
   screen_height = root.winfo_screenheight()
   center_x = int(screen_width / 2 - width / 2)
   center_y = int(screen_height / 2 - height / 2)
   root.geometry(f'{width}x{height}+{center_x}+{center_y}')
def create_home_page(open_customer_management_callback, open_view_form_callback, open_search_form_callback, open_queries_form_callback, db_connection):
    home_root = tk.Tk()
    home_root.title("Car Insurance Company")
    cm_to_pixels = home_root.winfo_fpixels('3c')
    relative_y_position = 1 - (cm_to_pixels / home_root.winfo_screenheight())

    background_color = "#5B8889"
    home_root.configure(background=background_color)
    window_width = home_root.winfo_screenwidth()
    window_height = home_root.winfo_screenheight()
    center_window(home_root, window_width, window_height)

    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=10)
    style.configure('W.TButton', font=('Arial', 12, 'bold'), foreground='white', background='#0078D7')

    welcome_font = font.Font(family="Italic", size=24, weight="bold")
    welcome_label = tk.Label(home_root, text="Welcome to our car insurance company", font=welcome_font, background=background_color, foreground="white")
    welcome_label.pack(pady=(40, 20))


    original_image = Image.open("logo.png")

    new_image_with_background = Image.new("RGBA", original_image.size, background_color)
    new_image_with_background.paste(original_image, (0, 0), original_image if original_image.mode == 'RGBA' else None)
    resized_image = new_image_with_background.resize((1000, 350), Image.Resampling.LANCZOS)
    logo_image = ImageTk.PhotoImage(resized_image)

    logo_label = ttk.Label(home_root, image=logo_image)
    logo_label.image = logo_image
    logo_label.pack(pady=10)

    buttons_frame = tk.Frame(home_root, background="White")
    buttons_frame.pack(pady=30)

    us_label = tk.Label(home_root, text="\n\n\n\n\n\n\n\n\n\nHazar Michael 1201838\tBaraa Shaikh Ahmad 1201714\tMaisam Nasser 1201058", font=('Arial', 12), background=background_color, foreground="white")
    us_label.pack(pady=(10, 20))

    customer_button = ttk.Button(buttons_frame, text="Customer",  style='TButton', command=lambda: open_customer_management_callback(home_root, db_connection))
    customer_button.grid(row=0, column=2, padx=5, pady=5)

    search_button = ttk.Button(buttons_frame, text="Search Portal", style='TButton', command=lambda: open_search_form_callback(home_root, db_connection))
    search_button.grid(row=0, column=3, padx=5, pady=5)

    view_button = ttk.Button(buttons_frame, text="Data Reports", style='TButton', command=lambda: open_view_form_callback(home_root, db_connection))
    view_button.grid(row=0, column=4, padx=5, pady=5)
    exit_button = ttk.Button(home_root, text="Exit", style='TButton', command=lambda: home_root.destroy())
    exit_button.place(relx=0.9, rely=relative_y_position, anchor="center")

    queries_button = ttk.Button(buttons_frame, text="Queries", style='TButton',
                                command=lambda: open_queries_form_callback(home_root, db_connection))
    queries_button.grid(row=0, column=5, padx=5, pady=5)

    buttons_frame.pack(anchor='center')

    return home_root


def open_customer_management_form(parent_root, db_connection):
    parent_root.withdraw()
    customer_root = tk.Toplevel()
    setup_customer_gui(customer_root, parent_root, db_connection)


def setup_customer_gui(root, parent_root, db_connection):
    root.title("Customer Management")

    # Set the background color
    background_color = "#5B8889"
    root.configure(bg=background_color)

    # Get the width and height of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    button_width = 30  # Width of buttons in characters
    frame_padding = 20  # Padding around the button frame

    # Set the geometry of the window to match the screen size
    root.geometry(f"{screen_width}x{screen_height}+0+0")

    try:
        # Assuming the image is in the same directory as the script
        image_path = "1.png"
        original_image = Image.open(image_path)
    except Exception as e:
        print(f"Error opening the image: {e}")
        return

    resized_image = original_image.resize((600, 300), Image.Resampling.LANCZOS)
    fun_image = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(root, image=fun_image, bg=background_color)
    image_label.image = fun_image
    image_label.pack(pady=20)
    button_frame = ttk.Frame(root)
    button_frame.pack(fill='x', padx=50, pady=10)

    button_frame = ttk.Frame(root, padding=frame_padding)
    button_frame.pack(pady=5)
    add_button = ttk.Button(button_frame, text="Add New Customer",
                            width=button_width,
                            command=lambda: open_insert_customer_form(parent_root, db_connection))
    add_button.pack(side='top', pady=1)

    delete_button = ttk.Button(button_frame, text="Delete insurancepolicy",
                               width=button_width,
                               command=lambda: open_delete_insurancepolicy_form(parent_root, db_connection))
    delete_button.pack(side='top', pady=1)
    delete_button_coveredperson = ttk.Button(button_frame, text="Delete a covered person",
                               width=button_width,
                               command=lambda: open_delete_coveredperson_form(parent_root, db_connection))
    delete_button_coveredperson.pack(side='top', pady=1)
    update_button = ttk.Button(button_frame, text="Update Customer's Informations",
                               width=button_width,
                               command=lambda: open_UPDATE_customer_form(parent_root, db_connection))
    update_button.pack(side='top', pady=1)
    Covered_Car = ttk.Button(button_frame, text="Add Another car for existing customer",
                               width=button_width,
                               command=lambda: Add_Another_Covered_Car(parent_root, db_connection))
    Covered_Car.pack(side='top', pady=1)
    Return_to_the_homepage_button = ttk.Button(button_frame, text="Back",
                                               width=button_width,
                                               command=lambda: Return_to_the_homepage(parent_root, root))
    Return_to_the_homepage_button.pack(side='top', pady=1)

def Add_Another_Covered_Car(parent_root, db_connection):
    parent_root.withdraw()
    Covered_Car_root = tk.Toplevel()
    setup_Covered_Car_gui(Covered_Car_root, parent_root, db_connection)

def setup_Covered_Car_gui(root, parent_root, db_connection):
    root.title("Add Another Covered Car")
    background_color = "#5B8889"  # Set the background color
    root.configure(bg=background_color)

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    customer_id_label = ttk.Label(root, text="customer ID:", background=background_color, font=("Helvetica", 16))
    customer_id_label.pack(pady=10)

    customer_id_entry = ttk.Entry(root)
    customer_id_entry.pack(pady=10)

    delete_button = ttk.Button(root, text="SEARCH",
                               command=lambda: ADD_Covered_Car_action(customer_id_entry.get(), db_connection, root,
                                                                      parent_root))
    delete_button.pack(padx=10, pady=10)

    return_button = ttk.Button(root, text="Back", command=lambda: return_to_parent(parent_root, root))
    return_button.pack( padx=10, pady=10)

    try:
        original_image = Image.open("1.png")
        resized_image = original_image.resize((500, 500), Image.LANCZOS)
        fun_image = ImageTk.PhotoImage(resized_image)
        image_label = ttk.Label(root, image=fun_image, background=background_color)
        image_label.image = fun_image  # Keep a reference!
        image_label.pack(pady=50)
    except Exception as e:
        print(f"Error opening the image: {e}")


def ADD_Covered_Car_action(customer_id, db_connection, child_root, parent_root):
    customer_data = search_customer(customer_id)
    if customer_data:
        open_insert_car_form(parent_root, db_connection, customer_id)
    else:
        messagebox.showerror("Error", f"No customer found with CustomerID {customer_id}")

def open_search_customer_form(parent_root, db_connection):
    parent_root.withdraw()
    search_customer_root = tk.Toplevel()
    setup_search_customer_gui(search_customer_root, parent_root, db_connection)

def setup_search_customer_gui(root, parent_root, db_connection):
    root.title("Search Customer")
    # Set a background color
    background_color = "#5B8889"
    root.configure(bg=background_color)
    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)
    # Create a fun and colorful header label
    header_label = ttk.Label(root, text="Find Customer Information", font=("Helvetica", 20),
                             background=background_color)
    header_label.pack(pady=20)

    # Create a customer ID label
    customer_id_label = ttk.Label(root, text="Enter Customer ID:", background=background_color)
    customer_id_label.pack(pady=10)

    # Create a customer ID entry field
    customer_id_entry = ttk.Entry(root)
    customer_id_entry.pack(pady=10, ipadx=20, ipady=5)  # Increase padding inside the entry field

    # Create a search button (maintaining existing structure)
    search_button = ttk.Button(root, text="Search", command=lambda: search_customer_action(
        customer_id_entry.get(), db_connection, root, parent_root))
    search_button.pack(pady=10)

    back_button = ttk.Button(root, text="Back", command=lambda: return_to_parent(parent_root, root))
    back_button.pack(pady=10)

    try:
        image_path = "5.png"
        original_image = tk.PhotoImage(file=image_path)

        subsample_factor = 2
        image = original_image.subsample(subsample_factor, subsample_factor)

        image_label = ttk.Label(root, image=image, background=background_color)
        image_label.image = image
        image_label.pack(pady=(10, 20))
    except Exception as e:
        print("Error loading image:", str(e))


def return_to_parent(parent_root, current_root):
    current_root.destroy()
    parent_root.deiconify()

def search_customer_action(customer_id, db_connection, child_root, parent_root):
    customer_data = search_customer(customer_id)
    cars_info = []
    if customer_data:
        CARID = get_customer_cars(customer_id)
        cars_info.append(customer_data)
        for car_id in CARID:
            car_info = search_CAR77(car_id)
            cars_info.append(car_info)
        info_window = tk.Toplevel(child_root)
        info_window.title("Customer Information")
        info_window.configure(bg='#5B8889')  # Set background color
        custom_font = ('Helvetica', 12, 'bold')  # Define custom font
        info_text = tk.Text(info_window, wrap="word", height=190, width=190, bg='#5B8889', font=custom_font)
        info_text.pack(padx=10, pady=10)
        info_text.insert(tk.END, "                                                                                      Customer Information:\n\n\n")
        if cars_info:
            for car_info in cars_info:
                info_text.insert(tk.END, "                                                                                    \n\n")
                if isinstance(car_info, dict):
                    for key, value in car_info.items():
                        info_text.insert(tk.END, f"{key}: {value}\n", custom_font)
                        info_text.insert(tk.END, f"\n", custom_font)
                    info_text.insert(tk.END, "\n")
                else:
                    info_text.insert(tk.END, "                                                                                      No car information available.\n", custom_font)
        else:
            info_text.insert(tk.END, "                                                                                      No customer information available.", custom_font)
    else:
        messagebox.showerror("Error", f"No customer found with CustomerID {customer_id}")



def open_insert_customer_form(parent_root, db_connection):
    parent_root.withdraw()
    insert_customer_root = tk.Toplevel()
    setup_gui(lambda data: perform_insert(db_connection, data), insert_customer_root, parent_root, db_connection)

def setup_gui(insert_callback, root, parent_root, db_connection):
    root.title("Customer Registration")
    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()

    center_window(root, window_width, window_height)

    style = ttk.Style()
    style.theme_use('clam')

    font_size = 12

    label_font = font.Font(family="Arial", size=font_size, weight="bold")
    entry_font = font.Font(family="Arial", size=font_size)

    style.configure('TLabel', font=label_font, background='#5B8889')
    style.configure('TEntry', font=entry_font, background='#5B8889')
    style.configure('TButton', font=('Arial', 12), padding=10)
    style.configure('W.TButton', font=('Arial', 12), foreground='black', background='White')

    main_frame = ttk.Frame(root, padding="10", style='TLabel')
    main_frame.pack(fill='both', expand=True)

    entries = {}
    labels = ['Customer ID', 'Name', 'Date of Birth', 'Contact Number', 'Email']

    for i, label_text in enumerate(labels):
        label = ttk.Label(main_frame, text=label_text + ":", style='TLabel')
        label.grid(row=i, column=0, sticky='w', padx=10, pady=5)

        entry = ttk.Entry(main_frame, font=entry_font, style='TEntry')
        entry.grid(row=i, column=1, sticky='ew', padx=10, pady=5)
        entries[label_text] = entry

    submit_button = ttk.Button(main_frame, text="Submit", command=lambda: on_submit(entries, insert_callback),
                               style='W.TButton')
    submit_button.grid(row=len(labels), columnspan=2, pady=10)

    def on_submit(entries, callback):
        customer_data = {label: entries[label].get() for label in labels}

        name = customer_data['Name']
        if not re.match("^[a-zA-Z\s]*$", name):
            messagebox.showerror("Error", "Name should contain only letters")
            return
        email = customer_data['Email']
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email address")
            return

        success, message = callback(customer_data)
        if success:
            messagebox.showinfo("Success", message)
            root.destroy()

            open_insert_car_form(parent_root, db_connection, customer_data['Customer ID'])
        else:
            messagebox.showerror("Error", message)

    return root


def pay_payment(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("payment Details")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    new_window.geometry(f'{window_width}x{window_height}+0+0')

    CoveredPerson_data = fetch_all_own_pay_payment(db_connection)
    tree = ttk.Treeview(new_window)
    tree["columns"] = ("PaymentNo", "Amount", "PaymentDate", "PaymentMethod", "CarID")
    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col)

    for customer in CoveredPerson_data:
        tree.insert("", tk.END, values=customer)

    tree.pack(fill='both', expand=True)


def own_car_det(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("car Details")
    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    new_window.geometry(f'{window_width}x{window_height}+0+0')

    CoveredPerson_data = fetch_all_own_car(db_connection)
    tree = ttk.Treeview(new_window)
    tree["columns"] = ("CarID", "Model", "ManufactureYear", "RegistrationNumber", "CustomerID")
    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col)

    for customer in CoveredPerson_data:
        tree.insert("", tk.END, values=customer)

    tree.pack(fill='both', expand=True)


def open_insert_customer_form(parent_root, db_connection):
    parent_root.withdraw()
    insert_customer_root = tk.Toplevel()
    setup_gui(lambda data: perform_insert(db_connection, data), insert_customer_root, parent_root, db_connection)



def setup_delete_coveredperson_gui(root, parent_root, db_connection):
    root.title("Delete coveredperson")
    background_color = "#5B8889"  # Set the background color
    root.configure(bg=background_color)

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    coveredperson_id_label = ttk.Label(root, text="coveredperson ID:", background=background_color, font=("Helvetica", 16))
    coveredperson_id_label.pack(pady=10)

    coveredperson_id_entry = ttk.Entry(root)
    coveredperson_id_entry.pack(pady=10)

    delete_button = ttk.Button(root, text="Delete",
                               command=lambda: delete_coveredperson_action(coveredperson_id_entry.get(), db_connection, root,
                                                                      parent_root))
    delete_button.pack(padx=10, pady=10)

    return_button = ttk.Button(root, text="Back", command=lambda: return_to_parent(parent_root, root))
    return_button.pack( padx=10, pady=10)

    try:
        original_image = Image.open("9.png")
        resized_image = original_image.resize((500, 500), Image.LANCZOS)
        fun_image = ImageTk.PhotoImage(resized_image)
        image_label = ttk.Label(root, image=fun_image, background=background_color)
        image_label.image = fun_image  # Keep a reference!
        image_label.pack(pady=50)
    except Exception as e:
        print(f"Error opening the image: {e}")
def setup_delete_insurancepolicy_gui(root, parent_root, db_connection):
    root.title("Delete insurancepolicy")
    background_color = "#5B8889"  # Set the background color
    root.configure(bg=background_color)

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    customer_id_label = ttk.Label(root, text="insurancepolicy ID:", background=background_color, font=("Helvetica", 16))
    customer_id_label.pack(pady=10)

    customer_id_entry = ttk.Entry(root)
    customer_id_entry.pack(pady=10)

    delete_button = ttk.Button(root, text="Delete",
                               command=lambda: delete_insurancepolicy_action(customer_id_entry.get(), db_connection, root,
                                                                      parent_root))
    delete_button.pack(padx=10, pady=10)

    return_button = ttk.Button(root, text="Back", command=lambda: return_to_parent(parent_root, root))
    return_button.pack( padx=10, pady=10)

    try:
        original_image = Image.open("9.png")
        resized_image = original_image.resize((500, 500), Image.LANCZOS)
        fun_image = ImageTk.PhotoImage(resized_image)
        image_label = ttk.Label(root, image=fun_image, background=background_color)
        image_label.image = fun_image  # Keep a reference!
        image_label.pack(pady=50)
    except Exception as e:
        print(f"Error opening the image: {e}")
def delete_coveredperson_action(insurancepolicy_ID, db_connection, child_root, parent_root):
    success, message = delete_coveredperson_id(db_connection, insurancepolicy_ID)
    if success:
        messagebox.showinfo("Success", message)
        child_root.destroy()
        parent_root.deiconify()
    else:
        messagebox.showerror("Error", message)
def delete_insurancepolicy_action(insurancepolicy_ID, db_connection, child_root, parent_root):
        success, message = delete_insurancepolicy_id(db_connection, insurancepolicy_ID)
        if success:
            messagebox.showinfo("Success", message)
            child_root.destroy()
            parent_root.deiconify()
        else:
            messagebox.showerror("Error", message)

def open_delete_coveredperson_form(parent_root, db_connection):
    parent_root.withdraw()
    delete_customer_root = tk.Toplevel()
    setup_delete_coveredperson_gui(delete_customer_root, parent_root, db_connection)
def open_delete_insurancepolicy_form(parent_root, db_connection):
    parent_root.withdraw()
    delete_customer_root = tk.Toplevel()
    setup_delete_insurancepolicy_gui(delete_customer_root, parent_root, db_connection)
def coveredperson(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("coveredperson Details")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    new_window.geometry(f'{window_width}x{window_height}+0+0')
    new_window.state('zoomed')

    CoveredPerson_data = fetch_all_CoveredPerson(db_connection)
    tree = ttk.Treeview(new_window)
    tree["columns"] = ("CoveredPersonID", "coveredName", "PolicyNo")
    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col)
    for customer in CoveredPerson_data:
        tree.insert("", tk.END, values=customer)
    tree.pack(fill='both', expand=True)
def have_insurancepolicy_det(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("insurancepolicy Details")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    new_window.geometry(f'{window_width}x{window_height}+0+0')
    new_window.state('zoomed')

    insurancepolicy_data = fetch_all_insurancepolicy(db_connection)
    tree = ttk.Treeview(new_window)
    tree["columns"] = ("PolicyNo", "StartDate", "EndDate", "CoverageType", "PremiumAmount", "CarID")
    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col)

    for customer in insurancepolicy_data:
        tree.insert("", tk.END, values=customer)

    tree.pack(fill='both', expand=True)
def display_customers(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("Customer Details")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    new_window.geometry(f'{window_width}x{window_height}+0+0')
    new_window.state('zoomed')

    customer_data = fetch_all_customers(db_connection)
    tree = ttk.Treeview(new_window)
    tree["columns"] = ("CustomerID", "Cname", "DateOfBirth", "ContactNumber", "Email")
    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col)

    for customer in customer_data:
        tree.insert("", tk.END, values=customer)

    tree.pack(fill='both', expand=True)
def open_insert_car_form(parent_root, db_connection, customer_id):
    parent_root.withdraw()
    insert_car_root = tk.Toplevel()
    setup_car_gui(lambda data: perform_car_insert(db_connection, data), insert_car_root, parent_root, customer_id, db_connection)


def setup_car_gui(insert_callback, root, parent_root, customer_id, db_connection):
    root.title("Car Registration")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    main_frame = ttk.Frame(root, padding="20", style='Main.TFrame')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Main.TFrame', background='#5B8889')
    style.configure('TLabel', font=('Arial', 10), background='#5B8889',
                    foreground='white')  # Smaller font size for labels
    style.configure('TEntry', font=('Arial', 12), background='white')
    style.configure('TButton', font=('Arial', 12, 'bold'), foreground='black', background='white')

    main_frame.pack(fill='both', expand=True)

    entries = {}
    labels = ['CarID', 'Model', 'ManufactureYear', 'RegistrationNumber']

    for label_text in labels:
        frame = ttk.Frame(main_frame, style='Main.TFrame')
        frame.pack(fill='x', pady=5)  # Reduced padding for a tighter layout

        label = ttk.Label(frame, text=label_text + ":", width=20, anchor='w')  # Fixed label width with left alignment
        label.pack(side='left', padx=5)  # Add some padding for better spacing

        entry = ttk.Entry(frame, font=('Arial', 12), width=30)
        entry.pack(side='left', padx=5)  # Pack on the left side with padding
        entries[label_text] = entry

    submit_button = ttk.Button(main_frame, text="Submit", command=lambda: on_submit(entries, insert_callback))
    submit_button.pack(pady=10)



    def on_submit(entries, callback):
        car_data = {label: entries[label].get() for label in labels}
        car_data['CustomerID'] = customer_id
        success, message = callback(car_data)
        if success:
            messagebox.showinfo("Success", message)
            for entry in entries.values():
                entry.delete(0, tk.END)
            root.destroy()  # Close the car form
            open_insert_insurancepolicy_form(parent_root, db_connection, car_data['CarID'])
        else:
            messagebox.showerror("Error", message)


def open_insert_insurancepolicy_form(parent_root, db_connection, CarID):
    parent_root.withdraw()
    insert_insurancepolicy_root = tk.Toplevel()
    setup_insurancepolicy_gui(lambda data: insurancepolicy_insert(db_connection, data), insert_insurancepolicy_root, parent_root, CarID,db_connection)


def setup_insurancepolicy_gui(insert_callback, root, parent_root, CarID, db_connection):
    root.title("Insurance Policy Registration")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    main_frame = ttk.Frame(root, padding="10", style='TFrame')
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#5B8889')
    style.configure('TLabel', font=('Arial', 10), background='#5B8889', foreground='white')  # Smaller font size for labels
    style.configure('TEntry', font=('Arial', 12), background='white')
    style.configure('TButton', font=('Arial', 12, 'bold'), foreground='black', background='white')

    main_frame.pack(fill='both', expand=True)

    entries = {}
    labels = ['StartDate', 'EndDate', 'CoverageType', 'PremiumAmount']

    for label_text in labels:
        frame = ttk.Frame(main_frame, style='TFrame')
        frame.pack(fill='x', pady=5)

        label = ttk.Label(frame, text=label_text + ":", width=20, anchor='w')  # Fixed width with left alignment
        label.pack(side='left', padx=5)  # Add padding for better spacing

        entry = ttk.Entry(frame, font=('Arial', 12), width=30)
        entry.pack(side='left', padx=5)  # Pack entry on the left side with padding
        entries[label_text] = entry

    submit_button = ttk.Button(main_frame, text="Submit", command=lambda: on_submit(entries, insert_callback))
    submit_button.pack(pady=10)

    def on_submit(entries, callback):
        # Extract data from entries
        insurancepolicy_data = {label: entries[label].get() for label in labels}
        insurancepolicy_data['CarID'] = CarID

        # Check if StartDate and EndDate are in the correct format
        try:
            start_date = datetime.strptime(insurancepolicy_data['StartDate'], '%Y-%m-%d')
            end_date = datetime.strptime(insurancepolicy_data['EndDate'], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return

        # Check if EndDate is after StartDate
        if end_date <= start_date:
            messagebox.showerror("Error", "End Date must be after Start Date")
            return

        success, message, result = insurancepolicy_insert(db_connection, insurancepolicy_data)
        if success:
            policy_no = result['policy_no']
            messagebox.showinfo("Success", message)
            for entry in entries.values():
                entry.delete(0, tk.END)
            root.destroy()
            open_insert_payment_form(parent_root, db_connection, CarID, policy_no)
            parent_root.deiconify()
        else:
            messagebox.showerror("Error", message)


def open_insert_payment_form(parent_root, db_connection, CarID, policy_no):
    parent_root.withdraw()
    insert_payment_root = tk.Toplevel()
    setup_payment_gui(lambda data: payment_insert(db_connection, data), insert_payment_root, parent_root, CarID, db_connection, policy_no)


def setup_payment_gui(insert_callback, root, parent_root, CarID, db_connection, policy_no):
    root.title("Payment Registration")
    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    main_frame = ttk.Frame(root, padding="10", style='TFrame')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TFrame', background='#5B8889')
    style.configure('TLabel', font=('Arial', 10), background='#5B8889',
                    foreground='white')  # Smaller font size for labels
    style.configure('TEntry', font=('Arial', 12), background='white')
    style.configure('TButton', font=('Arial', 12, 'bold'), foreground='black', background='white')

    main_frame.pack(fill='both', expand=True)

    entries = {}
    labels = ['Amount', 'PaymentDate']

    for label_text in labels:
        frame = ttk.Frame(main_frame, style='TFrame')
        frame.pack(fill='x', pady=5)

        label = ttk.Label(frame, text=label_text + ":", width=20, anchor='w')  # Fixed width with left alignment
        label.pack(side='left', padx=5)

        entry = ttk.Entry(frame, font=('Arial', 12), width=30)
        entry.pack(side='left', padx=5)  # Pack entry on the left side with padding
        entries[label_text] = entry

    payment_method_var = tk.StringVar()
    payment_method_frame = ttk.Frame(main_frame, style='TFrame')
    payment_method_frame.pack(fill='x', pady=5)

    payment_method_label = ttk.Label(payment_method_frame, text="Payment Method:", width=20, anchor='w')
    payment_method_label.pack(side='left', padx=5)

    payment_methods = ['Cash', 'Visa', 'Checks']
    for method in payment_methods:
        ttk.Radiobutton(payment_method_frame, text=method, variable=payment_method_var, value=method).pack(side='left')

    submit_button = ttk.Button(main_frame, text="Submit",
                               command=lambda: on_submit(entries, payment_method_var, insert_callback), style='TButton')
    submit_button.pack(pady=10)

    def on_submit(entries, payment_method_var, callback):
        # Extract data from entries
        payment_data = {label: entries[label].get() for label in labels}
        payment_data['CarID'] = CarID
        payment_data['PolicyNo'] = policy_no
        payment_data['PaymentMethod'] = payment_method_var.get()
        try:
            datetime.strptime(payment_data['PaymentDate'], '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
        success, message = callback(payment_data)
        if success:
            messagebox.showinfo("Success", message)
            for entry in entries.values():
                entry.delete(0, tk.END)
            root.destroy()
            open_insert_coveredperson_form(parent_root, db_connection, policy_no)
            parent_root.deiconify()
        else:
            messagebox.showerror("Error", message)


def open_insert_coveredperson_form(parent_root, db_connection, PolicyNo):
    parent_root.withdraw()
    insert_coveredperson_root = tk.Toplevel()
    setup_coveredperson_gui(lambda data: coveredperson_insert(db_connection, data), insert_coveredperson_root, parent_root, PolicyNo,db_connection)

def setup_coveredperson_gui(insert_callback, root, parent_root, PolicyNo, db_connection):
    root.title("coveredperson Registration")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    # Decrease the font size for labels
    label_font = font.Font(family="Arial", size=8, weight="bold")  # Adjusted size from 10 to 8
    entry_font = font.Font(family="Arial", size=10)

    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill='both', expand=True)

    entries = {}
    labels = ['CoveredPersonID', 'coveredName']

    for label_text in labels:
        frame = ttk.Frame(main_frame)
        frame.pack(fill='x', pady=5)

        label = ttk.Label(frame, text=label_text + ":", font=label_font)
        label.pack(side='left')

        entry = ttk.Entry(frame, font=entry_font)
        entry.pack(side='right', expand=True, fill='x')
        entries[label_text] = entry

    submit_button = ttk.Button(main_frame, text="Submit", command=lambda: on_submit(entries, insert_callback))
    submit_button.pack(pady=10)
    done_button = ttk.Button(main_frame, text="Done", command=lambda: on_submit3(entries, insert_callback))
    done_button.pack(pady=10)

    def on_submit(entries, callback):
        coveredperson_data = {label: entries[label].get() for label in labels}
        coveredperson_data['PolicyNo'] = PolicyNo

        if not coveredperson_data['coveredName']:
            messagebox.showerror("Error", "Covered name cannot be empty.")
            return

        success, message = callback(coveredperson_data)
        if success:
            messagebox.showinfo("Success", message)
            for entry in entries.values():
                entry.delete(0, tk.END)
            root.destroy()
            open_insert_coveredperson_form(parent_root, db_connection, PolicyNo)
        else:
            messagebox.showerror("Error", message)

    def on_submit3(entries, callback):
            root.destroy()  # Close the coveredperson form
            parent_root.deiconify()



def open_search_CARID_form(parent_root, db_connection):
    parent_root.withdraw()
    search_CAR_root = tk.Toplevel()
    setup_search_CARID_gui(search_CAR_root, parent_root, db_connection)


def setup_search_CARID_gui(root, parent_root, db_connection):
    root.title("Search By Car ID")

    # Set a background color
    background_color = "#5B8889"
    root.configure(bg=background_color)

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    # Create a fun and colorful header label similar to the customer search GUI
    header_label = ttk.Label(root, text="Search By Car ID", font=("Helvetica", 20), background=background_color)
    header_label.pack(pady=20)

    # Create a CAR ID label with the background color
    CAR_id_label = ttk.Label(root, text="Car ID:", background=background_color)
    CAR_id_label.pack(pady=10)

    # Create a CAR ID entry field with increased padding
    CAR_id_entry = ttk.Entry(root)
    CAR_id_entry.pack(pady=10, ipadx=20, ipady=5)

    # Create a search button (maintaining existing structure)
    search_button = ttk.Button(root, text="Search", command=lambda: search_CARID_action(
        CAR_id_entry.get(), db_connection, root, parent_root))
    search_button.pack(pady=10)

    # Back button similar to the customer search GUI
    back_button = ttk.Button(root, text="Back", command=lambda: return_to_parent(parent_root, root))
    back_button.pack(pady=10)

    try:
        image_path = "7.png"
        original_image = Image.open(image_path)

        # Reduce the desired width for the image a bit more
        desired_width = int(window_width * 0.4)  # Set to 40% of the window width, for example

        # Calculate the new height to maintain aspect ratio
        aspect_ratio = original_image.height / original_image.width
        new_height = int(desired_width * aspect_ratio)

        resized_image = original_image.resize((desired_width, new_height), Image.Resampling.LANCZOS)
        car_image = ImageTk.PhotoImage(resized_image)
        image_label = ttk.Label(root, image=car_image, background=background_color)
        image_label.image = car_image  # Keep a reference to the image

        # Pack the image with less vertical padding to move it up
        image_label.pack(pady=(5, 10))  # Reduce the top padding value
    except Exception as e:
        print("Error loading image:", str(e))


def search_CARID_action(customer_id, db_connection, child_root, parent_root):
    CAR_data = search_CAR(customer_id)
    if CAR_data:
        info_window = tk.Toplevel(child_root)
        info_window.title("Car Information")
        info_window.configure(bg='#5B8889')  # Set background color
        custom_font = ('Helvetica', 12, 'bold')  # Define custom font
        info_text = tk.Text(info_window, wrap="word", height=190, width=190, bg='#5B8889', font=custom_font)
        info_text.pack(padx=10, pady=10)
        info_text.insert(tk.END, "                                                                                      Car Information:\n\n\n")
        if isinstance(CAR_data, dict):
            for key, value in CAR_data.items():
                info_text.insert(tk.END, f"{key}: {value}\n", custom_font)
                info_text.insert(tk.END, f"\n\n", custom_font)
        else:
            info_text.insert(tk.END, "No CAR information available.", custom_font)
    else:
        messagebox.showerror("Error", f"No CAR found with CARID {customer_id}")


def open_search_insurancepolicy_form(parent_root, db_connection):
    parent_root.withdraw()
    search_insurancepolicy_root = tk.Toplevel()
    setup_search_insurancepolicy_gui(search_insurancepolicy_root, parent_root, db_connection)

def setup_search_insurancepolicy_gui(root, parent_root, db_connection):
    root.title("Search Insurance Policy")

    # Set a background color
    background_color = "#5B8889"
    root.configure(bg=background_color)

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    # Create a header label with the background color
    header_label = ttk.Label(root, text="Find Insurance Policy Information", font=("Helvetica", 20), background=background_color)
    header_label.pack(pady=20)

    # Create an Insurance Policy ID label with the background color
    insurancepolicy_id_label = ttk.Label(root, text="Insurance Policy ID:", background=background_color)
    insurancepolicy_id_label.pack(pady=10)

    # Create an Insurance Policy ID entry field with increased padding
    insurancepolicy_id_entry = ttk.Entry(root)
    insurancepolicy_id_entry.pack(pady=10, ipadx=20, ipady=5)

    # Create a search button (maintaining existing structure)
    search_button = ttk.Button(root, text="Search", command=lambda: search_insurancepolicy_action(
        insurancepolicy_id_entry.get(), db_connection, root, parent_root))
    search_button.pack(pady=10)

    # Back button similar to the customer search GUI
    back_button = ttk.Button(root, text="Back", command=lambda: return_to_parent(parent_root, root))
    back_button.pack(pady=10)

    try:
        image_path = "8.png"
        original_image = Image.open(image_path)

        # Calculate the new height keeping the aspect ratio intact
        base_width = window_width // 2  # Desired width, for example, half of the window width
        wpercent = (base_width / float(original_image.size[0]))
        hsize = int((float(original_image.size[1]) * float(wpercent)))

        resized_image = original_image.resize((base_width, hsize), Image.Resampling.LANCZOS)
        insurance_image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(root, image=insurance_image, background=background_color)
        image_label.image = insurance_image  # Keep a reference to the image
        image_label.pack(pady=(10, 20))
    except Exception as e:
        print("Error loading image:", str(e))

def search_insurancepolicy_action(insurancepolicy_id, db_connection, child_root, parent_root):
    insurancepolicy_data = search_insurancepolicy(insurancepolicy_id)
    if insurancepolicy_data is not None:
        info_window = tk.Toplevel(child_root)
        info_window.title("Insurance Policy Information")
        info_window.configure(bg='#5B8889')  # Set background color
        custom_font = ('Helvetica', 12, 'bold')  # Define custom font
        info_text = tk.Text(info_window, wrap="word", height=190, width=190, bg='#5B8889', font=custom_font)
        info_text.pack(padx=10, pady=10)
        info_text.insert(tk.END, "                                                                                   Insurance Policy Information:\n\n\n")
        if isinstance(insurancepolicy_data, dict):
            for key, value in insurancepolicy_data.items():
                info_text.insert(tk.END, f"{key}: {value}\n", custom_font)
                info_text.insert(tk.END, f"\n")
        else:
            info_text.insert(tk.END, "No insurancepolicy information available.", custom_font)
    else:
        messagebox.showerror("Error", f"No insurancepolicy found with insurancepolicyID {insurancepolicy_id}")


def open_search_form(parent_root, db_connection):
    parent_root.withdraw()
    search_root = tk.Toplevel()
    setup_search_gui(search_root, parent_root, db_connection)


def open_queries_form(parent_root, db_connection):
    parent_root.withdraw()
    queries_root = tk.Toplevel()
    setup_queries_gui(queries_root, parent_root, db_connection)

def setup_queries_gui(root, parent_root, db_connection):
    root.title("Queries")

    # Maximize the window to full screen
    root.state('zoomed')

    main_frame = tk.Frame(root, bg="#5B8889")
    main_frame.pack(fill='both', expand=True)

    # Set the styles to match the main page for TButton
    style = ttk.Style()
    style.configure('TButton', font=('Arial', 12), padding=10)

    # Load and resize the image
    try:
        original_image = Image.open("3.png")
        resized_image = original_image.resize((600, 300), Image.Resampling.LANCZOS)
        fun_image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(main_frame, image=fun_image, bg="#5B8889")
        image_label.image = fun_image  # Keep a reference!
        image_label.pack(pady=20)
    except Exception as e:
        print(f"Error opening the image: {e}")
        return
    buttons_frame = tk.Frame(main_frame, bg="#5B8889")
    buttons_frame.pack()
    feb_3_day_policies_button = ttk.Button(buttons_frame, text="Expiring Policies - within the next 30 days",
                                          command=lambda: show_policies_expiring_in_feb_2024(root, db_connection))
    feb_3_day_policies_button.pack(side=tk.TOP, fill='x', padx=7, pady=7)
    feb_2024_policies_button = ttk.Button(buttons_frame, text="Expiring Policies - Within the next 3 days",
                                          command=lambda: show_policies_expiring_in_3days(root, db_connection))
    feb_2024_policies_button.pack(side=tk.TOP, fill='x', padx=7, pady=7)
    BIRTH_button = ttk.Button(buttons_frame, text="Birthdays today",
                                          command=lambda: show_birth_customer(root, db_connection))
    BIRTH_button.pack(side=tk.TOP, fill='x', padx=7, pady=7)
    BPAY_button = ttk.Button(buttons_frame, text="Best Payment Methods for Customers",
                                          command=lambda: show_payment_methods(root, db_connection))
    BPAY_button.pack(side=tk.TOP, fill='x', padx=7, pady=7)
    Explore_Car_Models_Report = ttk.Button(buttons_frame, text="Explore Car Models ",
                                           command=lambda: FEB_Explore_Car_Models_Report(root, db_connection))
    Explore_Car_Models_Report.pack(side=tk.TOP, fill='x', padx=7, pady=7)

    explore_payment_methods_button = ttk.Button(buttons_frame, text="Explore Payment Methods",
                                                command=lambda: Explore_Payment_Methods_Report(root, db_connection))
    explore_payment_methods_button.pack(side=tk.TOP, fill='x', padx=7, pady=7)

    back_button = ttk.Button(buttons_frame, text="Back", command=lambda: return_to_main(root, parent_root))
    back_button.pack(side=tk.TOP, fill='x', padx=7, pady=7)



    def return_to_main(current_window, main_root):
        current_window.destroy()  # Close the current window
        main_root.deiconify()  # Show the main window again
    return root
def show_policies_expiring_in_feb_2024(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("Policies Expiring within the next 30 days ")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    new_window.geometry(f'{window_width}x{window_height}+0+0')

    policies_data = fetch_policies_expiring_soon(db_connection)
    tree = ttk.Treeview(new_window)
    tree["columns"] = ("PolicyNo", "StartDate", "EndDate", "CoverageType", "PremiumAmount", "CarID")
    tree.column("#0", width=0, stretch=tk.NO)
    for col in tree["columns"]:
        tree.column(col, anchor=tk.CENTER)
        tree.heading(col, text=col)

    for policy in policies_data:
        tree.insert("", tk.END, values=policy)

    tree.pack(fill='both', expand=True)

def setup_search_gui(root, parent_root, db_connection):
    root.title("Search")
    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    # Set the background color
    background_color = "#5B8889"
    root.configure(bg=background_color)

    # Load and display the image
    try:
        image_path = "4.png"  # Replace with your actual image file
        original_image = Image.open(image_path)
        resized_image = original_image.resize((300, 300), Image.Resampling.LANCZOS)
        search_image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(root, image=search_image, bg=background_color)
        image_label.image = search_image  # Keep a reference!
        image_label.pack(pady=20)
    except Exception as e:
        print(f"Error opening the image: {e}")

    # Create a frame for buttons
    buttons_frame = ttk.Frame(root, padding="10", relief=tk.RAISED)
    buttons_frame.pack(pady=10, padx=10)


    search_customer_button = ttk.Button(buttons_frame, text="Customer Report by ID",
                                        command=lambda: open_search_customer_form(root, db_connection))
    search_customer_button.pack(side=tk.TOP, fill='x', padx=10, pady=10)

    search_CARID_button = ttk.Button(buttons_frame, text="Car Report by ID",
                                     command=lambda: open_search_CARID_form(root, db_connection))
    search_CARID_button.pack(side=tk.TOP, fill='x', padx=10, pady=10)

    search_insurancepolicy_button = ttk.Button(buttons_frame, text="Policy Report by ID",
                                               command=lambda: open_search_insurancepolicy_form(root, db_connection))
    search_insurancepolicy_button.pack(side=tk.TOP, fill='x', padx=10, pady=10)

    Return_to_the_homepage_button = ttk.Button(buttons_frame, text="Main Menu",
                                               command=lambda: Return_to_the_homepage(parent_root, root))
    Return_to_the_homepage_button.pack(side=tk.TOP, fill='x', padx=10, pady=10)

    return root


def open_view_form(parent_root, db_connection):
    parent_root.withdraw()
    view_root = tk.Toplevel()
    setup_view_gui(view_root, parent_root, db_connection)

def setup_view_gui(root, parent_root, db_connection):
    root.title("Data Reports")

    # Set the background color
    background_color = "#5B8889"
    root.configure(bg=background_color)

    # Get the width and height of the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    button_width = 30  # Adjust to your preferred width
    frame_padding = 13  # Padding around the button frame

    # Set the geometry of the window to match the screen size
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    try:
        image_path = "6.png"
        original_image = Image.open(image_path)
        # Increase the size as needed
        new_size = (800, 400)  # For example, to make the image larger
        resized_image = original_image.resize(new_size, Image.Resampling.LANCZOS)
        fun_image = ImageTk.PhotoImage(resized_image)
    except Exception as e:
        print(f"Error opening the image: {e}")
        return
    image_label = tk.Label(root, image=fun_image, bg=background_color)
    image_label.image = fun_image  # Keep a reference.
    image_label.pack(pady=(0, 20))  # Adjust the bottom padding to move the frame down
    resized_image = original_image.resize((300, 600), Image.Resampling.LANCZOS)
    fun_image = ImageTk.PhotoImage(resized_image)
    image_label = tk.Label(root, image=fun_image, bg=background_color)
    image_label.image = fun_image

    # Create the button frame with padding and place it in the center
    button_frame = ttk.Frame(root, padding=frame_padding)
    button_frame.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
    view_button = ttk.Button(button_frame, text="Customers List",
                             width=button_width,
                             command=lambda: display_customers(root, db_connection))
    view_button.pack(fill=tk.X, pady=5)
    view_coveredperson_button2 = ttk.Button(button_frame, text="Covered Persons' Details",
                                            width=button_width,
                                            command=lambda: coveredperson(root, db_connection))
    view_coveredperson_button2.pack(fill=tk.X, pady=5)
    view_buttonfetch_own_car = ttk.Button(button_frame, text="Registered Cars",
                                          width=button_width,
                                          command=lambda: own_car_det(root, db_connection))
    view_buttonfetch_own_car.pack(fill=tk.X, pady=5)
    view_buttonfetch_all_insurancepolicy = ttk.Button(button_frame, text="Policy Details",
                                                      width=button_width,
                                                      command=lambda: have_insurancepolicy_det(root, db_connection))
    view_buttonfetch_all_insurancepolicy.pack(fill=tk.X, pady=5)

    view_buttonfetchpay_payment = ttk.Button(button_frame, text="Financial History",
                                             width=button_width,
                                             command=lambda: pay_payment(root, db_connection))
    view_buttonfetchpay_payment.pack(fill=tk.X, pady=5)

    Return_to_the_homepage_button = ttk.Button(button_frame, text="Main Menu",
                                               width=button_width,
                                               command=lambda: Return_to_the_homepage(parent_root, root))
    Return_to_the_homepage_button.pack(fill=tk.X, pady=5)
def Return_to_the_homepage(main_root, current_window):
    current_window.destroy()  # Close the current window
    main_root.deiconify()     # Show the main window again


def open_UPDATE_customer_form(parent_root, db_connection):
    parent_root.withdraw()
    search_UPDATE_root = tk.Toplevel()
    open_UPDATE_customer_form_gui(search_UPDATE_root, parent_root, db_connection)



def open_UPDATE_customer_form_gui(root, parent_root, db_connection):
    root.title("Update customer's information")
    root.configure(bg="#5B8889")

    window_width = parent_root.winfo_screenwidth()
    window_height = parent_root.winfo_screenheight()
    center_window(root, window_width, window_height)

    customer_id_label = ttk.Label(root, text="the ID of the customer you want to update:", background="#5B8889", foreground="black",
                                  font=("Arial", 16))
    customer_id_label.pack(pady=10)

    customer_id_entry = ttk.Entry(root, font=("Arial", 16), width=20)
    customer_id_entry.pack(pady=10)

    search_button = ttk.Button(root, text="Search", command=lambda: open_UPDATE_customer_form_action(root,
                                                                                                     customer_id_entry.get(),
                                                                                                     db_connection,
                                                                                                     root, parent_root))
    search_button.pack(pady=10)

    return_button = ttk.Button(root, text="Back", command=lambda: return_to_parent(parent_root, root))
    return_button.pack(padx=10, pady=10)

    try:
        original_image = Image.open("10.png")
        resized_image = original_image.resize((500, 500), Image.LANCZOS)
        fun_image = ImageTk.PhotoImage(resized_image)

        image_label = ttk.Label(root, image=fun_image, background="#5B8889")
        image_label.image = fun_image  # Keep a reference!
        image_label.pack(pady=50)
    except Exception as e:
        print(f"Error opening the image: {e}")

def open_UPDATE_customer_form_action(root, customer_id, db_connection, child_root, parent_root):
    customer_data = search_customer(customer_id)
    if customer_data:
        # Clear existing widgets in root
        for widget in root.winfo_children():
            widget.destroy()
        root.title("UPDATE Information")
        # Configure the rows and columns of the root window
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(2, weight=1)

        button_frame = ttk.Frame(root)
        button_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        button_width = 20
        # Get the background color of the root window
        bg_color = root.cget('bg')

        # Load the image with PIL
        image_path = "13.png"  # Update this path to your image's path
        pil_image = Image.open(image_path)
        photo = ImageTk.PhotoImage(pil_image)

        # Create a label for the image with the window background color and place it in the grid
        image_label = tk.Label(root, image=photo, bg=bg_color)
        image_label.image = photo  # Keep a reference!
        image_label.grid(row=0, column=1, padx=20, pady=20)  # Adjust row and column as needed

        # Get the list of car IDs associated with the customer
        car_ids = get_customer_cars(customer_id)

        # Create a button for each car ID
        for index, car_id in enumerate(car_ids):
            button = ttk.Button(button_frame, text=f"Car ID: {car_id}", width=button_width,
                                command=lambda id=car_id: open_car_update_form(root,id, parent_root, db_connection,customer_id))
            button.grid(row=index, column=0, padx=10, pady=5)
        return_button = ttk.Button(button_frame, text="Return", width=button_width,
                                   command=root.destroy)
        return_button.grid(row=len(car_ids), column=0, padx=10, pady=5)
    else:
        messagebox.showerror("Error", f"No customer found with CustomerID {customer_id}")
def open_car_update_form (root,id, parent_root, db_connection,customer_id):

        for widget in root.winfo_children():
            widget.destroy()
        root.title("UPDATE Information")
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(2, weight=1)

        button_frame = ttk.Frame(root)
        button_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        button_width = 30
        # Get the background color of the root window
        bg_color = root.cget('bg')

        # Load the image with PIL
        image_path = "13.png"  # Update this path to your image's path
        pil_image = Image.open(image_path)
        photo = ImageTk.PhotoImage(pil_image)

        # Create a label for the image with the window background color and place it in the grid
        image_label = tk.Label(root, image=photo, bg=bg_color)
        image_label.image = photo  # Keep a reference!
        image_label.grid(row=0, column=1, padx=20, pady=20)  # Adjust row and column as needed

        # Configure the button frame with the same background color
        button_frame = ttk.Frame(root, style='TFrame')
        button_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_rowconfigure(6, weight=1)  # Assuming you have 6 rows; adjust if necessary
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)


        # Assuming you have a style configured for your buttons, set the background color
        style = ttk.Style()
        style.configure('TFrame', background=bg_color)
        # Each button now has its own row in the grid
        add_covered_person_button = ttk.Button(button_frame, text="Add Covered Person", width=button_width,
                                               command=lambda: add_covered_person(id, parent_root, db_connection))
        add_covered_person_button.grid(row=1, column=1, padx=10, pady=1)  # Adjust padding as needed

        update_insu_policy_button = ttk.Button(button_frame, text="Update Insurance Policy", width=button_width,
                                               command=lambda: update_insu(id, parent_root, db_connection))
        update_insu_policy_button.grid(row=2, column=1, padx=10, pady=1)
        update_payment_button = ttk.Button(button_frame, text="Update Payment Information", width=button_width,
                                            command=lambda: update_pay_payment(id, parent_root, db_connection))
        update_payment_button.grid(row=3, column=1, padx=10, pady=1)
        update_car_info_button = ttk.Button(button_frame, text="Update Car Information", width=button_width,
                                            command=lambda: own_car(customer_id, parent_root, db_connection))
        update_car_info_button.grid(row=4, column=1, padx=10, pady=1)

        update_customer_info_button = ttk.Button(button_frame, text="Update Customer Information", width=button_width,
                                                 command=lambda: customer_UP(customer_id, parent_root, db_connection))
        update_customer_info_button.grid(row=5, column=1, padx=10, pady=1)
        # Return button
        return_button = ttk.Button(button_frame, text="Return", width=button_width,
                                   command=root.destroy)
        return_button.grid(row=6, column=1, padx=10, pady=1)
def  add_covered_person(carID,parent_root, db_connection):
    policy_no = update_customer_coveredperson(carID)
    open_insert_coveredperson_form(parent_root, db_connection, policy_no)
def update_insu(CARID, parent_root, db_connection):
    insurance_data = get_insurance_policy_info(CARID)
    if insurance_data:
        insu_window = tk.Toplevel(parent_root)
        insu_window.title("Insurance Policy Information")
        insu_window.configure(background="#5B8889")
        # Set the geometry of the window
        screen_width = insu_window.winfo_screenwidth()
        screen_height = insu_window.winfo_screenheight()
        insu_window.geometry(f"{screen_width}x{screen_height}")

        # Create separate frames for the form and the image
        form_frame = tk.Frame(insu_window, background="#5B8889")
        image_frame = tk.Frame(insu_window, background="#5B8889")

        # Pack the frames on either side of the window
        form_frame.pack(side='left', fill='both', expand=True)
        image_frame.pack(side='right', fill='y')

        # Use grid within form_frame for labels and entry widgets
        entry_boxes = {}
        label_font = ('Arial', 12, 'bold')  # Set the font for labels

        for i, field in enumerate(insurance_data.keys()):
            label = tk.Label(form_frame, text=field, bg="#5B8889", fg="white", font=label_font)
            label.grid(row=i, column=0, padx=10, pady=10)
            text_box = tk.Entry(form_frame, width=50)  # Adjust the width of the text box
            text_box.insert(tk.END, insurance_data[field])
            text_box.grid(row=i, column=1, padx=30, pady=10)
            entry_boxes[field] = text_box

        # Styling for the buttons
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), padding=6)  # Smaller buttons
        style.configure('W.TButton', font=('Arial', 10, 'bold'), foreground='black', background='#0078D7')

        # Function to save changes
        def save_changes():
            try:
                # Data conversion and validation
                for key in ['StartDate', 'EndDate']:
                    if entry_boxes[key].get():
                        insurance_data[key] = datetime.strptime(entry_boxes[key].get(), '%Y-%m-%d').date()
                    else:
                        insurance_data[key] = None

                # Check if EndDate is after StartDate
                if insurance_data['StartDate'] and insurance_data['EndDate']:
                    if insurance_data['EndDate'] <= insurance_data['StartDate']:
                        messagebox.showerror("Error", "End Date must be after Start Date")
                        return

                insurance_data['PremiumAmount'] = float(entry_boxes['PremiumAmount'].get()) if entry_boxes[
                    'PremiumAmount'].get() else None
                insurance_data['CoverageType'] = entry_boxes['CoverageType'].get()

                # Update in database
                success, message = update_insurance_policy(insurance_data, db_connection, CARID)
                messagebox.showinfo("Update Status", message)
                if success:
                    insu_window.destroy()

            except ValueError as ve:
                messagebox.showerror("Error", f"Invalid input: {ve}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        # Function to cancel update and close the window
        def cancel_update():
            insu_window.destroy()
        button_frame = tk.Frame(form_frame, bg="#5B8889")
        button_frame.grid(row=len(insurance_data) + 1, column=0, columnspan=2)
        save_button = ttk.Button(button_frame, text="Update", style='W.TButton', command=save_changes)
        save_button.grid(row=0, column=0, padx=5, pady=10)
        cancel_button = ttk.Button(button_frame, text="Cancel", style='W.TButton', command=cancel_update)
        cancel_button.grid(row=0, column=1, padx=5, pady=10)
        try:
            original_image = Image.open("12.png")  # Replace with the correct image path
            # Adjust the width and height in the resize() method to make the image larger
            resized_image = original_image.resize((800, 600), Image.LANCZOS)  # Example size: 800x600
            fun_image = ImageTk.PhotoImage(resized_image)

            image_label = ttk.Label(image_frame, image=fun_image, background="#5B8889")
            image_label.image = fun_image  # Keep a reference!
            image_label.pack(padx=50, pady=50, fill='both', expand=True)
        except Exception as e:
            messagebox.showerror("Image Error", f"Error opening the image: {e}")
    else:
        messagebox.showerror("Error", f"No insurance policy found with CARID {CARID}")


def save_changes(window, insurance_data, entry_boxes, db_connection,CARID):
    data_modified = False
    for field in insurance_data.keys():
        text_box = entry_boxes.get(field)
        if text_box is not None:
            new_value = text_box.get().strip()
            if new_value != str(insurance_data[field]):
                try:
                    value = int(new_value)
                    if value <= 0:
                        raise ValueError
                except ValueError:
                    messagebox.showerror("Error", f"Invalid value for {field}.")
                    return
                insurance_data[field] = value
                data_modified = True
    if data_modified:
        try:
            update_insurance_policy(insurance_data, db_connection,CARID)
            messagebox.showinfo("Success", "Update successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showinfo("No Changes", "No changes were made.")
    window.destroy()
def update_pay_payment(CARID, parent_root, db_connection):
    pay_payment_data = get_pay_payment_data_info(CARID)
    if pay_payment_data:
        payment_window = tk.Toplevel(parent_root)
        payment_window.title("Payment Information")
        payment_window.configure(background="#5B8889")

        # Set the geometry of the window
        screen_width = payment_window.winfo_screenwidth()
        screen_height = payment_window.winfo_screenheight()
        payment_window.geometry(f"{screen_width}x{screen_height}")

        # Create separate frames for the form and the image
        form_frame = tk.Frame(payment_window, background="#5B8889")
        image_frame = tk.Frame(payment_window, background="#5B8889")

        # Pack the frames on either side of the window
        form_frame.pack(side='left', fill='both', expand=True)
        image_frame.pack(side='right', fill='y')

        # Use grid within form_frame for labels and entry widgets
        entry_boxes = {}
        label_font = ('Arial', 12, 'bold')  # Set the font for labels

        for i, field in enumerate(pay_payment_data.keys()):
            label = tk.Label(form_frame, text=field, bg="#5B8889", fg="white", font=label_font)
            label.grid(row=i, column=0, padx=10, pady=10)
            text_box = tk.Entry(form_frame, width=50)
            text_box.insert(tk.END, pay_payment_data[field])
            text_box.grid(row=i, column=1, padx=30, pady=10)
            entry_boxes[field] = text_box

        # Styling for the buttons
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('W.TButton', font=('Arial', 10, 'bold'), foreground='black', background='#5B8889')

        # Button frame inside form_frame to use grid
        button_frame = tk.Frame(form_frame, bg="#5B8889")
        button_frame.grid(row=len(pay_payment_data) + 1, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(button_frame, text="Update", style='W.TButton', command=lambda: save_changes_pay_payment(payment_window, pay_payment_data, entry_boxes, db_connection,CARID))
        save_button.grid(row=0, column=0, padx=5, pady=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", style='W.TButton', command=payment_window.destroy)
        cancel_button.grid(row=0, column=1, padx=5, pady=10)

        # Load and display the image in image_frame
        try:
            original_image = Image.open("12.png")  # Make sure to provide the correct path to your image
            resized_image = original_image.resize((800, 600), Image.LANCZOS)  # The size you want for the image
            fun_image = ImageTk.PhotoImage(resized_image)
            image_label = ttk.Label(image_frame, image=fun_image, background="#5B8889")
            image_label.image = fun_image  # Keep a reference!
            image_label.pack(padx=50, pady=50, fill='both', expand=True)
        except Exception as e:
            messagebox.showerror("Image Error", f"Error opening the image: {e}")

    else:
        messagebox.showerror("Error", f"No payment found with CARID {CARID}")
def save_changes_pay_payment(window, pay_payment_data, entry_boxes, db_connection,CARID):
    data_modified = False
    for field in pay_payment_data.keys():
        text_box = entry_boxes.get(field)
        if text_box is not None:
            new_value = text_box.get().strip()
            if new_value != str(pay_payment_data[field]):
                if field == 'Amount':
                    try:
                        value = float(new_value)  # Amount should be a float
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid value for {field}. Must be a number.")
                        return
                elif field == 'PaymentDate':
                    try:
                        value = datetime.strptime(new_value, '%Y-%m-%d').date()  # PaymentDate should be a date
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid date format for {field}. Use YYYY-MM-DD.")
                        return
                else:
                    value = new_value  # Other fields are strings, no conversion needed

                pay_payment_data[field] = value
                data_modified = True

    if data_modified:
        try:
            update_pay_payment_policy(pay_payment_data, db_connection,CARID)
            messagebox.showinfo("Success", "Update successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showinfo("No Changes", "No changes were made.")
    window.destroy()

def own_car(customer_id, parent_root, db_connection):
    own_car_data = get_own_car_data_info(customer_id)
    if own_car_data:
        car_window = tk.Toplevel(parent_root)
        car_window.title("Car Information")
        car_window.configure(background="#5B8889")

        # Set the geometry of the window
        screen_width = car_window.winfo_screenwidth()
        screen_height = car_window.winfo_screenheight()
        car_window.geometry(f"{screen_width}x{screen_height}")

        # Create separate frames for the form and the image
        form_frame = tk.Frame(car_window, background="#5B8889")
        image_frame = tk.Frame(car_window, background="#5B8889")

        # Pack the frames on either side of the window
        form_frame.pack(side='left', fill='both', expand=True)
        image_frame.pack(side='right', fill='y')

        # Use grid within form_frame for labels and entry widgets
        entry_boxes = {}
        label_font = ('Arial', 12, 'bold')  # Set the font for labels

        for i, field in enumerate(own_car_data.keys()):
            label = tk.Label(form_frame, text=field, bg="#5B8889", fg="white", font=label_font)
            label.grid(row=i, column=0, padx=10, pady=10)
            text_box = tk.Entry(form_frame, width=50)  # Adjust the width of the text box
            text_box.insert(tk.END, own_car_data[field])
            text_box.grid(row=i, column=1, padx=30, pady=10)
            entry_boxes[field] = text_box

        # Styling for the buttons
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('W.TButton', font=('Arial', 10, 'bold'), foreground='black', background='#0078D7')

        # Button frame inside form_frame to use grid
        button_frame = tk.Frame(form_frame, bg="#5B8889")
        button_frame.grid(row=len(own_car_data) + 1, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(button_frame, text="Update", style='W.TButton', command=lambda: save_changes_own_car(car_window, own_car_data, entry_boxes, db_connection,customer_id))
        save_button.grid(row=0, column=0, padx=5, pady=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", style='W.TButton', command=car_window.destroy)
        cancel_button.grid(row=0, column=1, padx=5, pady=10)

        # Load and display the image in image_frame
        try:
            original_image = Image.open("12.png")  # Make sure to provide the correct path to your image
            resized_image = original_image.resize((800, 600), Image.LANCZOS)  # The size you want for the image
            fun_image = ImageTk.PhotoImage(resized_image)
            image_label = ttk.Label(image_frame, image=fun_image, background="#5B8889")
            image_label.image = fun_image  # Keep a reference!
            image_label.pack(padx=50, pady=50, fill='both', expand=True)
        except Exception as e:
            messagebox.showerror("Image Error", f"Error opening the image: {e}")

    else:
        messagebox.showerror("Error", f"No car found with customer_id {customer_id}")

def save_changes_own_car(window, own_car_data, entry_boxes, db_connection,customer_id):
    data_modified = False

    for field in own_car_data.keys():
        text_box = entry_boxes.get(field)
        if text_box is not None:
            new_value = text_box.get().strip()
            if new_value != str(own_car_data[field]):
                # Handle different fields separately
                if field == 'ManufactureYear':
                    try:
                        value = int(new_value)
                        if value < 1900 or value > 2100:  # Assuming reasonable year range
                            raise ValueError("Invalid year")
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid value for {field}. Enter a valid year.")
                        return
                elif field == 'RegistrationNumber':
                    try:
                        value = int(new_value)
                        if value <= 0:
                            raise ValueError("Invalid registration number")
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid value for {field}. Enter a valid number.")
                        return
                else:
                    value = new_value

                own_car_data[field] = value
                data_modified = True

    if data_modified:
        try:
            update_own_car_policy(own_car_data, db_connection,customer_id)
            messagebox.showinfo("Success", "Update successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showinfo("No Changes", "No changes were made.")
    window.destroy()

def customer_UP(customer_id, parent_root, db_connection):
    customer_data = get_customer_info(customer_id)
    if customer_data:
        customer_window = tk.Toplevel(parent_root)
        customer_window.title("Customer Information")
        customer_window.configure(background="#5B8889")

        # Set the geometry of the window
        screen_width = customer_window.winfo_screenwidth()
        screen_height = customer_window.winfo_screenheight()
        customer_window.geometry(f"{screen_width}x{screen_height}")

        # Create separate frames for the form and the image
        form_frame = tk.Frame(customer_window, background="#5B8889")
        image_frame = tk.Frame(customer_window, background="#5B8889")

        # Pack the frames on either side of the window
        form_frame.pack(side='left', fill='both', expand=True)
        image_frame.pack(side='right', fill='y')

        # Use grid within form_frame for labels and entry widgets
        entry_boxes = {}
        label_font = ('Arial', 12, 'bold')  # Set the font for labels

        for i, field in enumerate(customer_data.keys()):
            label = tk.Label(form_frame, text=field, bg="#5B8889", fg="white", font=label_font)
            label.grid(row=i, column=0, padx=10, pady=10)
            text_box = tk.Entry(form_frame, width=50)
            text_box.insert(tk.END, customer_data[field])
            text_box.grid(row=i, column=1, padx=30, pady=10)
            entry_boxes[field] = text_box

        # Styling for the buttons
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 10), padding=6)
        style.configure('W.TButton', font=('Arial', 10, 'bold'), foreground='black', background='#0078D7')

        # Button frame inside form_frame to use grid
        button_frame = tk.Frame(form_frame, bg="#5B8889")
        button_frame.grid(row=len(customer_data) + 1, column=0, columnspan=2, pady=10)

        save_button = ttk.Button(button_frame, text="Update", style='W.TButton', command=lambda: save_changes_customer(customer_window, customer_data, entry_boxes, db_connection,customer_id))
        save_button.grid(row=0, column=0, padx=5, pady=10)

        cancel_button = ttk.Button(button_frame, text="Cancel", style='W.TButton', command=customer_window.destroy)
        cancel_button.grid(row=0, column=1, padx=5, pady=10)

        # Load and display the image in image_frame
        try:
            original_image = Image.open("12.png")  # Make sure to provide the correct path to your image
            resized_image = original_image.resize((800, 600), Image.LANCZOS)  # The size you want for the image
            fun_image = ImageTk.PhotoImage(resized_image)
            image_label = ttk.Label(image_frame, image=fun_image, background="#5B8889")
            image_label.image = fun_image  # Keep a reference!
            image_label.pack(padx=50, pady=50, fill='both', expand=True)
        except Exception as e:
            messagebox.showerror("Image Error", f"Error opening the image: {e}")

    else:
        messagebox.showerror("Error", f"No customer found with customer_id {customer_id}")
def save_changes_customer(window, customer_data, entry_boxes, db_connection,customer_id):
    data_modified = False
    for field in customer_data.keys():
        text_box = entry_boxes.get(field)
        if text_box is not None:
            new_value = text_box.get().strip()
            if new_value != str(customer_data[field]):
                # Special handling for DateOfBirth
                if field == 'DateOfBirth':
                    try:
                        new_value = datetime.strptime(new_value, '%Y-%m-%d').date()
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid date format for {field}. Use YYYY-MM-DD.")
                        return

                customer_data[field] = new_value
                data_modified = True

    if data_modified:
        try:
            update_customer_info(customer_data, db_connection,customer_id)
            messagebox.showinfo("Success", "Update successful!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showinfo("No Changes", "No changes were made.")
    window.destroy()


def toggle_fullscreen(window):
    if window.attributes('-fullscreen'):
        window.attributes('-fullscreen', False)
    else:
        window.attributes('-fullscreen', True)


def FEB_Explore_Car_Models_Report(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("Car Models Count")
    new_window.geometry(f'{new_window.winfo_screenwidth()}x{new_window.winfo_screenheight()}')

    fullscreen_button = tk.Button(new_window, text="Toggle Fullscreen", command=lambda: toggle_fullscreen(new_window),
                                  bg="white")  # Set background color to white
    fullscreen_button.pack(fill=tk.BOTH)

    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT Model, COUNT(*) as ModelCount
        FROM own_car
        GROUP BY Model
    """)
    result = cursor.fetchall()
    if result:
        field_names = [i[0] for i in cursor.description]
        models = [row[field_names.index('Model')] for row in result]
        counts = [row[field_names.index('ModelCount')] for row in result]

        # Define the desired range for the y-axis
        y_axis_range = range(1, 8)  # This will ensure the y-axis goes from 1 to 7

        # Adjust the bar_width to make the bars narrower
        bar_width = 0.5  # Adjust this value to make the bars narrower or wider

        fig, ax = plt.subplots(figsize=(1, 1), tight_layout=True)
        bars = ax.bar(models, counts, color='#5B8889', width=bar_width)
        ax.set_xlabel('Car Model')
        ax.set_ylabel('Count')
        ax.set_title('Car Models Count')
        ax.set_yticks(y_axis_range)  # Set y-axis ticks to the desired range
        for bar in bars:
            bar.set_edgecolor('#5B8889')
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
    else:
        print("No data found.")
    cursor.close()

def Explore_Payment_Methods_Report(parent_root, db_connection):
    new_window = tk.Toplevel(parent_root)
    new_window.title("Payment Methods Count")
    new_window.geometry(f'{new_window.winfo_screenwidth()}x{new_window.winfo_screenheight()}')

    fullscreen_button = tk.Button(new_window, text="Toggle Fullscreen", command=lambda: toggle_fullscreen(new_window),
                                  bg="white")
    fullscreen_button.pack(fill=tk.BOTH)

    cursor = db_connection.cursor()
    cursor.execute("""
        SELECT PaymentMethod, COUNT(*) as MethodCount
        FROM pay_payment
        GROUP BY PaymentMethod
    """)
    result = cursor.fetchall()
    if result:
        field_names = [i[0] for i in cursor.description]
        methods = [row[field_names.index('PaymentMethod')] for row in result]
        counts = [row[field_names.index('MethodCount')] for row in result]

        y_axis_numbers = [1, 2, 3, 4, 5, 6, 7]
        bar_width = 0.5

        fig, ax = plt.subplots(figsize=(1, 1), tight_layout=True)
        bars = ax.bar(methods, counts, color='#5B8889', width=bar_width)
        ax.set_xlabel('Payment Method')
        ax.set_ylabel('Count')
        ax.set_title('Payment Methods Count')
        ax.set_yticks(y_axis_numbers)
        for bar in bars:
            bar.set_edgecolor('#5B8889')
        canvas = FigureCanvasTkAgg(fig, master=new_window)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        canvas.draw()
    else:
        print("No data found.")
    cursor.close()

def show_policies_expiring_in_3days(parent_root, db_connection):
    try:
        today_date = datetime.now().date()
        end_date_range = today_date + timedelta(days=3)
        results = fetch_policies_expiring_in_3_days(db_connection, today_date, end_date_range)
        if results:
            info_window = tk.Toplevel(parent_root)
            info_window.title("Expiring Policies - Within the next 3 days")
            info_window.configure(bg='#5B8889')
            custom_font = ('Helvetica', 12, 'bold')
            info_text = tk.Text(info_window, wrap="word", height=190, width=190, bg='#5B8889', font=custom_font)
            info_text.pack(padx=10, pady=10)
            if isinstance(results[0], tuple):
                info_text.insert(tk.END,
                                 "                                                                                                        Expiring Policies - Within the next 3 days:\n\n\n")
                for result in results:
                    info_text.insert(tk.END,
                                     f"                                                                                                                                     ")
                    info_text.insert(tk.END, f"Name: {result[0]}\n", custom_font)
                    info_text.insert(tk.END,
                                     f"                                                                                                                                     ")
                    info_text.insert(tk.END, f"Contact Number: {result[1]}\n", custom_font)
                    info_text.insert(tk.END,
                                     f"                                                                                                ")
                    info_text.insert(tk.END, "-" * 250 + "\n")
            else:
                info_text.insert(tk.END, "No information")
        else:
            messagebox.showerror("Error", "No Expiring Policies - Within the next 3 days")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
def show_birth_customer(parent_root, db_connection):
    try:
        today_date = datetime.now().date()
        results = fetch_birth_customer(db_connection, today_date)
        if results:
            info_window = tk.Toplevel(parent_root)
            info_window.title("Birthdays Today")

            # Get the screen width and height
            screen_width = parent_root.winfo_screenwidth()
            screen_height = parent_root.winfo_screenheight()

            # Set the window size to the screen size
            info_window.geometry(f"{screen_width}x{screen_height}+0+0")

            info_window.configure(bg='#5B8889')
            custom_font = ('Helvetica', 14, 'bold')

            info_text = tk.Text(info_window, wrap="word", bg='#5B8889', font=custom_font)
            info_text.pack(padx=10, pady=10)

            info_text.insert(tk.END, "Birthdays Today:\n\n")
            for result in results:
                name, contact_number = result  # Unpacking the tuple for clarity
                info_text.insert(tk.END, f"Name: {name}\nContact Number: {contact_number}\n\n")

            info_text.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Notification", "No Birthdays Today")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


def show_payment_methods(parent_root, db_connection):
    try:
        best_payment_method = fetch_payment_methods(db_connection)
        if best_payment_method:
            info_window = tk.Toplevel(parent_root)
            info_window.title("Best Payment Method for Customers")
            info_window.state('zoomed')

            info_window.configure(bg='#5B8889')
            custom_font = ('Helvetica', 14, 'bold')

            title_label = tk.Label(info_window, text="Best Payment Method for Customers", bg='#5B8889', font=custom_font)
            title_label.pack(padx=10, pady=(10, 0))

            info_text = tk.Text(info_window, wrap="word", height=10, width=50, bg='#5B8889', font=('Helvetica', 12))
            info_text.pack(padx=10, pady=10)
            info_text.insert(tk.END, f"\n\n {best_payment_method}\n\n")
            info_text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "No payment data available")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
