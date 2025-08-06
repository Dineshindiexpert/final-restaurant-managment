from datetime import datetime

def error_log(e,where):
    with open("logs/log.txt", "a") as file:
        file.write(f"THE ERROR IS: {e}\n on this: {datetime.now()}\n")
        file.write(f" on this{ where}")


 