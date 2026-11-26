# 💰 Personal Finance Management System

![Python](https://img.shields.io/badge/Python-3.13+-blue?logo=python&logoColor=white)
![UI](https://img.shields.io/badge/GUI-CustomTkinter-2b5b84)
![Database](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white)

A desktop-based **Personal Finance Intelligence System** built with Python, CustomTkinter, and SQLite. It helps users securely manage accounts, track daily income and expenses, set monthly budgets, visualize spending habits, and export activity logs.

---

## ✨ Key Features

- **🔐 Secure User Authentication:** Built-in login and registration system backed by SQLite (`finance.db`).
- **📊 Modern Interactive Dashboard:** Clean, responsive dark-mode interface with full window resizing and navigation.
- **💸 Transaction Tracking:** Log, categorize, and review all income and expense entries in real time.
- **🎯 Budget Management:** Create and monitor monthly category budgets to prevent overspending.
- **📈 Financial Analytics & ML Insights:** Visual spending breakdowns and predictive financial modeling.
- **📁 CSV Activity Export:** Automatically logs user activity and supports exporting financial records to CSV.

---

## 🗂️ Project Structure

```text
Personal-Finance-Management-System/
├── activity/       # User activity logging and CSV exports
├── analytics/      # Financial data analysis and reporting
├── database/       # SQLite database connection and schema manager
├── gui/            # CustomTkinter windows (Auth, Dashboard, Budgets, Analytics, Transactions)
├── main/           # Application entry point (main.py)
├── model/          # Machine learning & predictive analytics module
└── README.md       # Project documentation
