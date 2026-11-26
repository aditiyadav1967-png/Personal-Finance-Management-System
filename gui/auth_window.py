import customtkinter as ctk
from tkinter import messagebox

class AuthWindow:
    def __init__(self, root, db_manager, on_login_success):
        self.root = root
        self.db_manager = db_manager
        self.on_login_success = on_login_success

        self.root.title("Personal Finance Intelligence System - Authentication")
        self.root.geometry("450x520")
        self.root.configure(fg_color="#090d16")
        
        # Enabled window resizing and full-screen maximize button
        self.root.resizable(True, True)

        self.setup_ui()

    def setup_ui(self):
        card = ctk.CTkFrame(self.root, fg_color="#1e293b", corner_radius=16)
        card.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(card, text="Finance Hub", font=("Segoe UI", 22, "bold"), text_color="#38bdf8").pack(pady=(35, 5))
        ctk.CTkLabel(card, text="Sign in or create an account to continue", font=("Segoe UI", 12), text_color="#94a3b8").pack(pady=(0, 25))

        self.tabview = ctk.CTkTabview(card, fg_color="#0f172a", segmented_button_selected_color="#2563eb", width=360, height=300)
        self.tabview.pack(padx=20, pady=10)

        self.tab_login = self.tabview.add("Login")
        self.tab_register = self.tabview.add("Register")

        # Login Tab
        ctk.CTkLabel(self.tab_login, text="Username", font=("Segoe UI", 11, "bold"), text_color="#f8fafc").pack(anchor="w", padx=20, pady=(15, 5))
        self.login_user_entry = ctk.CTkEntry(self.tab_login, width=280, height=38)
        self.login_user_entry.pack(padx=20)

        ctk.CTkLabel(self.tab_login, text="Password", font=("Segoe UI", 11, "bold"), text_color="#f8fafc").pack(anchor="w", padx=20, pady=(15, 5))
        self.login_pass_entry = ctk.CTkEntry(self.tab_login, width=280, height=38, show="*")
        self.login_pass_entry.pack(padx=20)

        ctk.CTkButton(self.tab_login, text="Login to Dashboard", font=("Segoe UI", 12, "bold"), fg_color="#2563eb", hover_color="#1d4ed8", height=40, command=self.handle_login).pack(padx=20, pady=30)

        # Register Tab
        ctk.CTkLabel(self.tab_register, text="Choose Username", font=("Segoe UI", 11, "bold"), text_color="#f8fafc").pack(anchor="w", padx=20, pady=(15, 5))
        self.reg_user_entry = ctk.CTkEntry(self.tab_register, width=280, height=38)
        self.reg_user_entry.pack(padx=20)

        ctk.CTkLabel(self.tab_register, text="Choose Password", font=("Segoe UI", 11, "bold"), text_color="#f8fafc").pack(anchor="w", padx=20, pady=(15, 5))
        self.reg_pass_entry = ctk.CTkEntry(self.tab_register, width=280, height=38, show="*")
        self.reg_pass_entry.pack(padx=20)

        ctk.CTkButton(self.tab_register, text="Create Account", font=("Segoe UI", 12, "bold"), fg_color="#16a34a", hover_color="#15803d", height=40, command=self.handle_register).pack(padx=20, pady=30)

    def handle_login(self):
        username = self.login_user_entry.get().strip()
        password = self.login_pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all login fields.")
            return

        user_id = self.db_manager.login_user(username, password)
        if user_id:
            self.root.destroy()
            self.on_login_success(user_id, username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def handle_register(self):
        username = self.reg_user_entry.get().strip()
        password = self.reg_pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please fill in all registration fields.")
            return

        success = self.db_manager.register_user(username, password)
        if success:
            messagebox.showinfo("Success", "Account created successfully! Please log in.")
            self.tabview.set("Login")
            self.reg_user_entry.delete(0, ctk.END)
            self.reg_pass_entry.delete(0, ctk.END)
        else:
            messagebox.showerror("Error", "Username already exists. Choose another.")