from service.authantication import UserChoice, AdminChoice, Authentication 
from datetime import datetime
from logs import log

def main():
    auth = Authentication()

    while True:
        print("\n" + "HI WELCOME TO APNA RESTAURANT!".center(150))
        print("Select any option according to your role:".center(150))
        print("1. Admin Login".center(150))
        print("2. Staff Login".center(150))
        print("3. Staff Signup".center(150))
        print("0. Exit".center(150))

        try:
            choice = input("Enter your choice: ").strip()

            if not choice.isdigit():
                raise ValueError("Please enter a valid number between 0 and 3.")
            choice = int(choice)

            if choice == 1:
                print("Admin Login".center(150))
                auth.login_user("admin")  # replaces search_user()

            elif choice == 2:
                print("Staff Login".center(150))
                auth.login_user("staff")  # replaces search_staff()

            elif choice == 3:
                print("Staff Registration".center(150))
                auth.register_user("staff")  # replaces register_staff()

            elif choice == 0:
                print("Thank you! Exiting...".center(150))
                break

            else:
                print("Invalid option! Try again.".center(150))

        except ValueError as e:
            log.error_log(e)
            print(f"Error: {e}. Please enter a valid number between 0 and 3.".center(150))

        except Exception as e:
            log.error_log(e)
            print(f"An error occurred: {e}. Please try again.".center(150))

main()
