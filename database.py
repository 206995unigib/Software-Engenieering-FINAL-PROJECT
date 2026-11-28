# database.py - the only file that talks to the SQLite database (app.db).
# My functions:
#   get_connection()      -> opens app.db
#   create_table()        -> CREATE TABLE IF NOT EXISTS
#   add_vehicle(...)      -> INSERT
#   delete_vehicle(plate) -> DELETE
#   plate_exists(plate)   -> SELECT, True if the plate is already saved
#   get_vehicle(search)   -> SELECT (all, or by brand/plate)

import sqlite3

# Reversibility: I keep all the SQL in this file, so changing the database only touches here
DB_NAME = "app.db"


# I create a function that returns the connection with the database.
# As I use the connection in multiple functions, I apply the DRY principle
def get_connection():
    return sqlite3.connect(DB_NAME)
# The first time I run the app, create_table() creates app.db (if it is missing).
# After that, every function just opens that connection.
# With conn = get_connection(), I use conn.execute, conn.commit and conn.close


# I create the vehicles table. plate is the PRIMARY KEY, so it can't repeat
def create_table():
    conn = get_connection()  # Now conn has access to the database, so I can send requests
    conn.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            plate TEXT PRIMARY KEY,
            brand TEXT NOT NULL,
            model TEXT NOT NULL,
            year INTEGER NOT NULL,
            price REAL NOT NULL,
            km INTEGER NOT NULL
        )
    """)
    conn.commit()  # I save the changes on disk
    conn.close()  # I close the connection


# I insert a new car. The ? placeholders keep the values safe (no SQL injection)
def add_vehicle(plate, brand, model, year, price, km):
    conn = get_connection()
    conn.execute("""
        INSERT INTO vehicles (plate, brand, model, year, price, km) VALUES (?, ?, ?, ?, ?, ?)
    """, (plate, brand, model, year, price, km))
    conn.commit()  # I save the changes on disk
    conn.close()  # I close the connection


def delete_vehicle(plate):  # I delete the car with this plate
    conn = get_connection()
    conn.execute(" DELETE FROM vehicles WHERE plate = ?", (plate,))
    conn.commit()
    conn.close()

# If I find the plate, row = [tuple] -> the list is not empty -> True


def plate_exists(plate):
    conn = get_connection()
    row = conn.execute("SELECT plate FROM vehicles WHERE plate = ?", (plate,)).fetchall()
    conn.close()
    if len(row) == 0:
        return False
    else:
        return True


def get_vehicle(search=""):  # I give search a default value (empty)
    # fetchall() brings the results of the query as a list of rows
    conn = get_connection()  # I open the connection to the database
    if search == "":  # If search is empty, the user didn't type a brand or plate, so I return all cars
        rows = conn.execute("SELECT * FROM vehicles").fetchall()
    else:  # Otherwise I return only the cars with that brand or plate
        rows = conn.execute("SELECT * FROM vehicles WHERE brand = ? OR plate = ?", (search, search)).fetchall()
    conn.close()
    return rows  # I return the list of tuples to gui.py
