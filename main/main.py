import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from database.db_manager import DatabaseManager
from gui.auth_window import AuthWindow
from gui.dashboard import DashboardWindow

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def on_login_success(user_id, username):
    dashboard_root = ctk.CTk()
    db_manager = DatabaseManager()
    DashboardWindow(dashboard_root, user_id, username, db_manager)
    dashboard_root.mainloop()

def main():
    root = ctk.CTk()
    db_manager = DatabaseManager()
    AuthWindow(root, db_manager, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()