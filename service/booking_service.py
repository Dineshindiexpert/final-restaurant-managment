import json
import os
from service.menu import MenuManager
from datetime import datetime
from logs import log

class Orders:
    def __init__(self, orders_file='database/currentorders.json', previous_orders_file='database/previousorders.json', menu_file='database/menu.json'):
        self.orders_file = orders_file
        self.previous_orders_file = previous_orders_file
        self.menu_file = menu_file

        # Ensure the orders file exists
        self._ensure_file_exists(self.orders_file)
        self._ensure_file_exists(self.previous_orders_file)

    def _ensure_file_exists(self, file_name):
        """ Ensure the file exists, create if it doesn't """
        if not os.path.exists(file_name):
            with open(file_name, 'w') as file:
                json.dump([], file, indent=4)

    def load_menu(self):
        """ Load the menu from the menu file """
        try:
            with open(self.menu_file, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error loading menu: {e}")
            return []

    def load_orders(self, file_name):
        """ Load orders from a given file """
        try:
            with open(file_name, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError) as e:
            log.error_log(e)
            print(f"Error loading orders from {file_name}.")
            return []

    def save_orders(self, orders, file_name):
        """ Save orders to a file """
        try:
            with open(file_name, 'w') as file:
                json.dump(orders, file, indent=4)
        except IOError as e:
            log.error_log(e)
            print(f"Error saving orders to {file_name}: {e}")

    def move_order_to_previous(self, order_id):
        """ Move a completed order from current orders to previous orders """
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

    def process_payment(self, order_id):
        """ Process payment for an order and move it to previous orders """
        current_orders = self.load_orders(self.orders_file)

        order_to_process = None
        for order in current_orders:
            if order['order_id'] == order_id:
                if order['status'] == 'completed':
                    print(f"Order {order_id} has already been paid for.")
                    return
                order_to_process = order
                break

        if order_to_process:
            print(f"Processing payment for Order {order_id}...")
            order_to_process['status'] = 'completed'
            self.move_order_to_previous(order_id)
        else:
            print(f"Order ID {order_id} not found in current orders.")

    def take_order(self):
        """ Take a new order, generate an order ID, and print the bill """
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
            dish_entry = next(
                (item for item in menu if item.get('name', '').lower() == dish_name.lower()),
                None
            )

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
                log.error_log(e)
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

        # Generate order ID
        orders = self.load_orders(self.orders_file)
        next_id = f"O{len(orders) + 1:03d}"

        # Calculate totals
        base_total = sum(item["price"] * item["quantity"] for item in order_items)
        gst = base_total * 0.18  # 18% GST
        total_price = base_total + gst

        # Save the new order
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

        # Generate and print receipt
        self.generate_receipt(order_data)

    def cancel_order(self, identifier):
        """ Cancel an order by order ID or mobile number """
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
        """ Display the list of current orders """
        orders = self.load_orders(self.orders_file)

        if not orders:
            print("No orders to display.")
            return

        # Define column widths
        order_id_width = 10
        mobile_width = 12
        status_width = 10
        total_width = 10
        items_label = "Items"

        # Print header
        print("=" * 150)
        print(f"{'Order ID':<{order_id_width}} | {'Mobile':<{mobile_width}} | {'Status':<{status_width}} | {'Total':<{total_width}} | {items_label}")
        print("=" * 150)

        for order in orders:
            # First item line with order details
            first_item = order['items'][0] if order['items'] else None
            item_str = f"{first_item['dish']} ({first_item['portion']}) x{first_item['quantity']}" if first_item else "No items"
            print(f"|| {order['order_id']:<{order_id_width}} | {order['mobile']:<{mobile_width}} | {order['status']:<{status_width}} | ₹{order['total_price']:<{total_width - 1}.2f} | {item_str}")

            # Print the rest of the items aligned under "Items"
            for item in order['items'][1:]:
                indent = ' ' * (order_id_width + mobile_width + status_width + total_width + 13)  # extra for separators and ₹
                item_str = f"{item['dish']} ({item['portion']}) x{item['quantity']}"
                print(f"{indent}{item_str}")

            print("-" * 150)

    def generate_receipt(self, order_data):
        """ Generate a formatted receipt for the order """
        print("\n" + "=" * 45)
        print(f"{'Apna Restaurant':^45}")
        print("=" * 45)
        print(f"Order ID: {order_data['order_id']}")
        print(f"Mobile: {order_data['mobile']}")
        print("-" * 45)
        for item in order_data['items']:
            print(f"{item['dish']} ({item['portion']}) x{item['quantity']} - ₹{item['price'] * item['quantity']:.2f}")
        print("-" * 45)
        print(f"GST (18%): ₹{order_data['gst']:.2f}")
        print(f"Total Price: ₹{order_data['total_price']:.2f}")
        print("=" * 45)
