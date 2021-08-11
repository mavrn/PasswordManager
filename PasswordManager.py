import base64
import string
import time
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import pyperclip as pc
import sys

import PasswordWriter
from PasswordGenerator import PasswordGenerator, SPECIAL_CHARACTERS

MAIN_MENU = """[1] Get password
[2] List all passwords
[3] Write password
[4] List Registered Sites
[5] Replace Credentials
[6] Delete Credentials
[7] Customize Generator
[8] Generate Passwords
[9] Exit"""

CUSTOMIZE_MENU = """[1] Customize length
[2] Customize characters
[3] Set exclusive characters
[4] Print generator info
[5] Exit"""

SITE_NOT_FOUND_MSG = "There doesn't seem to be a site registered with this name."
gen = PasswordGenerator()
key = ""
encryptor = None


kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'\xa3\x8f\xcd\xf1\xe2@(\xc8\x89!\xb9\xe9s\x8c\xad\xec',
        iterations=100000,
        backend=default_backend()
)


def printl(input_list):
    for element in input_list:
        print(element.capitalize())


def wait_for_enter():
    time.sleep(1)
    input("Press Enter to continue...")


def encrypt(input_string):
    return encryptor.encrypt(input_string.encode())


def decrypt(input_string):
    try:
        return encryptor.decrypt(input_string.encode()).decode("utf-8")
    except InvalidToken:
        return "[Encrypted]"


def password_input(print_string="Leave blank to randomly generate | Enter the password: "):
    print(print_string)
    while True:
        password = input()
        if password == "" or password == "r":
            while True:
                password = gen.generate(re=True)[0]
                print("Randomly generated password:", password)
                print("Accept? [y/n/a]")
                answer = input()
                if answer == "y":
                    return password
                elif answer == "a":
                    print("Generating...")
                elif answer == "n":
                    print("Okay, enter password: ")
                    break
                else:
                    print("Invalid input. Enter password: ")
                    break
        else:
            if validate_password(password):
                return password
            else:
                print("This password doesn't seem very secure. Are you sure? [y/n]")
                answer = input()
                if answer == "y":
                    return password
                else:
                    print(print_string)


def validate_password(password):
    if password == "s":
        return True
    if len(password) < 8:
        return False
    has_specials = False
    has_numbers = False
    for char in password:
        if char in SPECIAL_CHARACTERS:
            has_specials = True
        elif char in string.digits:
            has_numbers = True
    return has_specials and has_numbers


def new_password():
    pw_info = {}
    site = input("Enter the site for the credentials: ").lower()
    if site in PasswordWriter.get_sites():
        print("This site is already registered")
        return
    else:
        pw_info["Site"] = site
        pw_info["Username"] = input("Enter the username: ")
        pw_info["Password"] = encrypt(password_input()).decode()
        PasswordWriter.set_pw(pw_info)
        print("Successfully registered password for site", pw_info["Site"].capitalize())


def get_password():
    site = input("Enter the site: ").lower()
    credentials = PasswordWriter.get_pw(site)
    if credentials is None:
        print(SITE_NOT_FOUND_MSG)
    else:
        print("Username: " + credentials[0])
        print("Password: " + decrypt(credentials[1]) + " (Copied to clipboard)")
        pc.copy(decrypt(credentials[1]))


def list_passwords():
    for site, user, password in PasswordWriter.get_credentials():
        print("{}: {} | {}".format(site.capitalize(), user, decrypt(password)))


def list_registered_sites():
    print("Fetching sites...")
    time.sleep(0.5)
    sites = PasswordWriter.get_sites()
    if not sites:
        print("No sites registered")
    else:
        printl(sites)


def replace_credentials():
    site = input("Enter the site: ").lower()
    if site in PasswordWriter.get_sites():
        credentials = PasswordWriter.get_pw(site)
        if decrypt(credentials[1]) == "[Encrypted]":
            print("You entered the wrong key to replace the password of this site.")
        else:
            print("Current Username:", credentials[0])
            new_user = input("Type \"s\" to leave the same | New Username: ")
            print("Current Password:", decrypt(credentials[1]))
            new_pass = password_input("Leave blank to randomly generate, type \"s\" to leave the same | New Password: ").decode()
            if new_user == "s":
                new_user = credentials[0]
            if new_pass == "s":
                new_pass = credentials[1]
            else:
                new_pass = encrypt(new_pass)
            PasswordWriter.replace_pw(site, new_user, new_pass)
            print("Successfully updated your credentials.")
    else:
        print(SITE_NOT_FOUND_MSG)


def delete_credentials():
    site = input("Enter the site: ").lower()
    if site in PasswordWriter.get_sites():
        PasswordWriter.delete_pw(site)
        print("Successfully deleted the credentials of site", site.capitalize())
    else:
        print(SITE_NOT_FOUND_MSG)


def customize_generator():
    while True:
        print(CUSTOMIZE_MENU)
        inp = input()
        if inp == "1":
            try:
                gen.set_length(int(input("Set new length: ")))
            except ValueError:
                print("Input was not a number.")
        elif inp == "2":
            wants_letters = False if input("Do you want letters in the pool? [y/n]") == "n" else True
            wants_numbers = False if input("Do you want numbers in the pool? [y/n]") == "n" else True
            wants_specials = False if input("Do you want specials in the pool? [y/n]") == "n" else True
            gen.set_characters(wants_letters, wants_numbers, wants_specials)
            print("Customized the character pool.")
        elif inp == "3":
            gen.set_custom_chars(input("Leave blank to disable | Type your custom characters in one line: "))
        elif inp == "4":
            print(gen)
        elif inp == "5":
            return
        else:
            print("Invalid input")


def generate_passwords():
    gen.generate(input("How many passwords do you want to generate? "))


MAIN_MENU_SWITCHER = {
            "1": get_password,
            "2": list_passwords,
            "3": new_password,
            "4": list_registered_sites,
            "5": replace_credentials,
            "6": delete_credentials,
            "7": customize_generator,
            "8": generate_passwords,
            "9": sys.exit
            }


def main():
    PasswordWriter.create_file()
    key_input = input("Enter a encryption key: ").encode()
    derived_key = kdf.derive(key_input)
    global encryptor
    encryptor = Fernet(base64.urlsafe_b64encode(derived_key))
    while True:
        print(MAIN_MENU)
        inp = input()
        if inp in MAIN_MENU_SWITCHER:
            MAIN_MENU_SWITCHER[inp]()
            wait_for_enter()
        else:
            print("Invalid input")


if __name__ == "__main__":
    main()
