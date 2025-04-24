# Personal_Finance_Management_Application
Project Overview
The Personal Finance Management Application is a user-friendly, GUI-based desktop software developed in Python during my internship at Innobyte Services. The application allows users to manage their personal finances, track income and daily expenses, generate financial reports, and visualize their financial trends. It combines authentication, data management, and visualization in one compact tool.

Objective
To build a secure, intuitive desktop-based financial management system that allows users to:
- Track and manage income and expenses.
- View savings and spending summaries.
- Interact with their financial data through graphical representations.
- Perform CRUD operations on financial records.

Key Features
User Authentication
- Sign Up:  New users can create an account using email and password.
- Login:  Only registered users can log in to access personal finance tools.

Income Tracking
- Users can save their income by entering the salary and clicking Save Salary.

Expense Recording
- Add transaction details with category and amount.
- Supports comma-separated categories.
- Automatically captures the current date.
- Click Save Record to log the expense.

Balance Calculation
- The Total Balance button calculates and displays:
  - Total Income
  - Total Expenditure
  - Net Savings

Graph Generation
- Generate Graph visualizes financial trends using bar charts or line graphs for better insights.

Live Record Table
- Displays all data in a table format with the ability to:
  - Update: Click a row → Edit data → Click Update.
  - Delete: Select a row → Click Delete to remove.

Utility Buttons
- Clear Entry: Clears all input fields.
- Exit: Exits the application.

Technologies Used
- Python 3.x
- Tkinter & CustomTkinter – GUI development
- SQLite – Lightweight local database
- Matplotlib – Graph generation
- Datetime – Date handling and formatting

How to Use the Application
1. Sign Up
- Launch the application.
- Go to the Sign Up tab.
- Enter your email and password.
- Click Register to create your account.

2. Login
- Use your registered email ID and password.
- Click Login to access your dashboard.

3. Add Monthly Income
- Input salary in the Enter the Salary field.
- Click Save Salary to store your income.

4. Record Daily Expenses
- Enter the Transaction Type (e.g., Rent, Food, Utilities — use commas for multiple).
- Input the Amount spent.
- Click Current Date to auto-fill today’s date.
- Click Save Record to log the transaction.

5. View Balance Summary
- Click Total Balance to view:
  - Total Income
  - Total Expenditure
  - Savings

6. Generate Financial Graph
- Click Generate Graph to see a visual representation of your financial data.

7. Update or Delete Data
- Update:
  - Click a row from the table.
  - The data appears in the fields.
  - Edit the data and click Update.
- Delete:
  - Select a row and click Delete to remove it.

8. Other Buttons
- Clear Entry: Empties all input fields.
- Exit: Closes the application safely.
