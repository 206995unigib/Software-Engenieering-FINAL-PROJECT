# My tests for database.py. I run them from the project root: python -m pytest -v
from database import add_vehicle, delete_vehicle, plate_exists


# I add a test car and check that it exists
def test_add_vehicle():
    add_vehicle("TEST1", "Toyota", "Corolla", 2018, 20000, 20000)
    assert plate_exists("TEST1") == True
    delete_vehicle("TEST1")  # I clean up, so app.db stays the same


# I add a test car, delete it and check that it's gone
def test_delete_vehicle():
    add_vehicle("TEST2", "Ford", "Fiesta", 2015, 9000, 80000)
    delete_vehicle("TEST2")
    assert plate_exists("TEST2") == False
