import json
from logs import log
from reports.Reports import ReportsManagement  
from service.booking_service import Orders   
 
 

class Payment:
    def __init__(self):
        pass

    import json

    def process_payment(self):
        print("press 1 for the cash.")
        print("")
        try:
            # Step 1: Get valid Order ID or Mobile No
            id = input("Enter the Order ID or Mobile No: ").strip()

            if not id:
                print("Order ID or Mobile number cannot be empty.")
                return

            orders = Orders()
            current_orders = orders.load_orders("database/currentorders.json")

            matched_order = None

            # Step 2: Find the order
            for order in current_orders:
                if order['order_id'] == id or order['mobile'] == id:
                    matched_order = order
                    break

            if matched_order:
                # Step 3: Print bill
                print("\n" + "="*40)
                print("                 APNA RESTAURANT".center(40))
                print("="*40)
                print(f"Order ID      : {matched_order['order_id']}")
                print(f"Mobile No     : {matched_order['mobile']}")
                print("="*40)
                print("Items Purchased:")
                print("-" * 40)

                max_dish_length = max(len(item['dish']) for item in matched_order['items'])
                header_format = "{:<" + str(max_dish_length) + "} {:<8} {:<10} {:<10}"
                item_format = "{:<" + str(max_dish_length) + "} {:<8} {:<10} ₹{:<10.2f}"

                print(header_format.format("Dish", "Portion", "Qty", "Price"))
                print("-" * 40)

                for item in matched_order['items']:
                    dish = item['dish']
                    portion = item['portion']
                    quantity = item['quantity']
                    price = item['price']
                    subtotal = quantity * price
                    print(item_format.format(dish, portion, quantity, subtotal))

                print("-" * 40)
                print(f"Base Total     : ₹{matched_order['base_total']:.2f}")
                print(f"GST (18%)      : ₹{matched_order['gst']:.2f}")
                print(f"Total Price    : ₹{matched_order['total_price']:.2f}")
                print("=" * 40)
                print(f"Status         : {matched_order['status'].capitalize()}")
                print("=" * 40)

                # Step 4: Check status
                if matched_order['status'].lower() == 'completed':
                    print("Payment already completed. Thank you for visiting!")
                else:
                    try:
                        amount_str = input(f"Please pay ₹{matched_order['total_price']:.2f}: ₹").strip()
                        if not amount_str.replace('.', '', 1).isdigit() or float(amount_str) < 0:
                            print("Invalid amount entered.")
                            return

                        amount = float(amount_str)

                        if amount == matched_order['total_price']:
                            matched_order['status'] = 'completed'
                            print("\nPayment successful. Thank you for visiting!")

                             
                            try:
                                report_manager = ReportsManagement()
                                report_manager.update_report(matched_order)
                                print(" Report updated successfully.")
                            except Exception as e:
                                log.error_log(e)
                                print(" Error updating report data.")

                            # Save updated orders
                            with open("database/currentorders.json", "w") as file:
                                json.dump(current_orders, file, indent=4)
                        else:
                            print("\n Payment failed. Insufficient or incorrect amount.")
                    except ValueError:
                        print("Invalid input! Please enter a numeric value for payment.")
            else:
                print("No order found for the given ID or mobile number.")

        except Exception as e:
            log.error_log(e)
            print("Unexpected error occurred during payment process.")
