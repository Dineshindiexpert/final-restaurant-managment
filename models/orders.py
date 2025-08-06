import json
from logs import log

class Orders:
    # You can choose a consistent file name or adjust as needed
    FILE_PATH = "database/currentorders.json"

    @staticmethod
    def load_orders():
        """Load orders from the file."""
        try:
            with open(Orders.FILE_PATH, "r") as file:
                return json.load(file)
        except FileNotFoundError as e:
            showerror="on the search file paht in the  load_orders() fun."
            log.error_log(e,showerror)
            return []
        except json.JSONDecodeError as e:
        
            log.error_log(e,showerror)
            return []

    @staticmethod
    def save_orders(orders):
        """Save orders to the file."""
        try:
            with open(Orders.FILE_PATH, "w") as file:
                json.dump(orders, file, indent=4)
        except Exception as e:
            showerror="on the save file of previous orders in the database of perviousorders.json"
            log.error_log(f"Failed to save orders: {e}",showerror)
