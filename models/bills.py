import json

class Ordersbill:
    def __init__(self):
        self.file_path = "database/currentorders.json"

    def load_all_orders(self):
        try:
            with open(self.file_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            with open("logs/log.txt","a") as file:
                file.write(f"error will be {e}")
            return []

     
    def print_bill(self):
        intp = input("Enter your mobile number or order ID: ").strip()
        data = self.load_all_orders()
        found = False

        for order in data:
            if order.get("order_id") == intp or order.get("mobile") == intp:
                found = True
                print("\n" + "=" * 40)
                print("        WELCOME TO APNA RESTAURANT")
                print("-"*40)
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
                    print(f"{name:20} {qty:>3} {rate:>6} {amt:>7}")

                print("-" * 40)
                print(f"{'Subtotal':>30} : ₹{order.get('base_total')}")
                print(f"{'GST':>30} : ₹{order.get('gst')}")
                print(f"{'TOTAL':>30} : ₹{order.get('total_price')}")
                print(f"{'Payment Status':>30} : {order.get('status').capitalize()}")
                print("=" * 40)
                print("         .Thank You! Visit Again.")
                print("            ..................")
                print("")
                print("=" * 40)
                break

        if not found:
            print(" Order not found. Please check the number or order ID.")


 