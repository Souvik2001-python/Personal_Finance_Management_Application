import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def plot_daily_income_expense_savings():
    # Always connect to DB fresh and fetch data
    conn = sqlite3.connect('myexpense.db')
    
    # Fetch latest salary (income) data
    salary_query = "SELECT credit_date, amount FROM salary"
    salary_df = pd.read_sql_query(salary_query, conn)
    
    # Fetch latest expense data
    expense_query = "SELECT purchase_date, item_price FROM expense_record"
    expense_df = pd.read_sql_query(expense_query, conn)
    
    conn.close()

    # Convert to datetime
    salary_df['credit_date'] = pd.to_datetime(salary_df['credit_date'])
    expense_df['purchase_date'] = pd.to_datetime(expense_df['purchase_date'])

    # Keep only date
    salary_df['date'] = salary_df['credit_date'].dt.date
    expense_df['date'] = expense_df['purchase_date'].dt.date

    # Group daily
    income_by_day = salary_df.groupby('date')['amount'].sum().reset_index()
    expense_by_day = expense_df.groupby('date')['item_price'].sum().reset_index()

    # Merge and sort
    merged_df = pd.merge(income_by_day, expense_by_day, on='date', how='outer').fillna(0)
    merged_df = merged_df.sort_values('date').reset_index(drop=True)

    # Cumulative savings calculation
    merged_df['savings'] = 0.0
    savings = 0.0
    for i in range(len(merged_df)):
        income = merged_df.at[i, 'amount']
        expense = merged_df.at[i, 'item_price']
        savings = max(savings + income - expense, 0)
        merged_df.at[i, 'savings'] = savings

    # Plotting
    x = np.arange(len(merged_df['date']))
    width = 0.25

    fig = Figure(figsize=(12, 6), dpi=100)
    ax = fig.add_subplot(111)

    bars1 = ax.bar(x - width, merged_df['amount'], width, label='Income', color='#4CAF50')
    bars2 = ax.bar(x, merged_df['item_price'], width, label='Expenditure', color='#F44336')
    bars3 = ax.bar(x + width, merged_df['savings'], width, label='Savings', color='#2196F3')

    # Labels on top
    for bar in bars1 + bars2 + bars3:
        height = bar.get_height()
        if height > 0:
            ax.annotate(f'{height:.2f}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8, rotation=90)

    # Styling
    ax.set_xlabel('Date', fontsize=12, fontweight='bold')
    ax.set_ylabel('Amount', fontsize=12, fontweight='bold')
    ax.set_title('Daily Income, Expenditure, and Savings (Cumulative)', fontsize=14, weight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(merged_df['date'].astype(str), rotation=45, fontsize=8)
    ax.legend(fontsize=10)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    return fig
