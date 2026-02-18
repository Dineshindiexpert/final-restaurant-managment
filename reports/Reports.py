import json
import os
from logs import log

class ReportsManagement:
    def __init__(self, report_file='database/reports.json'):
        self.report_file = report_file
        self._ensure_report_file()

    def _ensure_report_file(self):
        if not os.path.exists(self.report_file):
            with open(self.report_file, 'w') as f:
                json.dump({
                    "total_sales": 0.0,
                    "items_sold": {}
                }, f, indent=4)

    def load_report(self):
        try:
            with open(self.report_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            showerror="on the load reports."
            log.error_log(e,showerror)
            print("Failed to load reports.")
            return {
                "total_sales": 0.0,
                "items_sold": {}
            }

    def save_report(self, report_data):
        try:
            with open(self.report_file, 'w') as f:
                json.dump(report_data, f, indent=4)
        except Exception as e:
            showerror="on the savereprots"
            log.error_log(e,showerror)
            print("Failed to save report data.")

    def update_report(self, order_data):
        """ Update the report based on a completed order """
        report = self.load_report()

        # Update total sales
        report["total_sales"] += order_data["total_price"]

        # Update item counts
        for item in order_data["items"]:
            name = item["dish"]
            quantity = item["quantity"]
            if name in report["items_sold"]:
                report["items_sold"][name] += quantity
            else:
                report["items_sold"][name] = quantity

        self.save_report(report)

    def reports_maker(self):
        """ Display the full turnover and most sold items """
        report = self.load_report()

        print("\n" + "=" * 50)
        print(f"{'SALES REPORT':^50}")
        print("=" * 50)
        print(f"{'Total revenue:':<30} ₹{report['total_sales']:.2f}")
        print("-" * 50)

        if not report['items_sold']:
            print("No items sold yet.")
            return

        print(f"{'Dish':<30} | {'Qty Sold'}")
        print("-" * 50)
        sorted_items = sorted(report['items_sold'].items(), key=lambda x: x[1], reverse=True)

        for name, qty in sorted_items:
            print(f"{name:<30} | {qty}")
        print("=" * 50)
