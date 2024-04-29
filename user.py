from passlib import pwd
from passlib.hash import sha512_crypt
import os
import re
import json
import db
import shutil
from datetime import datetime

WRKDIR = f"/home/{os.getlogin()}/.localpwm/"
PW_HASH_FILE = "user-hash.txt"
HOSTNAME = os.getlogin()
DB_FILE = f"/home/{HOSTNAME}/.localpwm/pw.db"

def is_valid_password(password):
    # Check if password length is between 8 and 24 characters
    if len(password) < 8 or len(password) > 24:
        return False
    
    # Check if password contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False
    
    # Check if password contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False
    
    # Check if password contains at least one digit
    if not re.search(r'[0-9]', password):
        return False
    
    # Check if password contains at least one symbol
    if not re.search(r'[!@#$%^&*()_+{}|:"<>?`\-=[\];\',./]', password):
        return False
    
    return True 

class User:



    def __init__(self):
        self.passwords = {}
        self.active = False
        self.name = os.getlogin()
        self.init_user()

    def init_user(self):
        if os.path.exists(WRKDIR) and os.path.exists(f"{WRKDIR}{PW_HASH_FILE}"):
            print(f"Welcome {self.name}!")
            return 0
        elif os.path.exists(WRKDIR) and not os.path.exists(f"{WRKDIR}{PW_HASH_FILE}"):
            print("Oh no you have no password!")
            if not os.path.exists(f"{WRKDIR}pw.db"):
                print("No .db file... creating now")
            with open(DB_FILE, "w") as file:
                db.create_table()
            self.set_user_password()
            return None
        elif os.path.exists(WRKDIR) and not os.path.exists(f"{WRKDIR}pw.db"):
            print("No .db file... creating now")
            with open(DB_FILE, "w") as file:
                db.create_table()
        else:
            os.mkdir(WRKDIR)
            with open(DB_FILE) as file:
                db.create_table()
            self.set_user_password()
            

    def set_user_password(self): 
        if os.path.exists(f"{WRKDIR}{PW_HASH_FILE}"):
            print("Enter master password.")
            return None  
        user_pw = input("Enter master password --> ")
        if is_valid_password(user_pw):
            self.user_password = user_pw
            hashed_password = sha512_crypt.hash(self.user_password)
            if not os.path.exists(f"{WRKDIR}{PW_HASH_FILE}"):
                with open(f"{WRKDIR}{PW_HASH_FILE}", "w") as file:
                    file.write(hashed_password)
                
            return self.user_password
        print("Password is invalid")
        return None

    def login(self):
        pw_attempt = input("Enter password --> ")
        if not os.path.exists(f"{WRKDIR}{PW_HASH_FILE}"):
            print(f"Password not found check {WRKDIR} for {PW_HASH_FILE}")
            return None
        with open(f"{WRKDIR}{PW_HASH_FILE}", "r") as file:
            pw_hash = file.read()
        if sha512_crypt.verify(pw_attempt, pw_hash):
            print("Hash match, password correct.")
            with open(f"{WRKDIR}Logged_in", 'w') as file:
                file.write("Will be deleted on logout")
            self.active = True
            return self.active
        else:
            print("Wrong password")

    def logout(self):
        if self.active and os.path.exists(f"{WRKDIR}Logged_in"):
            os.remove(f"{WRKDIR}Logged_in")
            self.active = False
            return None
        

    def add_passwords(self):
        if self.active:
            website = input("Enter the name of the website --> ")
            username = input("Enter username/email --> ")
            length = int(input("Choose password length 8-24 --> "))
            created_at = datetime.now()
            if length > 8 and length < 24:
                password = pwd.genword(length=length, charset='ascii_72')
                self.passwords[website] = password
                data = (website, username, password, created_at)
                db.add_PW_to_table(data)
                return True
            else:
                print("Password must be between 8 and 24 characters")

    def select_pw(self, website):
        db.select_pw(website)
     
    def display_all_passwords(self):
        db.view_pws()
        if not self.active:
            print("Must enter password.")

    def display_websites(self):
        db.view_sites()
        if not self.active:
            print("Must enter password.")

    def reset(self):
        try:
            shutil.rmtree(WRKDIR)
        except FileNotFoundError:
            print("You cannot destroy that which never was.")