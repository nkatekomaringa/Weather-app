import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
#import seaborn as sns
import sqlite3

# Initialize SQLite database
db = sqlite3.connect('finance.db')
cursor =db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS transactions(id INTEGER PRIMARY KEY, amount REAL, category TEXT, date TEXT, type TEXT CHECK(type IN ('income', 'expense')))")
db.commit()

def add_transaction():
    
    amount = float(input("Amount: "))
    category = input("Category: ")
    date = input("Date (YYYY-MM-DD): ")
    trans_type = input("Type (income/expense): ").lower()
    
    cursor.execute('''INSERT INTO transactions (amount, category, date, type)VALUES (?, ?, ?, ?)''', (amount, category, date, trans_type))
    db.commit()
    print("Transaction added!")

def view_transactions():
    df = pd.read_sql('SELECT * FROM transactions', db)
    print(df)
    return df

def plot_spending():
    df = pd.read_sql('SELECT * FROM transactions', db)
    df['date'] = pd.to_datetime(df['date'])
    
    # Daily Balance Over Time
    df['net'] = df.apply(lambda x: x['amount'] if x['type'] == 'income' else -x['amount'], axis=1)
    daily_balance = df.groupby('date')['net'].sum().cumsum()
    
    plt.figure(figsize=(10, 5))
    plt.plot(daily_balance.index, daily_balance.values, marker='o')
    plt.title("Net Balance Over Time")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.grid(True)
    
    #Pie Chart
    expenses = df[df['type'] == 'expense']
    if not expenses.empty:
        plt.figure(figsize=(8, 8))
        expenses.groupby('category')['amount'].sum().plot.pie(autopct='%1.1f%%')
        plt.title("Spending by Category")
    
    plt.show()

def predict_future():
    #Linear Regression.
    df = pd.read_sql('SELECT * FROM transactions', db)
    df['date'] = pd.to_datetime(df['date'])
    df['net'] = df.apply(lambda x: x['amount'] if x['type'] == 'income' else -x['amount'], axis=1)
    daily_balance = df.groupby('date')['net'].sum().cumsum().reset_index()
    daily_balance['days'] = (daily_balance['date'] - daily_balance['date'].min()).dt.days
    
    # training
    X = daily_balance[['days']]
    y = daily_balance['net']
    
    model = LinearRegression()
    model.fit(X, y)
    
    #predictions for a month
    future_days = pd.DataFrame({'days': range(daily_balance['days'].max() + 1, daily_balance['days'].max() + 31)})
    future_dates = pd.date_range(daily_balance['date'].max(), periods=30)
    future_balance = model.predict(future_days)
    
   
    plt.figure(figsize=(10, 5))
    plt.plot(daily_balance['date'], daily_balance['net'], label="Historical Balance")
    plt.plot(future_dates, future_balance, 'r--', label="Predicted Balance")
    plt.title("Future Balance Prediction")
    plt.xlabel("Date")
    plt.ylabel("Balance")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1. Add Transaction")
        print("2. View Transactions")
        print("3. Plot Spending")
        print("4. Predict Future Balance")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            plot_spending()
        elif choice == '4':
            predict_future()
        elif choice == '5':
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
    db.close()