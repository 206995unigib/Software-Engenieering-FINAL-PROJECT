# gui.py - everything the user sees (Tkinter). Each button calls one of my on_... functions,
# which read the fields, call validation.py and database.py, and show a messagebox.
# Orthogonality: I only build the screen in this file, no SQL or checks here.

import tkinter as tk
from tkinter import messagebox
from database import create_table, add_vehicle, plate_exists, delete_vehicle, get_vehicle  # I import my database functions
from validation import validate_vehicle  # I import my validation function

create_table()  # I create the table if it doesn't exist yet

# 1 - THE WINDOW

root = tk.Tk()  # I create the blank window
root.title('Car Dealership')  # I set the title of the window
root.geometry("1200x700")  # I give the window a fixed size
root.resizable(False, False)  # I block resizing, so it looks the same on any screen
root.configure(bg="#1c1c1e")  # I set the dark background

# 2 - BASIC WIDGETS
# pack() places each widget below the previous one

tk.Label(root, text="Car Dealership", font=("Arial", 32, "bold"), width=50, background="#c1121f", fg="white").pack(pady=30)  # I create the title bar, pady=30 leaves 30px above and below


# Add Vehicle button: I open a form to add a car
def on_add():
    win = tk.Toplevel(root)  # I create a new window, its parent is root
    win.title("Add Vehicle")

    win.geometry("600x450")

    # I create the FORM
    tk.Label(win, text="PLATE").grid(row=0, column=0)  # I create a text label that says PLATE
    plate = tk.Entry(win)
    plate.grid(row=0, column=1, padx=15)

    tk.Label(win, text="BRAND").grid(row=1, column=0)
    brand = tk.Entry(win)
    brand.grid(row=1, column=1, padx=15, pady=15)

    tk.Label(win, text="MODEL").grid(row=2, column=0)
    model = tk.Entry(win)  # I create an input inside the new window and store it in model
    model.grid(row=2, column=1, padx=15,)

    tk.Label(win, text="YEAR").grid(row=3, column=0)
    year = tk.Entry(win)  # I create the input first, then I show it with grid()
    year.grid(row=3, column=1, padx=15, pady=15)

    tk.Label(win, text="PRICE").grid(row=4, column=0)
    price = tk.Entry(win)  # I create the input and store it in price
    price.grid(row=4, column=1, padx=15)

    tk.Label(win, text="KMs").grid(row=5, column=0)
    km = tk.Entry(win)
    km.grid(row=5, column=1, padx=15, pady=15)

    # I save the car only if the plate is new and the data is valid
    def on_save():

        if plate_exists(plate.get()):  # I check if the plate is already saved
            messagebox.showerror("ERROR ", "PLATE ALREADY EXISTS")

        else:
            res = validate_vehicle(plate.get(), year.get(), price.get(), km.get())  # I get True or the error message
            if res == True:
                # I save the car in the database
                add_vehicle(plate.get(), brand.get(), model.get(), year.get(), price.get(), km.get())
                messagebox.showinfo("Saved", "Vehicle added")
            else:
                messagebox.showerror("ERROR", res)

    # I connect the SAVE button to on_save
    tk.Button(win, text="SAVE VEHICLE", width=25, command=on_save, background="#c1121f", fg="white").grid(row=6, column=0, columnspan=2)


# Filter Vehicles button: I open a window with the list of cars
def on_list():

    listwin = tk.Toplevel(root)
    listwin.title("LIST OF VEHICLES")
    listwin.geometry("650x450")

    tk.Label(listwin, text="Insert BRAND OR PLATE to filter the vehicles", font=20).grid(pady=15, columnspan=11)

    filtervehicle = tk.Entry(listwin, width=25, font=20)
    filtervehicle.grid(columnspan=11)

    # I show the cars that match the brand or plate typed
    def on_filter():
        for w in results.winfo_children():  # I delete the old rows before showing the new ones
            w.destroy()

        rows = get_vehicle(filtervehicle.get())  # I get a list of tuples, one tuple per car
        if len(rows) == 0:  # I found no cars
            messagebox.showerror("ERROR", "NO RESULTS FOUND")

        else:
            row = 1
            count = 5
            for i in rows:  # I go through each tuple, e.g. ('AB0213', 'Toyota', 'Corolla', 2020, 15000, 30000)
                tk.Label(results, text=row).grid(row=count, column=0)
                tk.Label(results, text="Plate", width=5, background="#2b2d42", fg="white").grid(row=count, column=1, padx=5)
                tk.Label(results, text=i[0]).grid(row=count, column=2)
                tk.Label(results, text="Brand", width=5, background="#2b2d42", fg="white").grid(row=count, column=3, padx=5)
                tk.Label(results, text=i[1]).grid(row=count, column=4)
                tk.Label(results, text="Model", width=5, background="#2b2d42", fg="white").grid(row=count, column=5, padx=5)
                tk.Label(results, text=i[2]).grid(row=count, column=6)
                tk.Label(results, text="Year", width=5, background="#2b2d42", fg="white").grid(row=count, column=7, padx=5)
                tk.Label(results, text=i[3]).grid(row=count, column=8)
                tk.Label(results, text="Price", width=5, background="#2b2d42", fg="white").grid(row=count, column=9, padx=5)
                tk.Label(results, text=i[4]).grid(row=count, column=10)
                tk.Label(results, text="KMs", width=5, background="#2b2d42", fg="white").grid(row=count, column=11, padx=5)
                tk.Label(results, text=i[5]).grid(row=count, column=12)

                count = count + 1
                row = row + 1

    # I connect the FILTER button to on_filter
    tk.Button(listwin, text="FILTER", width=15, command=on_filter, background="#c1121f", fg="white").grid(padx=15, pady=15, columnspan=11)

    results = tk.Frame(listwin)  # I create a box for the results and empty it on every filter
    results.grid(columnspan=13)

    on_filter()  # I call on_filter at the start, when the filtervehicle entry is empty,
    # so search="" and I get ALL the rows from the table


# Delete Vehicle button: I open a window to delete a car by plate
def on_delete():

    delwin = tk.Toplevel(root)
    delwin.geometry("350x200")
    delwin.title("ENTER PLATE")

    tk.Label(delwin, text="Enter the vehicle plate to DELETE", width=25).grid(padx=15, pady=15)
    delinput = tk.Entry(delwin, width=15, font=("Arial", 14))
    delinput.grid()

    # I delete the car only if the plate exists
    def on_submit():

        if plate_exists(delinput.get()):

            delete_vehicle(delinput.get())  # I delete it from the database
            messagebox.showinfo("SUCCESS", "VEHICLE DELETED SUCCESSFULLY")
        else:
            messagebox.showerror("ERROR", "VEHICLE NOT FOUND")

    tk.Button(delwin, text="SUBMIT", command=on_submit, background="#c1121f", fg="white", width=15).grid(pady=15)


# I create an invisible box (like a <div>) inside the window, to group the buttons
nav = tk.Frame(root, background="#1c1c1e")
nav.pack()  # I show the box below the title
# Each button: parent = nav (goes inside the box), width=33 = same width for all,
# side="left" = next to the previous one (not below), padx=5 = 5px gap on each side


# Refactoring: before, I created the three buttons separately.
# Now I define one function and use it for each button (DRY)
def select_buttons(option, function):
    tk.Button(nav, text=option, command=function, width=33, height=3, font=("Arial", 11), background="#c1121f", fg="white", cursor="hand2").pack(side="left", padx=5)


# I create the three main buttons
select_buttons("Add Vehicle", on_add)
select_buttons("Filter Vehicles", on_list)
select_buttons("Delete Vehicle", on_delete)


# I create a box for the car images
im = tk.Frame(root, bg="#1c1c1e")
im.pack(pady=25)


car_img2 = tk.PhotoImage(file="img/mercedesult.png").subsample(2)  # I show the image at half size with subsample(2), so it fits
tk.Label(im, image=car_img2, background="#1c1c1e").pack(side="left", padx=0)
tk.Label(im, image=car_img2, background="#1c1c1e").pack(side="left", padx=0)


root.mainloop()  # I keep the window open, it always goes at the end
