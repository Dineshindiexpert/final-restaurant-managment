from service.authantication import Authentication



print("HI WELCOME TO APNA RESTAURANT!".center(150))
print("Select any option according to your role :".center(150))

print("1. Admin login. ".center(150))
print("2. Staff login.".center(150))
print("3. singup staff.".center(150))
print("0. for the exit.".center(150))
auth = Authentication()  


while True:
    try:

        choice = int(input("Enter your choice: ").center(150))

        if choice == 1:
            role = "admin"
            auth.search_user(role) 
            
        elif choice == 2:
            role = "staff"
            auth.search_staff(role)
        elif choice==3:
            auth.register_staff()

        elif choice==0:
            break
    
        else:
            print("Invalid option! Try again.".center(150))
    except Exception  as e:
        with open("logs/log.txt","a") as file:
            file.write(f"the error will be{e} in the main file. ")
            print("Please enter a number (1 or 2).".center(150))
     
