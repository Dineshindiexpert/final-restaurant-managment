import json
import os

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
            print(f"Error loading menu: {e}")
            return []

    def save_menu(self, menu):
        """Save the updated menu back to the JSON file."""
        try:
            with open(self.menu_file, 'w', encoding='utf-8') as f:
                json.dump(menu, f, indent=4)
        except Exception as e:
            print(f"Error saving menu: {e}")

     
    def list_dishes(self):
        """Print and return the list of dishes from the menu."""
        try:
            with open(self.menu_file, 'r') as file:
                menu_data = json.load(file)

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
            print(f"Error reading menu: {e}")
            return []


    def add_dish(self, name, category, half_price, full_price, description):
        """Add a new dish to the menu."""
        try:
            half_price = float(half_price)
            full_price = float(full_price)
        except Exception:
            print("Invalid price value. Please enter numeric values for prices.")
            return

        if half_price <= 0 or full_price <= 0:
            print("Price values must be greater than zero.")
            return

        menu = self.load_menu()

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
        """Delete a dish from the menu by its name."""
        menu = self.load_menu()
        for dish in menu:
            if dish['name'].lower() == name.lower():
                menu.remove(dish)
                self.save_menu(menu)
                print(f"Dish '{name}' deleted from the menu.")
                return
        print(f"Dish '{name}' not found in the menu.")
