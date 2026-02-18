import json
import os
from datetime import datetime, timedelta
from logs import log    

class Table:
    bookingFile = "database/table.json"
    TIME_SLOTS = ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

    @classmethod
    def loadBooking(cls):
        if not os.path.exists(cls.bookingFile):
            return []
        with open(cls.bookingFile, "r") as f:
            return json.load(f)

    @classmethod
    def saveBooking(cls, bookings):
        os.makedirs(os.path.dirname(cls.bookingFile), exist_ok=True)
        with open(cls.bookingFile, "w") as f:
            json.dump(bookings, f, indent=4)

    @classmethod
    def viewAllBooking(cls):
        bookings = cls.loadBooking()
        if not bookings:
            print("No bookings yet.")
            return

        bookingDate = input("Enter date to view bookings (YYYY-MM-DD): ").strip()
        filtered = [b for b in bookings if b.get("bookingDate") == bookingDate]

        if not filtered:
            print(f"No bookings found on {bookingDate}")
            return

        print("\n------ All Bookings on", bookingDate, "------")
        for b in filtered:
            print(f"Table {b['tableNo']} | Customer: {b['customerName']} | Time Slot: {b['timeSlot']} | Duration: {b.get('duration', 1)} hr(s)")

    @staticmethod
    def isTimeOverlap(start1, duration1, start2, duration2):
        """ Check if two bookings overlap based on their start time and duration. """
        fmt = "%H:%M"
        end1 = (datetime.strptime(start1, fmt) + timedelta(hours=duration1)).time()
        end2 = (datetime.strptime(start2, fmt) + timedelta(hours=duration2)).time()
        s1 = datetime.strptime(start1, fmt).time()
        s2 = datetime.strptime(start2, fmt).time()

        # Handling time overlapping that spans midnight
        if s1 < end2 and s2 < end1:
            return True
        return False

    @classmethod
    def bookTable(cls):
        bookings = cls.loadBooking()
        allTables = list(range(1, 11))  # Tables 1 to 10

        now = datetime.now()
        bookingDate = now.strftime("%Y-%m-%d")
        start_time = now.strftime("%H:%M")

        try:
            duration = int(input("Enter how many hours to book (1-3): "))
            if not 1 <= duration <= 3:
                print("Duration must be between 1 to 3 hours.")
                return
        except ValueError as e:
            showerror=";in the book table on the fun is (booktable())."
            log.error_log(e,showerror)
            print("Invalid duration.")
            return

        availableTables = []
        for table in allTables:
            conflict = False
            for b in bookings:
                if b["bookingDate"] == bookingDate and b["tableNo"] == table:
                    if cls.isTimeOverlap(start_time, duration, b["timeSlot"], b.get("duration", 1)):
                        conflict = True
                        break
            if not conflict:
                availableTables.append(table)

        if not availableTables:
            print("No tables available for the selected time and duration.")
            return

        print("Available tables:", availableTables)
        customerName = input("Enter customer name: ").strip()

        try:
            tableNo = int(input("Enter table number to book: "))
        except ValueError as e:
            
            log.error_log(e,showerror)
            print("Invalid table number.")
            return

        if tableNo not in availableTables:
            print("Table already booked or invalid.")
            return

        dateTime = now.strftime("%Y-%m-%d %H:%M")

        bookings.append({
            "tableNo": tableNo,
            "customerName": customerName,
            "timeSlot": start_time,
            "duration": duration,
            "bookingDate": bookingDate,
            "dateTime": dateTime
        })

        cls.saveBooking(bookings)
        print(f"Table {tableNo} booked for {customerName} at {start_time} for {duration} hour(s).")

    @classmethod
    def cancelBooking(cls):
        bookings = cls.loadBooking()

        # Provide a flexible way to search bookings
        customerName = input("Enter customer name to cancel (or press Enter to view all bookings): ").strip()

        if customerName:
            filtered = [b for b in bookings if b['customerName'].lower() == customerName.lower()]
            if not filtered:
                print(f"No bookings found for customer {customerName}.")
                return
        else:
            # If no customer name is provided, show all bookings
            cls.viewAllBooking()
            return

        # Ask for further details to cancel the booking
        try:
            tableNo = int(input("Enter table number to cancel: "))
            timeSlot = input("Enter time slot to cancel (HH:MM): ").strip()
            bookingDate = input("Enter booking date (YYYY-MM-DD): ").strip()
        except ValueError as e:
            showerror="on the cancel table in the table cancel (cancelBooking().)"
            log.error_log(e,showerror)
            print("Invalid input.")
            return

        updated = [
            b for b in bookings
            if not (b["tableNo"] == tableNo and b["timeSlot"] == timeSlot and
                    b["customerName"] == customerName and b["bookingDate"] == bookingDate)
        ]

        if len(updated) == len(bookings):
            print("No matching booking found.")
        else:
            cls.saveBooking(updated)
            print(f"Booking for Table {tableNo} on {bookingDate} at {timeSlot} cancelled.")
