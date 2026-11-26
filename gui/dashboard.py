import os
import shutil
import customtkinter as ctk
from tkinter import messagebox, filedialog
from gui.transaction_window import TransactionFrame
from gui.budget_window import BudgetFrame
from gui.analytics_window import AnalyticsFrame
from analytics.analysis import FinanceAnalyzer
from model.ml_model import FinancePredictor
from activity.activity_logger import ActivityLogger

class DashboardWindow:
    def __init__(self, root, user_id, username, db_manager):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.db_manager = db_manager
        
        self.analyzer = FinanceAnalyzer()
        self.predictor = FinancePredictor()
        # Initialize logger specifically for the current logged-in user
        self.logger = ActivityLogger(username=self.username)

        self.root.title(f"Personal Finance Intelligence System - Welcome, {username}")
        self.root.geometry("1150x720")
        self.root.configure(fg_color="#090d16")

        self.setup_ui()

    def setup_ui(self):
        self.sidebar_frame = ctk.CTkFrame(self.root, width=240, corner_radius=0, fg_color="#0f172a")
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)

        self.content_container = ctk.CTkFrame(self.root, fg_color="#090d16", corner_radius=0)
        self.content_container.pack(side="right", fill="both", expand=True)

        brand_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        brand_frame.pack(fill="x", pady=30, padx=20)
        
        ctk.CTkLabel(brand_frame, text="Finance Hub", font=("Segoe UI", 20, "bold"), text_color="#38bdf8").pack(anchor="w")
        ctk.CTkLabel(brand_frame, text=f"User: {self.username}", font=("Segoe UI", 12), text_color="#94a3b8").pack(anchor="w", pady=(5, 0))

        nav_buttons = [
            ("📊 Overview & KPIs", self.show_overview),
            ("💳 Transactions", self.show_transactions),
            ("🎯 Budget Planning", self.show_budgets),
            ("🤖 Analytics & ML", self.show_analytics),
            ("📥 Download Activity CSV", self.download_activity_csv),
            ("🚪 Logout", self.logout)
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar_frame, text=text, font=("Segoe UI", 13, "bold"),
                fg_color="#1e293b", hover_color="#334155", text_color="#f8fafc",
                anchor="w", height=45, corner_radius=8, command=command
            )
            btn.pack(fill="x", pady=6, padx=15)

        self.show_overview()

    def clear_content(self):
        for widget in self.content_container.winfo_children():
            widget.destroy()

    def show_overview(self):
        self.clear_content()

        header = ctk.CTkFrame(self.content_container, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header, text="Financial Overview & Summary", font=("Segoe UI", 22, "bold"), text_color="#f8fafc").pack(side="left")

        transactions = self.db_manager.get_transactions(self.user_id)
        metrics = self.analyzer.get_summary_metrics(transactions)

        kpi_frame = ctk.CTkFrame(self.content_container, fg_color="transparent")
        kpi_frame.pack(fill="x", padx=30, pady=10)
        kpi_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.create_kpi_card(kpi_frame, "Total Income", f"₹{metrics['total_income']:,.2f}", "#22c55e", 0)
        self.create_kpi_card(kpi_frame, "Total Expense", f"₹{metrics['total_expense']:,.2f}", "#ef4444", 1)
        self.create_kpi_card(kpi_frame, "Net Savings", f"₹{metrics['net_savings']:,.2f}", "#3b82f6", 2)

        activity_frame = ctk.CTkFrame(self.content_container, fg_color="#1e293b", corner_radius=12)
        activity_frame.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(activity_frame, text=f"Welcome back, {self.username}!", font=("Segoe UI", 16, "bold"), text_color="#38bdf8").pack(anchor="w", padx=25, pady=(25, 10))
        ctk.CTkLabel(activity_frame, text="• Use the sidebar menu to log and manage your transactions and category budgets.\n• Visit Analytics & ML to view predictive forecasting powered by machine learning.\n• Click 'Download Activity CSV' anytime to export your personal transaction history directly for Excel.", font=("Segoe UI", 13), text_color="#cbd5e1", justify="left").pack(anchor="w", padx=25, pady=5)

    def create_kpi_card(self, parent, title, value, color, column):
        card = ctk.CTkFrame(parent, fg_color="#1e293b", corner_radius=12, height=110)
        card.grid(row=0, column=column, padx=10, sticky="nsew")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text=title, font=("Segoe UI", 12, "bold"), text_color="#94a3b8").pack(anchor="w", padx=20, pady=(15, 0))
        ctk.CTkLabel(card, text=value, font=("Segoe UI", 20, "bold"), text_color=color).pack(anchor="w", padx=20, pady=(5, 15))

    def show_transactions(self):
        self.clear_content()
        self.trans_frame = TransactionFrame(self.content_container, self.user_id, self.username, self.db_manager)
        self.trans_frame.pack(fill="both", expand=True)

    def show_budgets(self):
        self.clear_content()
        self.budget_frame = BudgetFrame(self.content_container, self.user_id, self.username, self.db_manager, self.analyzer)
        self.budget_frame.pack(fill="both", expand=True)

    def show_analytics(self):
        self.clear_content()
        self.analytics_frame = AnalyticsFrame(self.content_container, self.user_id, self.db_manager, self.analyzer, self.predictor)
        self.analytics_frame.pack(fill="both", expand=True)

    def download_activity_csv(self):
        source_path = self.logger.file_path
        if not os.path.exists(source_path):
            messagebox.showwarning("No Logs", "No transaction log file found for this user yet.")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV File (Opens in Excel)", "*.csv"), ("All Files", "*.*")],
            initialfile=f"activity_log_{self.username}.csv",
            title="Export Personal Transaction Log for Excel"
        )
        if save_path:
            try:
                shutil.copyfile(source_path, save_path)
                messagebox.showinfo(
                    "Export Successful", 
                    f"Your personal transaction log exported successfully!\n\nYou can open this file directly in Excel:\n{save_path}"
                )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file: {e}")

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.root.destroy()
            from gui.auth_window import AuthWindow
            root = ctk.CTk()
            AuthWindow(root, self.db_manager, lambda uid, uname: DashboardWindow(ctk.CTk(), uid, uname, self.db_manager))
            root.mainloop()