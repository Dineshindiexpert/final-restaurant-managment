import os
from service.menu import MenuManager
from models.table import Table
from service.payment_service import Payment
from models.bills import Ordersbill
from service.booking_service import Orders
from reports.Reports import ReportsManagement
from logs import log

 
menu_manager = MenuManager()
table_manager = Table()  # This now refers to your updated Table class
orders_manager = Orders()
payment_manager = Payment()
ordersbill_manager = Ordersbill()

class AdminChoice:
    @staticmethod
    def admin_choices():
        while True:
            print("\n--- Admin Menu ---")
            print("1. List Dishes")
            print("2. Add Dish")
            print("3. Delete Dish")
            print("4. Manage Tables")
            print("5. Show All Order Status")
            print("6. Place an Order")
            print("7. Process Payment")
            print("8. Print Receipt")
            print("9. Generate Reports")
            print("0. Exit")

            try:
                choice = int(input("Enter your choice (0-9): "))
            except ValueError as e:
                errorshow ="admin menu"
                log.error_log(e,errorshow)
                print("Invalid input! Please enter a number.")
                continue

            if choice == 1:
                menu_manager.list_dishes()

            elif choice == 2:
                AdminChoice.add_dishes_loop()

            elif choice == 3:
                try:
                    dish_name = input("Enter dish name to delete: ").strip()
                    menu_manager.delete_dish(dish_name)
                except Exception as e:
                    showerror="amin menu choice (delete dish.)"
                    log.error_log(e,showerror)
                    print("Error deleting dish.")

            elif choice == 4:
                AdminChoice.manage_tables()

            elif choice == 5:
                try:
                    orders_manager.view_orders()
                except Exception as e:
                    showerror="admin menu on the  view_orders "
                    log.error_log(e,showerror)
                    print("Error displaying orders.")

            elif choice == 6:
                try:
                    orders_manager.take_order()
                except Exception as e:
                    showerror="on the take_order() fun "
                    log.error_log(e,showerror)
                    print("Error placing order.")

            elif choice == 7:
                try:
                    payment_manager.process_payment()
                except Exception as e:
                    showerror="on the process payment.(process_payment())"
                    log.error_log(e),showerror
                    print("Error processing payment.")

            elif choice == 8:
                try:
                    ordersbill_manager.print_bill()
                except Exception as e:
                    showerror="on the print bill "
                    log.error_log(e,showerror)
                    print("Error printing bill.")

            elif choice == 9:
                try:
                    ob= ReportsManagement()
                    ob.reports_maker()
                except Exception as e:
                    showerror="reports making = (reportmaker())"
                    log.error_log(e,showerror)
                    print("Error generating report.")

            elif choice == 0:
                print("Exiting admin menu.")
                break

            else:
                print("Invalid choice! Please enter a number between 0 and 9.")

    @staticmethod
    def manage_tables():
        while True:
            print("\n--- Table Management ---")
            print("1. Show All Table Status")
            print("2. Book Table")
            print("3. Cancel Table")
            print("0. Back to Main Menu")

            try:
                choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue

            if choice == 1:
                table_manager.show_table_status()

            elif choice == 2:
                table_manager.book_table_for_persons()

            elif choice == 3:
                table_manager.cancel_table()

            elif choice == 0:
                break

            else:
                print("Invalid choice!")

    @staticmethod
    def add_dishes_loop():
        while True:
            name = input("Enter dish name: ")
            category = input("Enter category: ")
            try:
                half_price = float(input("Enter half plate price: "))
                full_price = float(input("Enter full plate price: "))
            except Exception as e:
                showerror="in the add dish on pice input ."
                log.error_log(e,showerror)
                print("Invalid price input.")
                continue

            description = input("Enter description: ")
            menu_manager.add_dish(name, category, half_price, full_price, description)

            cont = input("Do you want to add another dish? (yes/no): ").strip().lower()
            if cont in ['no', 'n']:
                break
            elif cont not in ['yes', 'y']:
                print("Invalid input. Returning to menu...")
                break


class UserChoice:
    def __init__(self):
        self.menu_manager = MenuManager()
        self.orders_manager = Orders()
        self.payment_manager = Payment()
        self.ordersbill_manager = Ordersbill()

    def user_choices(self):
        while True:
            print("\n--- User Menu ---")
            print("1. View Menu")
            print("2. Take Order")
            print("3. Make Payment")
            print("4. Table Management")
            print("5. Print Receipt")
            print("0. Exit")

            try:
                choice = int(input("Enter your choice (0-5): "))
            except Exception as e:
                showeror="in the staff input."
                log.error_log(e,showeror)
                print("Invalid input! Please enter a number.")
                continue

            if choice == 1:
                self.menu_manager.list_dishes()

            elif choice == 2:
                self.orders_manager.take_order()

            elif choice == 3:
                self.payment_manager.process_payment()

            elif choice == 4:
                AdminChoice.manage_tables()

            elif choice == 5:
                try:
                    self.ordersbill_manager.print_bill()
                except Exception as e:
                    showeror='in the print_bill() by the staff'
                    log.error_log(e,showeror)
                    print(f"Error printing bill !")

            elif choice == 0:
                print("Thank you for visiting!")
                break

            else:
                print("Invalid choice. Please select from the menu.")



