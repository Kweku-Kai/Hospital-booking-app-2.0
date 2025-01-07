import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry
from tktimepicker import SpinTimePickerModern
from tktimepicker import constants
from tkinter import messagebox
from datetime import datetime
from reportlab.lib.pagesizes import A4  # Import A4 page size
import webbrowser
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


connection = mysql.connector.connect(host='localhost', user="root", password="", port='3306', database='booking')
c = connection.cursor()

#global variables
treeview = None
tree_frame = None
patient_info_frame = None
actions= None
patient_id_entry = None
patient_name_entry = None
address_entry = None
phone_entry = None
gender_combobox = None
clinic_combobox = None
booking_id_entry = None
clinic_date_entry = None
time_entry = None
purpose_combobox = None
bookingdate_entry = None
actions = None
revert_button = None
delete_button = None
search_button = None
home_frame = None
print_button = None
canvas1 = None
total_label = None




window = tk.Tk()
window.title("Patient Booking System")

style = ttk.Style(window)
window.tk.call("source", "forest-light.tcl")
window.tk.call("source", "forest-dark.tcl")
style.theme_use("forest-dark")


main_frame = ttk.Frame(window)
main_frame.pack()


        
def show_home_page():
    # Function to switch to the home page
    global home_frame, canvas1, total_label
    if actions:
        actions.destroy()
    if tree_frame:
        tree_frame.destroy()
    if treeview:
        treeview.destroy()  
    if patient_info_frame:
        patient_info_frame.destroy() # Hide the tree frame for the booked list page
    # Create a new home frame
    home_frame = ttk.LabelFrame(main_frame, text="Home Page")
    home_frame.grid(row=0, column=1, padx=20, pady=20)

    # Fetch data from the database for gender distribution for the current day
    current_date = datetime.now().date()
    c.execute("SELECT Gender, COUNT(*) FROM patient_info WHERE Clinic_Date = %s GROUP BY Gender", (current_date,))
    gender_data = c.fetchall()

    # Calculate the total number of patients booked for the current day
    c.execute("SELECT COUNT(*) FROM patient_info WHERE Clinic_Date = %s", (current_date,))
    total_patients = c.fetchone()[0]

    # Prepare data for the pie chart (female-to-male distribution)
    gender_labels = [row[0] for row in gender_data]
    gender_counts = [row[1] for row in gender_data]

    # Plot pie chart for gender distribution
    fig1 = plt.figure(figsize=(5, 5))
    ax1 = fig1.add_subplot(221)  # Changed subplot position
    ax1.pie(gender_counts, labels=gender_labels, autopct='%1.1f%%', startangle=140)
    ax1.set_title('Gender Distribution for Today')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Fetch data from the database for clinic distribution
    c.execute("SELECT Clinic, COUNT(*) FROM patient_info GROUP BY Clinic")
    clinic_data = c.fetchall()
    clinic_labels = [row[0] for row in clinic_data]
    clinic_counts = [row[1] for row in clinic_data]

    # Plot pie chart for clinic distribution
    ax2 = fig1.add_subplot(222)  # Changed subplot position
    ax2.pie(clinic_counts, labels=clinic_labels, autopct='%1.1f%%', startangle=140)
    ax2.set_title('Clinic Distribution')
    ax2.axis('equal')

    # Display total number of patients booked for the day
    total_label = ttk.Label(home_frame, text=f"Total number of patients booked for today: {total_patients}")
    total_label.grid(row=1, column=0, pady=10)

    # Fetch data for address distribution
    c.execute("SELECT Address, COUNT(*) FROM patient_info WHERE Clinic_Date = %s GROUP BY Address", (current_date,))
    address_data = c.fetchall()
    addresses = [row[0] for row in address_data]
    counts = [row[1] for row in address_data]

    # Plot bar graph for address distribution
    ax3 = fig1.add_subplot(223)  # Changed subplot position
    ax3.bar(addresses, counts, color='skyblue')
    ax3.set_title('Address Distribution for Today')
    ax3.set_xlabel('Address')
    ax3.set_ylabel('Number of People')

    # Adjust layout
    plt.tight_layout()

    # Convert the Matplotlib figure to Tkinter canvas
    canvas1 = FigureCanvasTkAgg(fig1, master=home_frame)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=0, column=0, rowspan=2, columnspan=2)

    


def show_booking_page():
    # Function to switch to the booking page
    global tree_frame
    global treeview
    global patient_info_frame, actions, print_button, home_frame, canvas1, total_label
    global patient_id_entry, patient_name_entry, address_entry, phonenumber_entry, gender_combobox
    global clinic_combobox, booking_id_entry, clinicdate_entry, time_entry, purpose_combobox, bookingdate_entry
    if tree_frame:
        tree_frame.destroy()
    if treeview:
        treeview.destroy()
    if actions:
        actions.destroy()
    if home_frame:
        home_frame.destroy()
    #load_data()  # Load data for the booking page if needed
    # Add any other functionality specific to the booking page
    # You can modify this function to configure other widgets for the booking page
    #patient booking details
    #book form frame
#patient info section

    patient_info_frame = ttk.LabelFrame(main_frame, text="Patient Information")
    patient_info_frame.grid(row=0, column=1, padx=20, pady=20)

    patient_id_label = ttk.Label(patient_info_frame, text ="Patient ID")
    patient_id_label.grid(row=0, column=0)
    patient_name_label = ttk.Label(patient_info_frame, text ="Patient Name")
    patient_name_label.grid(row=0, column=1)
    address_label = ttk.Label(patient_info_frame, text ="Address")
    address_label.grid(row=0, column=2)
    phonenumber_label = ttk.Label(patient_info_frame, text ="Phonenumber")
    phonenumber_label.grid(row=2, column=0)

    patient_id_entry=ttk.Entry(patient_info_frame)
    patient_name_entry=ttk.Entry(patient_info_frame)
    address_entry=ttk.Entry(patient_info_frame)
    phonenumber_entry=ttk.Entry(patient_info_frame)
    patient_id_entry.grid(row=1, column=0)
    patient_name_entry.grid(row=1, column=1)
    address_entry.grid(row=1, column=2)
    phonenumber_entry.grid(row=3, column=0)

    gender_label= ttk.Label(patient_info_frame, text="Gender")
    gender_combobox = ttk.Combobox(patient_info_frame, values=["Male", "Female"])
    gender_label.grid(row=2, column=1)
    gender_combobox.grid(row=3, column=1)

    clinic_label= ttk.Label(patient_info_frame, text="Clinic")
    clinic_combobox = ttk.Combobox(patient_info_frame, values=["New Case", "Old case", "Review with Labs", "Labs", "Inquiry"])
    clinic_label.grid(row=2, column=2)
    clinic_combobox.grid(row=3, column=2)

    clinicdate_label = ttk.Label(patient_info_frame, text ="Clinic Date")
    clinicdate_label.grid(row=4, column=0)
    clinicdate_frame = ttk.Frame(patient_info_frame)
    clinicdate_frame.grid(row=5, column=0)
    clinicdate_entry = DateEntry(clinicdate_frame, selectmode='day')
    clinicdate_entry.pack()

    time_label = ttk.Label(patient_info_frame, text ="Time")
    time_label.grid(row=4, column=1)
    time_entry= SpinTimePickerModern(patient_info_frame)
    time_entry.addAll(constants.HOURS24)  # adds hours clock, minutes and period
    time_entry.configureAll(bg="#ffffff", height=1, fg="#000000", font=("Montserrat", 12), hoverbg="gray",
                            hovercolor="#000000", clickedbg="gray", clickedcolor="#ffffff", highlightcolor = "#000000", highlightbackground = "#000000")
    #time_entry.addHours12()
    time_entry.addHours24()
    time_entry.addMinutes()
    time_entry.grid(row=5, column=1)
    

    purpose_label= ttk.Label(patient_info_frame, text="Purpose")
    purpose_combobox = ttk.Combobox(patient_info_frame, values=["Breast", "Chemo", "Git and Sarcoma", "GU and CNS", "Gynae", "Head and Neck", "Review with Labs", "Labs", "Intramural", "CT Scan"])
    purpose_label.grid(row=6, column=0)
    purpose_combobox.grid(row=7, column=0)

    bookingdate_label = ttk.Label(patient_info_frame, text ="Booked Date")
    bookingdate_label.grid(row=6, column=1)
    bookingdate_frame = ttk.Frame(patient_info_frame)
    bookingdate_frame.grid(row=7, column=1)
    bookingdate_entry = DateEntry(bookingdate_frame, selectmode='day')
    bookingdate_entry.pack()

#Buttons
    submit_button = ttk.Button(patient_info_frame, text="Submit", command=submit_row)
    submit_button.grid(row=8, column=0, columnspan=3, sticky="nsew")

    for widget in patient_info_frame.winfo_children():
        widget.grid_configure(padx=10,pady=10)
        
def submit_row():
    try:
        patient_id = patient_id_entry.get()
        patient_name = patient_name_entry.get()
        address = address_entry.get()
        phone = phonenumber_entry.get()
        gender = gender_combobox.get()
        clinic = clinic_combobox.get()
        clinic_date = clinicdate_entry.get_date()
        clinic_time = time_entry.time()
        purpose = purpose_combobox.get()
        date_booked = bookingdate_entry.get_date()

        # Convert the time value to a formatted string
        clinic_hour = clinic_time[0]
        clinic_minute = clinic_time[1]

        # Convert the time value to a formatted string
        clinic_time= "{:02d}:{:02d}".format(clinic_hour, clinic_minute)

        insert_query = "INSERT INTO `patient_info`(`Patient_ID`, `Patient_Name`, `Address`, `Phone`, `Gender`, `Clinic`, `Clinic_Date`, `Clinic_Time`, `Purpose`, `Date_Booked`) VALUES (%s,%s,%s,%s, %s, %s, %s, %s, %s, %s)"
        row_values = (patient_id,patient_name,address,phone,gender,clinic,clinic_date,clinic_time,purpose,date_booked)
        print(patient_id,patient_name,address,phone,gender,clinic,clinic_date,clinic_time,purpose,date_booked)

        #Insert data into MySQL table
        c.execute(insert_query, row_values)
        connection.commit()

        messagebox.showinfo("Success", "Booking successful!")  # Show success message

        # Clear form entries after successful submission
        patient_id_entry.delete(0, tk.END)
        patient_name_entry.delete(0, tk.END)
        address_entry.delete(0, tk.END)
        phonenumber_entry.delete(0, tk.END)
        gender_combobox.set('')
        clinic_combobox.set('')
        purpose_combobox.set('')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to submit data: {str(e)}")
        
        


def show_booked_list_page():
    # Function to switch to the booked list page
    global tree_frame, treeview, patient_info_frame, actions, home_frame

    if patient_info_frame:
        patient_info_frame.destroy()
    if home_frame:
        home_frame.destroy()

    tree_frame = ttk.LabelFrame(main_frame, text="List")
    tree_frame.grid(row=0, column=1, pady=10)
    treeScroll = ttk.Scrollbar(tree_frame)
    treeScroll.pack(side="right", fill="y")
    cols = ("Patient ID", "Patient Name", "Clinic", "Clinic Date", "Clinic Time", "Purpose")
    treeview = ttk.Treeview(tree_frame, show="headings", columns=cols,
                            yscrollcommand=treeScroll.set, height=15)
    treeview.column("Patient ID", width=100, anchor="center")
    treeview.column("Patient Name", width=100, anchor="center")
    treeview.column("Clinic", width=100, anchor="center")
    treeview.column("Clinic Date", width=100, anchor="center")
    treeview.column("Clinic Time", width=100, anchor="center")
    treeview.column("Purpose", width=100, anchor="center")
    treeview.heading("Patient ID", text="Patient ID")
    treeview.heading("Patient Name", text="Patient Name")
    treeview.heading("Clinic", text="Clinic")
    treeview.heading("Clinic Date", text="Clinic Date")
    treeview.heading("Clinic Time", text="Clinic Time")
    treeview.heading("Purpose", text="Purpose")
    treeview.pack()
    treeScroll.config(command=treeview.yview)

    # Load data for the booked list page
    def displayData():
        # Clear existing data
        treeview.delete(*treeview.get_children())
        current_date = datetime.now().date()
        c.execute('SELECT * FROM `patient_info` WHERE `Clinic_Date` = %s', (current_date,))
        users = c.fetchall()

        for user in users:
            treeview.insert('', 'end', value=(user[0], user[1], user[5], user[7], user[8], user[9]))

    displayData()

    def delete_selected():
        selected_item = treeview.focus()  # Get the currently selected item in the Treeview
        if not selected_item:  # Check if no item is selected
            messagebox.showwarning("No Selection", "Please select an item to delete.")
            return  # Exit the function if no item is selected
        # If an item is selected, proceed with deletion
        item_id = treeview.item(selected_item, "values")[0]  # Get the Patient_ID from the selected item
        item_name = treeview.item(selected_item, "values")[1]  # Get the Patient_Name from the selected item

        # Show confirmation dialog before deleting
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete {item_name}?")
        if not confirm:  # If user cancels deletion, return without deleting
            return

        # Delete the selected item from the Treeview and database
        treeview.delete(selected_item)  # Delete from Treeview
        delete_from_database(item_id, item_name)  # Delete from database
        messagebox.showinfo("Deleted", f"{item_name} has been successfully deleted.")

    # Function to delete item from database
    def delete_from_database(item_id, item_name):
        delete_query = "DELETE FROM `patient_info` WHERE `Patient_ID` = %s AND `Patient_Name` = %s"
        c.execute(delete_query, (item_id, item_name))
        connection.commit()

    def search():
        val = searchbar_entry.get()
        if val:
            # Clear existing data
            treeview.delete(*treeview.get_children())

            # Execute search query
            c.execute("SELECT * FROM `patient_info` WHERE `Patient_Name` LIKE %s", ('%' + val + '%',))
            users1 = c.fetchall()

            if users1:
                for user in users1:
                    treeview.insert('', 'end', value=(user[0], user[1], user[5], user[7], user[8], user[9]))
            else:
                messagebox.showinfo("No Results", "No matching records found.")
        else:
            messagebox.showwarning("Empty Search", "Please enter a search term.")

    def generate_pdf():
        # Fetch unique clinic names from the database
        c.execute("SELECT * FROM patient_info")
        data = c.fetchall()
        c.execute("SELECT DISTINCT Clinic FROM patient_info")
        clinic_names = [row[0] for row in c.fetchall()]

        # Filter data based on clinic date equal to current date
        current_date = datetime.now().date()
        filtered_data = [row for row in data if row[7] == current_date]

        # Create a PDF document
        doc = SimpleDocTemplate("Cases.pdf", pagesize=A4)

        # Get the sample style sheet
        styles = getSampleStyleSheet()

        # Add the tables to the elements to be added to the document
        elements = []

        for clinic in clinic_names:
            # Create a Table object for each clinic
            table_data = [["Patient ID","Patient Name", "Clinic Time"]]  # Table headers
            for row in filtered_data:
                if row[5] == clinic:
                    patient_id = row[0]
                    patient_name = row[1]
                    clinic_time = str(row[8])
                    table_data.append([patient_id, patient_name, clinic_time])
                    
                    
            column_widths = [150, 150, 150]  # Adjust the widths as needed
            table = Table(table_data, colWidths=column_widths)

            # Create a TableStyle object and add it to the table
            style = TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ])
            table.setStyle(style)

            # Add clinic name as a heading above each table
            elements.append(Paragraph(clinic, styles["Title"]))
            elements.append(table)

            # Add a spacer between tables
            elements.append(Spacer(1, 0.5 * inch))  # Add a spacer of 0.5 inch height

        # Build the document
        doc.build(elements)

        # Return the output file name
        return "Cases.pdf"

    def print_pdf():
        # Generate the PDF
        output_file = generate_pdf()

        # Open the default print dialog box in Windows
        try:
            # Open the PDF file with the default application
            webbrowser.open(output_file)
            print(f"PDF opened with default application: '{output_file}'.")
        except Exception as e:
            print(f"Error opening print dialog box: {e}")

    # Actions frame
    actions = ttk.LabelFrame(main_frame, text="Actions")
    actions.grid(row=1, column=1, pady=10, padx=10)

    searchbar_entry = ttk.Entry(actions)
    searchbar_entry.grid(row=0, column=0)
    search_button = ttk.Button(actions, text="Search", command=search)
    search_button.grid(row=0, column=1, pady=10, padx=10)

    # Button to delete selected items
    delete_button = ttk.Button(actions, text="Delete", command=delete_selected)
    delete_button.grid(row=0, column=2, pady=10, padx=10)

    # Revert button
    revert_button = ttk.Button(actions, text="Revert", command=displayData)
    revert_button.grid(row=1, column=0, pady=10, padx=10)

    # Add a button to print the PDF
    print_button = ttk.Button(actions, text="Print PDF", command=print_pdf)
    print_button.grid(row=1, column=2, padx=10, pady=10)



options_frame = ttk.LabelFrame(main_frame, text="Navigation Tabs")
options_frame.grid(row=0, column=0, padx=20, pady=20, sticky='nsew')

show_home_page()

home_button = ttk.Button(options_frame, text="Home", command=show_home_page)
home_button.grid(row=2, column=0, sticky='nsew')

separator1 = ttk.Separator(options_frame)
separator1.grid(row=6, column=0, padx=(20, 20), pady=10, sticky="ew")

Book_button = ttk.Button(options_frame, text="Book", command=show_booking_page)
Book_button.grid(row=10, column=0, sticky='nsew')

separator2 = ttk.Separator(options_frame)
separator2.grid(row=14, column=0, padx=(20, 20), pady=10, sticky="ew")

list_button = ttk.Button(options_frame, text="Booked list", command=show_booked_list_page)
list_button.grid(row=18, column=0, sticky='nsew')

window.mainloop()