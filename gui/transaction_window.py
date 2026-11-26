import customtkinter as ctk
from tkinter import messagebox, ttk
from datetime import datetime
from activity.activity_logger import ActivityLogger

class TransactionFrame(ctk.CTkFrame):
    def __init__(self, parent, user_id, username, db_manager, refresh_callback=None):
        super().__init__(parent, fg_color="#090d16", corner_radius=0)
        self.user_id = user_id
        self.username = username
        self.db_manager = db_manager
        self.refresh_callback = refresh_callback
        self.logger = ActivityLogger()

        self.setup_ui()
        self.load_transactions()

    def setup_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header_frame, text="Transaction Management", font=("Segoe UI", 22, "bold"), text_color="#f8fafc").pack(side="left")

        form_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        form_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkLabel(form_frame, text="Add New Transaction", font=("Segoe UI", 15, "bold"), text_color="#38bdf8").pack(anchor="w", padx=20, pady=(15, 10))

        fields_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        fields_frame.pack(fill="x", padx=20, pady=(0, 10))
        fields_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Date & Type
        ctk.CTkLabel(fields_frame, text="Date (YYYY-MM-DD):", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ctk.CTkEntry(fields_frame, width=170, height=35)
        self.date_entry.grid(row=1, column=0, padx=5, pady=5)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))

        ctk.CTkLabel(fields_frame, text="Type:", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.type_combo = ctk.CTkComboBox(fields_frame, values=["Income", "Expense"], width=170, height=35, state="readonly")
        self.type_combo.grid(row=1, column=1, padx=5, pady=5)
        self.type_combo.set("Expense")

        # Category ComboBox with presets + Custom option
        ctk.CTkLabel(fields_frame, text="Category:", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.cat_combo = ctk.CTkComboBox(
            fields_frame, 
            values=["Salary", "Food", "Shopping", "Bills", "Travel", "Other (Custom)"], 
            width=170, 
            height=35, 
            state="readonly",
            command=self.on_category_select
        )
        self.cat_combo.grid(row=1, column=2, padx=5, pady=5)
        self.cat_combo.set("Food")

        ctk.CTkLabel(fields_frame, text="Amount (₹):", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.amount_entry = ctk.CTkEntry(fields_frame, width=170, height=35)
        self.amount_entry.grid(row=1, column=3, padx=5, pady=5)

        # Hidden/Dynamic Custom Category Field
        self.custom_cat_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        self.custom_cat_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        self.custom_cat_label = ctk.CTkLabel(self.custom_cat_frame, text="Type Custom Category Name:", font=("Segoe UI", 11, "bold"), text_color="#38bdf8")
        self.custom_cat_entry = ctk.CTkEntry(self.custom_cat_frame, width=300, height=35, placeholder_text="e.g. Freelance, Investment, Pets")

        desc_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        desc_frame.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(desc_frame, text="Description:", font=("Segoe UI", 11, "bold"), text_color="#cbd5e1").pack(anchor="w", pady=(0, 5))
        
        row_bottom = ctk.CTkFrame(desc_frame, fg_color="transparent")
        row_bottom.pack(fill="x")

        self.desc_entry = ctk.CTkEntry(row_bottom, height=35)
        self.desc_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))

        save_btn = ctk.CTkButton(row_bottom, text="Add Transaction", fg_color="#2563eb", hover_color="#1d4ed8", font=("Segoe UI", 12, "bold"), height=35, command=self.add_transaction)
        save_btn.pack(side="right")

        table_frame = ctk.CTkFrame(self, fg_color="#1e293b", corner_radius=12)
        table_frame.pack(fill="both", expand=True, padx=30, pady=10)

        ctk.CTkLabel(table_frame, text="Recent Transactions History", font=("Segoe UI", 15, "bold"), text_color="#38bdf8").pack(anchor="w", padx=20, pady=(15, 10))

        tree_container = ctk.CTkFrame(table_frame, fg_color="#0f172a")
        tree_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        columns = ("ID", "Date", "Type", "Category", "Amount", "Description")
        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings", height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.column("ID", width=60)
        self.tree.column("Description", width=200)

        scrollbar = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def on_category_select(self, choice):
        if choice == "Other (Custom)":
            self.custom_cat_label.pack(anchor="w", pady=(0, 3))
            self.custom_cat_entry.pack(anchor="w")
        else:
            self.custom_cat_entry.delete(0, ctk.END)
            self.custom_cat_entry.pack_forget()
            self.custom_cat_label.pack_forget()

    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        transactions = self.db_manager.get_transactions(self.user_id)
        for t in transactions:
            formatted_amount = f"₹{t['amount']:,.2f}"
            self.tree.insert("", "end", values=(t['id'], t['date'], t['type'], t['category'], formatted_amount, t['description']))

    def add_transaction(self):
        date = self.date_entry.get().strip()
        trans_type = self.type_combo.get()
        
        selected_cat = self.cat_combo.get()
        if selected_cat == "Other (Custom)":
            category = self.custom_cat_entry.get().strip()
            if not category:
                messagebox.showerror("Error", "Please enter a name for your custom category.")
                return
        else:
            category = selected_cat

        amount_str = self.amount_entry.get().strip()
        description = self.desc_entry.get().strip()

        if not date or not amount_str:
            messagebox.showerror("Error", "Date and Amount fields are required.")
            return

        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for the amount.")
            return

        self.db_manager.add_transaction(self.user_id, date, category, amount, trans_type, description, username=self.username)
        messagebox.showinfo("Success", "Transaction added successfully!")

        self.amount_entry.delete(0, ctk.END)
        self.desc_entry.delete(0, ctk.END)
        self.custom_cat_entry.delete(0, ctk.END)
        self.cat_combo.set("Food")
        self.on_category_select("Food")
        self.load_transactions()

        if self.refresh_callback:
            self.refresh_callback()