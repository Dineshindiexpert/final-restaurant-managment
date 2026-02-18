import json
import os
import re
import pwinput
from logs import log
from choice.adminchoice import AdminChoice, UserChoice

class Authentication:
    def __init__(self, filename='database/user.json'):
        self.filename = filename
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)

        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                json.dump([], file, indent=4)

    def register_user(self, role="staff"):
        """ Register user without hashing """
        try:
            user_id = input(f"Enter your {role} ID: ")
            password = pwinput.pwinput(prompt="Enter your password: ", mask="*")

            user_data = {
                "id": user_id,
                "password": password,
                "status": role
            }

            self.save_user(user_data)
        except Exception as e:
            showerror="on the register_user() function on the Authentication class on the authanticaiotn.py"
            log.error_log(e,showerror)
            print("Invalid input!")

    def save_user(self, user_data):
        existing_data = self.load_users()
        for user in existing_data:
            if user["id"] == user_data["id"]:
                print(f"User with ID '{user_data['id']}' already exists.")
                return
        existing_data.append(user_data)
        self.write_users(existing_data)
        print(f"User '{user_data['id']}' registered successfully!")

    def load_users(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except Exception as e:
            showerror="in the load user in the Authentication on the authentication.py"
            log.error_log(e,showerror)
            print(f"Error reading user file !")
            return []

    def write_users(self, data):
        try:
            with open(self.filename, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            showerror="in the write_users in the Authentication class on the authenctcation.py"
            log.error_log(e,showerror)
            print(f"Error writing to user file !")

    def login_user(self, role):
        """ Login user with plain password check """
        print("HI, WELCOME TO APNA RESTAURANT!")
        users = self.load_users()

        try:
            user_id = input(f"Enter your {role} ID: ")
            password = pwinput.pwinput(prompt="Enter your password: ", mask="*")

            for user in users:
                if user["id"] == user_id and user["password"] == password and user['status'] == role:
                    print(f"User {user_id} successfully logged in as {role}.")

                    if role == "admin":
                        AdminChoice().admin_choices()
                    elif role == "staff":
                        UserChoice().user_choices()
                    return True

            print(f"No matching {role} user found!")
            return False
        except Exception as e:
            showeror="on the login_user in the Authentication class on the authentication.py"
            log.error_log(e,showeror)
            print("Invalid input!")
            return False
