# My tests for validation.py. I run them from the project root: python -m pytest -v
from validation import validate_vehicle


# I check that a correct car returns True
def test_valid_vehicle():
    assert validate_vehicle("AB0213", "2020", "15000", "30000") == True


# I check that an empty plate returns the error
def test_valid_plate():
    assert validate_vehicle("", "2020", "15000", "30000") == 'Plate cannot be empty'


# I check that a wrong year returns the error
def test_valid_year():
    assert validate_vehicle("AB0213", "20201", "15000", "30000") == "Year must be between 1930 & 2026"


# I check that a negative price returns the error
def test_valid_price():
    assert validate_vehicle("AB0213", "2020", "-25", "30000") == "Price must be between 0 & 10000000"


# I check that too many KMs return the error
def test_valid_kms():
    assert validate_vehicle("AB0213", "2020", "15000", "3000000") == "Kms must be between 0 and 500000"


# I check that letters instead of numbers return the error
def test_letters_instead_of_numbers():
    assert validate_vehicle("AB0213", "abc", "15000", "30000") == "Year, price and KMs must be numbers"
