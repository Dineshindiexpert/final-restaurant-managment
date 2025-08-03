import json
import os
from datetime import datetime, timedelta
from logs import log

class Table:
    def __init__(self, booking_file='database/table.json', inventory_file='database/table_booking.json'):
        self.booking_file = booking_file
        self.inventory_file = inventory_file

        os.makedirs(os.path.dirname(self.booking_file), exist_ok=True)
        os.makedirs(os.path.dirname(self.inventory_file), exist_ok=True)

        if not os.path.exists(self.booking_file):
            with open(self.booking_file, 'w') as f:
                json.dump([], f, indent=4)

    def load_data(self, file_name):
        """ General method to load data from any JSON file """
        try:
            with open(file_name, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            log.error_log(f"Error loading {file_name}: {e}")
            return []

    def save_data(self, data, file_name):
        """ General method to save data to a JSON file """
        try:
            with open(file_name, 'w') as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            log.error_log(f"Error saving to {file_name}: {e}")

    def book_table_for_persons(self):
        try:
            persons = int(input("Enter number of persons: ").strip())
            hours = int(input("Enter booking duration in hours (1-3): ").strip())
            if hours < 1 or hours > 3:
                print("Duration must be between 1 and 3 hours.")
                return
        except ValueError as e:
            log.error_log(e)
            print("Invalid input. Please enter valid numbers.")
            return

        now = datetime.now()
        start_time = now
        end_time = now + timedelta(hours=hours)

        bookings = self.load_data(self.booking_file)
        inventory = self.load_data(self.inventory_file)

        suitable_tables = sorted(
            [t for t in inventory if t["seats"] >= persons],
            key=lambda x: x["seats"]
        )

        for table in suitable_tables:
            table_id = table["table_id"]
            is_conflict = False

            for b in bookings:
                if b["table_no"] == table_id:
                    st = datetime.strptime(b["start_time"], "%Y-%m-%d %H:%M:%S")
                    et = datetime.strptime(b["end_time"], "%Y-%m-%d %H:%M:%S")
                    if start_time < et and end_time > st:
                        is_conflict = True
                        break

            if not is_conflict:
                bookings.append({
                    "table_no": table_id,
                    "persons": persons,
                    "start_time": start_time.strftime('%Y-%m-%d %H:%M:%S'),
                    "end_time": end_time.strftime('%Y-%m-%d %H:%M:%S')
                })
                self.save_data(bookings, self.booking_file)
                print(f"Table {table_id} booked from {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')} for {persons} persons.")
                return

        print(f"No available table for {persons} persons at this time.")

    def cancel_table(self):
        try:
            table_no = input("Enter table number to cancel booking: ").strip()
            bookings = self.load_data(self.booking_file)

            updated = [b for b in bookings if b["table_no"] != table_no]
            if len(updated) == len(bookings):
                print(f"No active bookings found for Table {table_no}.")
            else:
                self.save_data(updated, self.booking_file)
                print(f"Booking for Table {table_no} canceled.")
        except Exception as e:
            log.error_log(e)
            print("Error canceling the table booking.")

    def show_table_status(self):
        now = datetime.now()
        inventory = self.load_data(self.inventory_file)
        bookings = self.load_data(self.booking_file)

        print("\n" + "=" * 60)
        print(f"{'Table ID':<10}{'Seats':<10}{'Status':<30}")
        print("-" * 60)

        for table in inventory:
            tid = table["table_id"]
            status = "Available"
            for b in bookings:
                if b["table_no"] == tid:
                    st = datetime.strptime(b["start_time"], '%Y-%m-%d %H:%M:%S')
                    et = datetime.strptime(b["end_time"], '%Y-%m-%d %H:%M:%S')
                    if st <= now < et:
                        status = f"Booked (till {et.strftime('%H:%M')})"
                        break
            print(f"{tid:<10}{table['seats']:<10}{status:<30}")
        print("=" * 60)

    def fetch_tables_by_seats(self):
        try:
            persons = int(input("Enter number of persons: ").strip())
        except ValueError:
            print("Please enter a valid number.")
            return

        now = datetime.now()
        inventory = self.load_data(self.inventory_file)
        bookings = self.load_data(self.booking_file)

        print("\nAvailable Tables for", persons, "persons:")

        available_tables = []
        for table in inventory:
            if table['seats'] == persons:
                table_id = table['table_id']
                is_booked = False

                for b in bookings:
                    if b["table_no"] == table_id:
                        st = datetime.strptime(b["start_time"], "%Y-%m-%d %H:%M:%S")
                        et = datetime.strptime(b["end_time"], "%Y-%m-%d %H:%M:%S")
                        if st <= now < et:
                            is_booked = True
                            break

                status = "Booked" if is_booked else "Available"
                available_tables.append((table_id, status))

        if not available_tables:
            print("No tables found with that seat capacity.")
        else:
            print("\n" + "=" * 40)
            print(f"{'Table ID':<15}{'Status':<20}")
            print("-" * 40)
            for tid, status in available_tables:
                print(f"{tid:<15}{status:<20}")
            print("=" * 40)
