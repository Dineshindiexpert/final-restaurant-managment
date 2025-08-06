import json
import os
from logs import log

class MenuManager:
    def __init__(self, menu_file='database/menu.json'):
        self.menu_file = menu_file
        
        if not os.path.exists(self.menu_file):
            with open(self.menu_file, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4)

    def load_menu(self):
        """Load the menu from the JSON file."""
        try:
            with open(self.menu_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            showeror="on the load_menu()in the class MenuManager on the menu.py"
            log.error_log(e,showeror)
            print(f"Error loading menu !")
            return []

    def save_menu(self, menu):
        """Save the updated menu back to the JSON file."""
        try:
            with open(self.menu_file, 'w', encoding='utf-8') as f:
                json.dump(menu, f, indent=4)
        except Exception as e:
            showerror="on the save_ORDERS() IN THE CLASS MenuManager on menu.py"
            log.error_log(e,showerror)
            print(f"Error saving menu !")

    def list_dishes(self):
        """Print and return the list of dishes from the menu."""
        try:
            menu_data = self.load_menu()

            if not menu_data:
                print("Menu is empty.")
                return []

            # Flatten dishes and attach category
            dishes = []
            if isinstance(menu_data, dict):
                for category, items in menu_data.items():
                    for item in items:
                        item_with_category = item.copy()
                        item_with_category["category"] = category
                        dishes.append(item_with_category)
            elif isinstance(menu_data, list):
                dishes = menu_data

            # Column widths
            no_width = 4
            name_width = 25
            category_width = 15
            half_price_width = 14
            full_price_width = 14
            desc_width = 60

            total_width = (
                no_width + name_width + category_width +
                half_price_width + full_price_width + desc_width + 21
            )

            # Header
            print("*" * total_width)
            print(f"* {'No':<{no_width}} | {'Name':<{name_width}} | {'Category':<{category_width}} | {'Half Price (Rs)':>{half_price_width}} | {'Full Price (Rs)':>{full_price_width}} | {'Description':<{desc_width}} *")
            print("-" * total_width)

            for i, dish in enumerate(dishes, start=1):
                name = dish.get('name', '')[:name_width]
                category = dish.get('category', '')[:category_width]
                half_price = f"RS.{dish.get('half_price', 0):.2f}"
                full_price = f"RS.{dish.get('full_price', 0):.2f}"
                description = dish.get('description', '')[:desc_width]

                print(f"* {i:<{no_width}} | {name:<{name_width}} | {category:<{category_width}} | {half_price:>{half_price_width}} | {full_price:>{full_price_width}} | {description:<{desc_width}} *")

            print("*" * total_width)
            return dishes

        except (FileNotFoundError, json.JSONDecodeError) as e:
            showerror="on the list_dish() on menu.py"
            log.error_log(e,showerror)
            print(f"Error reading menu: {e}")
            return []

    def add_dish(self, name, category, half_price, full_price, description):
        """Add a new dish to the menu with validation."""
        try:
            # Ensure prices are valid numbers
            half_price = float(half_price)
            full_price = float(full_price)

            if half_price <= 0 or full_price <= 0:
                print("Price values must be greater than zero.")
                return

        except ValueError:
            log.error_log("Invalid price value entered.")
            print("Invalid price value. Please enter numeric values for prices.")
            return

        if not name or not category or not description:
            print("Dish name, category, and description cannot be empty.")
            return

        menu = self.load_menu()

        # Check if the dish already exists in the menu
        for dish in menu:
            if dish['name'].lower() == name.lower():
                print(f"Dish '{name}' already exists.")
                return

        # Add the new dish
        menu.append({
            "name": name,
            "category": category,
            "half_price": half_price,
            "full_price": full_price,
            "description": description
        })
        self.save_menu(menu)
        print(f"Dish '{name}' added to the menu.")

    def delete_dish(self, name):
        """Delete a dish from the menu by its name with validation."""
        if not name:
            print("Dish name cannot be empty.")
            return

        menu = self.load_menu()
        dish_found = False

        # Check if the dish exists in the menu and delete it
        for dish in menu:
            if dish['name'].lower() == name.lower():
                menu.remove(dish)
                self.save_menu(menu)
                print(f"Dish '{name}' deleted from the menu.")
                dish_found = True
                break

        if not dish_found:
            print(f"Dish '{name}' not found in the menu.")

