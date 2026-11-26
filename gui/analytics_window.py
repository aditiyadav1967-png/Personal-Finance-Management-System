import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AnalyticsFrame(ctk.CTkFrame):
    def __init__(self, parent, user_id, db_manager, analyzer, predictor, refresh_callback=None):
        super().__init__(parent, fg_color="#090d16", corner_radius=0)
        self.user_id = user_id
        self.db_manager = db_manager
        self.analyzer = analyzer
        self.predictor = predictor
        self.refresh_callback = refresh_callback

        self.setup_ui()
        self.refresh_analytics()

    def setup_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=20)
        ctk.CTkLabel(header_frame, text="Analytics & Machine Learning Forecasting", font=("Segoe UI", 22, "bold"), text_color="#f8fafc").pack(side="left")

        self.scrollable_content = ctk.CTkScrollableFrame(self, fg_color="#090d16")
        self.scrollable_content.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        top_grid = ctk.CTkFrame(self.scrollable_content, fg_color="transparent")
        top_grid.pack(fill="x", pady=(0, 15))
        top_grid.grid_columnconfigure((0, 1), weight=1)

        self.ml_card = ctk.CTkFrame(top_grid, fg_color="#1e293b", corner_radius=12)
        self.ml_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        ctk.CTkLabel(self.ml_card, text="🤖 AI Expense Forecasting", font=("Segoe UI", 15, "bold"), text_color="#38bdf8").pack(anchor="w", padx=20, pady=(15, 5))
        self.ml_label = ctk.CTkLabel(self.ml_card, text="Analyzing financial trend...", font=("Segoe UI", 13), text_color="#cbd5e1", justify="left")
        self.ml_label.pack(anchor="w", padx=20, pady=(0, 15))

        self.rec_card = ctk.CTkFrame(top_grid, fg_color="#1e293b", corner_radius=12)
        self.rec_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(self.rec_card, text="💡 Smart Recommendations", font=("Segoe UI", 15, "bold"), text_color="#38bdf8").pack(anchor="w", padx=20, pady=(15, 5))
        self.rec_label = ctk.CTkLabel(self.rec_card, text="Generating insights...", font=("Segoe UI", 13), text_color="#cbd5e1", justify="left", wraplength=450)
        self.rec_label.pack(anchor="w", padx=20, pady=(0, 15))

        charts_grid = ctk.CTkFrame(self.scrollable_content, fg_color="transparent")
        charts_grid.pack(fill="both", expand=True, pady=10)
        charts_grid.grid_columnconfigure((0, 1), weight=1)

        self.chart1_frame = ctk.CTkFrame(charts_grid, fg_color="#1e293b", corner_radius=12)
        self.chart1_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

        self.chart2_frame = ctk.CTkFrame(charts_grid, fg_color="#1e293b", corner_radius=12)
        self.chart2_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

    def refresh_analytics(self):
        transactions = self.db_manager.get_transactions(self.user_id)
        budgets = self.db_manager.get_budgets(self.user_id)
        
        next_month_pred = self.predictor.predict_next_month_expense(transactions)
        self.ml_label.configure(text=f"• Predicted Expense for Next Month: ₹{next_month_pred:,.2f}\n• Model: Linear Regression Trend Analysis")

        recommendations = self.predictor.generate_recommendations(transactions, budgets)
        self.rec_label.configure(text=recommendations)

        plt.close('all')

        for widget in self.chart1_frame.winfo_children():
            widget.destroy()
        for widget in self.chart2_frame.winfo_children():
            widget.destroy()

        plt.style.use('dark_background')

        fig1, ax1 = plt.subplots(figsize=(5, 3.5))
        fig1.patch.set_facecolor('#1e293b')
        ax1.set_facecolor('#1e293b')
        
        breakdown = self.analyzer.get_category_breakdown(transactions)
        if breakdown:
            wedges, texts, autotexts = ax1.pie(
                breakdown.values(), 
                labels=breakdown.keys(), 
                autopct='%1.1f%%', 
                startangle=140, 
                colors=['#38bdf8', '#3b82f6', '#22c55e', '#f59e0b', '#ef4444']
            )
            for t in texts + autotexts:
                t.set_color('#f8fafc')
            ax1.set_title("Expenses by Category", fontsize=12, color="#f8fafc", pad=10)
        else:
            ax1.text(0.5, 0.5, "No transaction data available", color="#94a3b8", ha='center', va='center')
            ax1.axis('off')

        canvas1 = FigureCanvasTkAgg(fig1, master=self.chart1_frame)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        fig2, ax2 = plt.subplots(figsize=(5, 3.5))
        fig2.patch.set_facecolor('#1e293b')
        ax2.set_facecolor('#1e293b')

        metrics = self.analyzer.get_summary_metrics(transactions)
        categories = ['Income', 'Expense', 'Savings']
        values = [metrics['total_income'], metrics['total_expense'], metrics['net_savings']]
        
        ax2.bar(categories, values, color=['#22c55e', '#ef4444', '#3b82f6'])
        ax2.set_title("Financial Summary", fontsize=12, color="#f8fafc", pad=10)
        ax2.tick_params(colors='#f8fafc')
        ax2.spines['bottom'].set_color('#475569')
        ax2.spines['left'].set_color('#475569')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        canvas2 = FigureCanvasTkAgg(fig2, master=self.chart2_frame)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)