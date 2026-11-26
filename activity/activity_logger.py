import os
import csv
from datetime import datetime

class ActivityLogger:
    def __init__(self, username="default_user", filename=None, folder_name="activity"):
        self.folder_path = os.path.join(os.path.dirname(__file__), '..', folder_name)
        os.makedirs(self.folder_path, exist_ok=True)
        
        if not filename:
            filename = f"activity_log_{username}.csv"
            
        self.file_path = os.path.join(self.folder_path, filename)
        
        if not os.path.exists(self.file_path):
            with open(self.file_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Timestamp", "Username", "Transaction Type", "Category", "Amount", "Description"])

    def log_transaction(self, username, trans_type, category, amount, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.file_path, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Using 'Rs.' to prevent character encoding/mojibake issues in Excel
                writer.writerow([timestamp, username, trans_type, category, f"Rs. {amount:,.2f}", description])
        except Exception as e:
            print(f"Error logging transaction to CSV: {e}")