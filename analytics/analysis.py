import pandas as pd
import numpy as np

class FinanceAnalyzer:
    def __init__(self):
        pass

    def get_summary_metrics(self, transactions):
        if not transactions:
            return {"total_income": 0.0, "total_expense": 0.0, "net_savings": 0.0}

        df = pd.DataFrame(transactions)
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
        
        total_income = df[df['type'].str.lower() == 'income']['amount'].sum()
        total_expense = df[df['type'].str.lower() == 'expense']['amount'].sum()
        net_savings = total_income - total_expense

        return {
            "total_income": float(total_income),
            "total_expense": float(total_expense),
            "net_savings": float(net_savings)
        }

    def get_category_breakdown(self, transactions):
        if not transactions:
            return {}

        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
        expenses_df = df[df['type'].str.lower() == 'expense']
        if expenses_df.empty:
            return {}

        breakdown = expenses_df.groupby('category')['amount'].sum().to_dict()
        return breakdown