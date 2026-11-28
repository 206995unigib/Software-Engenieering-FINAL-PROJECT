# validation.py - I check the data the user types. I return True if it's fine, or the error message.
# KIS: I just use simple ifs and one try/except.
# My functions:
#   validate_vehicle(...) -> I validate the whole form before add_vehicle


# I check every field. I return the first error I find, or True at the end
def validate_vehicle(plate, year, price, km):
    try:

        if plate == "":  # I check the plate is not empty
            return "Plate cannot be empty"

        intyear = int(year)  # I convert year to an integer. If it fails, I jump to except ValueError

        if not (intyear >= 1930 and intyear <= 2026):  # I check the year range
            return "Year must be between 1930 & 2026"

        pricefloat = float(price)  # I convert the price to a number
        if not (pricefloat >= 0 and pricefloat <= 10000000):  # I check the price range
            return "Price must be between 0 & 10000000"

        floatkms = float(km)  # I convert the KMs to a number
        if not (floatkms >= 0 and floatkms <= 500000):  # I check the KMs range
            return "Kms must be between 0 and 500000"

    except ValueError:  # If any conversion fails, I return this error
        return "Year, price and KMs must be numbers"

    return True  # Everything is fine
