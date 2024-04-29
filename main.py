from user import User
import os

NAME = os.getlogin()
WRKDIR = f"/home/{NAME}/.localpwm/"

def main():
    user = User()
    for i in range(3):
        if user.active == False and not os.path.exists(f"{WRKDIR}Logged_in"):
            user.login()
        elif os.path.exists(f"{WRKDIR}Logged_in"):
            user.active = True
        if i > 3:
            print("Too many failed attempts")
            break
        
    while user.active:
        choice = input("What would you like to do? --> ").lower()

        match choice:
            case "add":
                user.add_passwords()
            case "view -a":
                user.display_all_passwords()
            case "view":
                user.display_websites()
            case "logout":
                user.logout()
                break
            case "red button":
                user.reset()
                user.logout()
        if choice.startswith("select"):
            website = choice[7:]
            print(f"{website.upper()} copied to clipboard")
            user.select_pw(website)
if __name__ == "__main__":
    main()

