import customtkinter as ctk
from tkinter import messagebox
from activity.activity_logger import ActivityLogger

class BudgetFrame(ctk.CTkFrame):
    def __init__(self, parent, user_id, username, db_manager, analyzer, refresh_callback=None):
        super().__init__(parent, fg_color="#090d16", corner_radius=0)
        self.user_id = user_id
        self.username = username
        self.db_manager = db_manager
        self.analyzer = analyzer
        self.refresh_callback = refresh_callback
        self.logger = ActivityLogger()

        self.setup_ui()
        self.load_budgets()

    def setup_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header_frame, text="Monthly Budget Planning", font=("Segoe UI", 22, "bold"), text_color="#f8fafc").pack(side="left")

        form_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        form_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(form_frame, text="Set / Update Category Budget", font=("Segoe UI", 15, "bold"), text_color="#38bdf8").pack(anchor="w", padx=20, pady=(15, 10))

        inputs_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        inputs_frame.pack(fill="x", padx=20, pady=(0, 10))
        inputs_frame.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(inputs_frame, text="Category:", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cat_combo = ctk.CTkComboBox(
            inputs_frame, 
            values=["Food", "Shopping", "Bills", "Travel", "Other (Custom)"], 
            width=200, 
            height=35, 
            state="readonly",
            command=self.on_category_select
        )
        self.cat_combo.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cat_combo.set("Food")

        ctk.CTkLabel(inputs_frame, text="Monthly Limit (₹):", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.limit_entry = ctk.CTkEntry(inputs_frame, width=200, height=35)
        self.limit_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        set_btn = ctk.CTkButton(inputs_frame, text="Save Budget", fg_color="#16a34a", hover_color="#15803d", font=("Segoe UI", 12, "bold"), height=35, command=self.save_budget)
        set_btn.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        self.custom_cat_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.custom_cat_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.custom_cat_label = ctk.CTkLabel(self.custom_cat_frame, text="Type Custom Category Name:", font=("Segoe UI", 11, "bold"), text_color="#38bdf8")
        self.custom_cat_entry = ctk.CTkEntry(self.custom_cat_frame, width=300, height=35, placeholder_text="e.g. Investment, Pets, Subscriptions")

        display_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        display_frame.pack(fill="both", expand=True, padx=30, pady=10)

        ctk.CTkLabel(display_frame, text="Budget Progress & Alerts", font=("Segoe UI", 15, "bold"), text_color="#38bdf8").pack(anchor="w", padx=20, pady=(15, 10))

        self.scrollable_content = ctk.CTkScrollableFrame(display_frame, fg_color="#0f172a", corner_radius=8)
        self.scrollable_content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def on_category_select(self, choice):
        if choice == "Other (Custom)":
            self.custom_cat_label.pack(anchor="w", pady=(0, 3))
            self.custom_cat_entry.pack(anchor="w")
        else:
            self.custom_cat_entry.delete(0, ctk.END)
            self.custom_cat_entry.pack_forget()
            self.custom_cat_label.pack_forget()

    def load_budgets(self):
        for widget in self.scrollable_content.winfo_children():
            widget.destroy()

        budgets = self.db_manager.get_budgets(self.user_id)
        transactions = self.db_manager.get_transactions(self.user_id)
        category_spent = self.analyzer.get_category_breakdown(transactions)

        if not budgets:
            ctk.CTkLabel(self.scrollable_content, text="No budgets set yet. Use the form above to set monthly category limits.", font=("Segoe UI", 13), text_color="#94a3b8").pack(pady=30)
            return

        for category, limit in budgets.items():
            spent = category_spent.get(category, 0.0)
            percentage = (spent / limit) if limit > 0 else 0
            display_pct = min(percentage * 100, 100)

            item_frame = ctk.CTkFrame(self.scrollable_content, fg_color="#1e293b", corner_radius=8)
            item_frame.pack(fill="x", padx=10, pady=8)

            info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=(12, 5))

            ctk.CTkLabel(info_frame, text=category, font=("Segoe UI", 14, "bold"), text_color="#f8fafc").pack(side="left")

            status_color = "#22c55e"
            status_text = "On Track"
            if percentage >= 1.0:
                status_color = "#ef4444"
                status_text = "EXCEEDED"
            elif percentage >= 0.8:
                status_color = "#f59e0b"
                status_text = "Warning (>=80%)"

            ctk.CTkLabel(info_frame, text=f"Spent: ₹{spent:,.2f} / Limit: ₹{limit:,.2f} ({display_pct:.1f}%) - {status_text}", font=("Segoe UI", 12, "bold"), text_color=status_color).pack(side="right")

            progress = ctk.CTkProgressBar(item_frame, orientation="horizontal", height=12, progress_color=status_color)
            progress.pack(fill="x", padx=15, pady=(0, 15))
            progress.set(min(percentage, 1.0))

    def save_budget(self):
        selected_cat = self.cat_combo.get()
        if selected_cat == "Other (Custom)":
            category = self.custom_cat_entry.get().strip()
            if not category:
                messagebox.showerror("Error", "Please enter a name for your custom category.")
                return
        else:
            category = selected_cat

        limit_str = self.limit_entry.get().strip()

        if not limit_str:
            messagebox.showerror("Error", "Please enter a monthly limit amount.")
            return

        try:
            limit = float(limit_str)
            if limit <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive numeric budget limit.")
            return

        self.db_manager.set_budget(self.user_id, category, limit)
        self.logger.log_activity(self.username, "SET_BUDGET", f"Set budget limit for '{category}' to ₹{limit:,.2f}")
        messagebox.showinfo("Success", f"Budget for '{category}' set to ₹{limit:,.2f} successfully!")
        
        self.limit_entry.delete(0, ctk.END)
        self.custom_cat_entry.delete(0, ctk.END)
        self.cat_combo.set("Food")
        self.on_category_select("Food")
        
        self.load_budgets()
        if self.refresh_callback:
            self.refresh_callback()