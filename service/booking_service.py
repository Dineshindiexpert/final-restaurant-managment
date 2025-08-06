import json
import os
from datetime import datetime
from service.menu import MenuManager
from logs import log


class Orders:
    def __init__(self, orders_file='database/currentorders.json', previous_orders_file='database/previousorders.json', menu_file='database/menu.json'):
        self.orders_file = orders_file
        self.previous_orders_file = previous_orders_file
        self.menu_file = menu_file

        self._ensure_file_exists(self.orders_file)
        self._ensure_file_exists(self.previous_orders_file)

    def _ensure_file_exists(self, file_name):
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                json.dump([], file, indent=4)

    def load_menu(self):
        try:
            with open(self.menu_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            showerror="on the load menu fun class is orders on the booking_service.py"
            log.error_log(e,showerror)
            print(f"Error loading menu !")
            return []

    def load_orders(self, file_name):
        try:
            with open(file_name, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            showerror="on the load_orders in the class orders on the booking_service.py"
            log.error_log(e,showerror)
            print(f"Error loading orders from {file_name}.")
            return []

    def save_orders(self, orders, file_name):
        try:
            with open(file_name, 'w') as file:
                json.dump(orders, file, indent=4)
        except IOError as e:
            showerror="on the save_orders() in the orders class on the booking_service.py"
            log.error_log(e,showerror)
            print(f"Error saving orders to {file_name}: {e}")

    def move_order_to_previous(self, order_id):
        current_orders = self.load_orders(self.orders_file)
        previous_orders = self.load_orders(self.previous_orders_file)

        order_to_move = None
        for order in current_orders:
            if order['order_id'] == order_id:
                order_to_move = order
                break

        if order_to_move:
            previous_orders.append(order_to_move)
            current_orders = [order for order in current_orders if order['order_id'] != order_id]
            self.save_orders(previous_orders, self.previous_orders_file)
            self.save_orders(current_orders, self.orders_file)
            print(f"Order {order_id} has been moved to previous orders.")
        else:
            print(f"No such order found with ID {order_id}.")

    def update_report(self, order_data):
        report_path = 'database/reports.json'

        # Create report if it doesn't exist
        if not os.path.exists(report_path):
            report_data = {"total_sales": 0, "most_sold_dishes": {}}
        else:
            try:
                with open(report_path, 'r') as f:
                    report_data = json.load(f)
            except json.JSONDecodeError:
                report_data = {"total_sales": 0, "most_sold_dishes": {}}

        # Update total sales
        report_data["total_sales"] += order_data["total_price"]

        # Update most sold dishes
        for item in order_data["items"]:
            dish = item["dish"]
            qty = item["quantity"]
            report_data["most_sold_dishes"][dish] = report_data["most_sold_dishes"].get(dish, 0) + qty

        # Save updated report
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=4)

        print("Report updated successfully.")

    def process_payment(self, order_id):
        current_orders = self.load_orders(self.orders_file)

        order_to_process = None
        for order in current_orders:
            if order['order_id'] == order_id or order['mobile'] == order_id:
                if order['status'] == 'completed':
                    print(f" Order {order['order_id']} has already been paid.")
                    return
                order_to_process = order
                break

        if not order_to_process:
            print(f" Order ID or mobile number '{order_id}' not found.")
            return

        self.generate_receipt(order_to_process)

        try:
            amount_input = input(f"\nEnter payment amount (₹{order_to_process['total_price']:.2f}): ₹").strip()
            amount = float(amount_input)
            if amount != order_to_process['total_price']:
                print(" Incorrect amount. Payment failed.")
                return
        except ValueError:
            print(" Invalid amount. Payment must be a number.")
            return

        order_to_process['status'] = 'completed'
        self.save_orders(current_orders, self.orders_file)
        self.move_order_to_previous(order_to_process['order_id'])
        self.update_report(order_to_process)

        print(" Payment successful and report updated.")

    def take_order(self):
        menu_manager = MenuManager()
        menu = menu_manager.list_dishes()

        if not menu:
            print("Menu is empty or not available.")
            return

        mobile = input("Enter your mobile number: ").strip()
        if not mobile.isdigit() or len(mobile) != 10:
            print("Invalid mobile number. Please enter a 10-digit number.")
            return

        order_items = []

        while True:
            dish_name = input("Enter Dish Name: ").strip()
            dish_entry = next((item for item in menu if item.get('name', '').lower() == dish_name.lower()), None)

            if not dish_entry:
                print(f"Dish '{dish_name}' not found in the menu.")
                continue

            portion = input("Enter portion size (half/full): ").strip().lower()
            if portion == 'half':
                price = dish_entry.get('half_price')
            elif portion == 'full':
                price = dish_entry.get('full_price')
            else:
                print("Invalid portion size. Please enter 'half' or 'full'.")
                continue

            try:
                quantity = int(input("Enter Quantity: ").strip())
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
            except Exception as e:
                showerror="on the booking_error/take_orders() in the orders class."
                log.error_log(e,showerror)
                print("Invalid quantity. Please enter a valid number.")
                continue

            order_items.append({
                "dish": dish_entry['name'],
                "portion": portion,
                "quantity": quantity,
                "price": price
            })

            more = input("Do you want to add another dish? (yes/no): ").strip().lower()
            if more != 'yes':
                break

        if not order_items:
            print("No items were added to the order.")
            return

        orders = self.load_orders(self.orders_file)
        next_id = f"O{len(orders) + 1:03d}"

        base_total = sum(item["price"] * item["quantity"] for item in order_items)
        gst = base_total * 0.18
        total_price = base_total + gst

        order_data = {
            "order_id": next_id,
            "mobile": mobile,
            "items": order_items,
            "status": "pending",
            "base_total": base_total,
            "gst": gst,
            "total_price": total_price,
            "datetime": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        orders.append(order_data)
        self.save_orders(orders, self.orders_file)
        self.generate_receipt(order_data)

    def cancel_order(self, identifier):
        orders = self.load_orders(self.orders_file)
        found = False

        for order in orders:
            if order["order_id"] == identifier or order["mobile"] == identifier:
                if order["status"] == "completed":
                    print(f"Order {identifier} has already been completed and cannot be canceled.")
                    return
                order["status"] = "canceled"
                found = True
                print(f"Order {order['order_id']} has been canceled for mobile {order['mobile']}.")
                break

        if not found:
            print(f"No order found with ID or mobile: {identifier}")
            return

        self.save_orders(orders, self.orders_file)

        def view_orders(self):
            orders = self.load_orders(self.orders_file)

            if not orders:
                print("No orders to display.")
                return

            order_id_width = 10
            mobile_width = 12
            status_width = 10
            total_width = 12
            items_label = "Items"

            print("=" * 90)
            print(f"{'Order ID':<{order_id_width}} | {'Mobile':<{mobile_width}} | {'Status':<{status_width}} | {'Total':<{total_width}} | {items_label}")
            print("=" * 90)

            for order in orders:
                first_item = order['items'][0] if order['items'] else None
                item_str = f"{first_item['dish']} ({first_item['portion']}) x{first_item['quantity']}" if first_item else "No items"
                print(f"{order['order_id']:<{order_id_width}} | {order['mobile']:<{mobile_width}} | {order['status']:<{status_width}} | ₹{order['total_price']:<{total_width}.2f} | {item_str}")

            print("=" * 90)

        def generate_receipt(self, order):
            print("\n" + "="*40)
            print(f"RECEIPT - Order ID: {order['order_id']}")
            print(f"Date & Time: {order['datetime']}")
            print(f"Mobile: {order['mobile']}")
            print("-"*40)
            print(f"{'Dish':20} {'Portion':8} {'Qty':4} {'Price':7}")
            print("-"*40)
            for item in order['items']:
                dish = item['dish']
                portion = item['portion']
                qty = item['quantity']
                price = item['price'] * qty
                print(f"{dish:20} {portion:8} {qty:<4} ₹{price:<7.2f}")
            print("-"*40)
            print(f"{'Subtotal':34} ₹{order['base_total']:.2f}")
            print(f"{'GST (18%)':34} ₹{order['gst']:.2f}")
            print(f"{'Total':34} ₹{order['total_price']:.2f}")
            print("="*40 + "\n")
