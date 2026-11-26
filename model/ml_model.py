import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

class FinancePredictor:
    def __init__(self):
        pass

    def predict_next_month_expense(self, transactions):
        if not transactions:
            return 0.0

        df = pd.DataFrame(transactions)
        expenses_df = df[df['type'].str.lower() == 'expense'].copy()
        
        if len(expenses_df) < 2:
            return float(expenses_df['amount'].sum()) if not expenses_df.empty else 0.0

        expenses_df['date'] = pd.to_datetime(expenses_df['date'], format='mixed', errors='coerce')
        expenses_df = expenses_df.dropna(subset=['date'])
        expenses_df = expenses_df.sort_values('date')

        if expenses_df.empty:
            return 0.0

        expenses_df['day_index'] = np.arange(len(expenses_df))
        
        X = expenses_df[['day_index']]
        y = expenses_df['amount']

        model = LinearRegression()
        model.fit(X, y)

        next_index = np.array([[len(expenses_df)]])
        prediction = model.predict(next_index)[0]

        return max(0.0, float(prediction))

    def generate_recommendations(self, transactions, budgets):
        if not transactions:
            return "No transaction history available yet to generate financial insights."

        df = pd.DataFrame(transactions)
        expenses_df = df[df['type'].str.lower() == 'expense']
        
        if expenses_df.empty:
            return "No expenses recorded yet. Keep tracking to receive AI-driven insights!"

        category_totals = expenses_df.groupby('category')['amount'].sum().to_dict()
        recommendations = []

        for cat, spent in category_totals.items():
            limit = budgets.get(cat, 0)
            if limit > 0:
                pct = (spent / limit) * 100
                if pct >= 100:
                    recommendations.append(f"🚨 Budget Exceeded: You have spent {pct:.1f}% of your '{cat}' budget.")
                elif pct >= 80:
                    recommendations.append(f"⚠️ Warning: You are at {pct:.1f}% of your '{cat}' budget limit.")
            else:
                recommendations.append(f"💡 Tip: '{cat}' has no budget limit set. Consider setting one.")

        if not recommendations:
            recommendations.append("✅ All spending is currently well within safe budget boundaries. Great job!")

        return "\n".join(recommendations)