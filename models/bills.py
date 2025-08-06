import json
from logs import log

class Ordersbill:
    FILE_PATH = "database/currentorders.json"  # Constant for file path

    def load_all_orders(self):
        try:
            with open(self.FILE_PATH, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            showeror="on the file read of currentorder json file ."
            log.error_log(e,showeror)
            return []

    def print_bill(self):
        try:
            intp = input("Enter your mobile number or order ID: ").strip()
            data = self.load_all_orders()

            # Search for the order
            for order in data:
                if order.get("order_id") == intp or order.get("mobile") == intp:
                    # Order found, print the bill
                    print("\n" + "=" * 40)
                    print("        WELCOME TO APNA RESTAURANT")
                    print("-" * 40)
                    print("        123 Food Street, Flavor Town")
                    print("           Phone: +91-9876xxxxxx")
                    print("=" * 40)
                    print(f"Order ID   : {order.get('order_id')}")
                    print(f"Mobile     : {order.get('mobile')}")
                    print(f"Date/Time  : {order.get('datetime')}")
                    print("-" * 40)
                    print(f"{'Item':20} {'Qty':>3} {'Rate':>6} {'Amt':>7}")
                    print("-" * 40)

                    for item in order.get("items", []):
                        name = f"{item['dish']} ({item['portion']})"
                        qty = item['quantity']
                        rate = item['price']
                        amt = qty * rate
                        print(f"{name:20} {qty:>3} {rate:>6.2f} {amt:>7.2f}")  # Ensure 2 decimal places for currency

                    print("-" * 40)
                    print(f"{'Subtotal':>30} : ₹{order.get('base_total'):>7.2f}")
                    print(f"{'GST':>30} : ₹{order.get('gst'):>7.2f}")
                    print(f"{'TOTAL':>30} : ₹{order.get('total_price'):>7.2f}")
                    print(f"{'Payment Status':>30} : {order.get('status').capitalize()}")
                    print("=" * 40)
                    print("         .Thank You! Visit Again.")
                    print("            ..................")
                    print("=" * 40)
                    return  # Exit once the order is found

            # If no matching order was found
            print("Order not found. Please check the number or order ID.")
        
        except ValueError as e:
            showerror="on the invalid input of print bill fun .:- print_bill()"
            log.error_log(f"Invalid input: {e}",showerror)
            print("Invalid input!")
        except Exception as e:
            log.error_log(f"Error occurred while printing the bill: {e}",showerror)
            print('An error occurred!')

