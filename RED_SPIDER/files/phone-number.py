import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import PhoneNumberFormat

n = input("Enter the phone number: ")

# IMPORTANT: Set your country code here for accurate parsing (e.g., "FR", "US", "GB", "CA")
country_code = "FR" 

# Parse the number
try:
    number_object = phonenumbers.parse(n, country_code)
except Exception as e:
    print(f"Error parsing number: {e}")
    exit()

print("\n--- Basic Information ---")

# 1. Location/Region
location = geocoder.description_for_number(number_object, "en")
print("Country/Region:", location)

# 2. Service Provider/Carrier
operator = carrier.name_for_number(number_object, "en")
print("Operator/Carrier:", operator)

print("\n--- Technical Validation ---")

# 3. Validation Check
is_valid = phonenumbers.is_valid_number(number_object)
print("Is a valid number:", is_valid)

# 4. Possibility Check (often used to check if it's a mobile number)
is_possible = phonenumbers.is_possible_number(number_object)
print("Is a possible number (e.g., correct length):", is_possible)

# L'option qui causait l'erreur a été supprimée.

print("\n--- Formatting ---")

# 5. National Format
national_format = phonenumbers.format_number(number_object, PhoneNumberFormat.NATIONAL)
print("National Format:", national_format)

# 6. International Format
international_format = phonenumbers.format_number(number_object, PhoneNumberFormat.INTERNATIONAL)
print("International Format:", international_format)