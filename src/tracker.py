import json
import os
from datetime import datetime, timedelta

#manages financial transactions and data persistance
class FinanceTracker:
    def __init__(self, filename='data/finance_data.json'):
        # Store the filename as an instance variable (self.filename)
        self.filename = filename
        # Make sure the directory exists
        self._ensure_data_directory()
        # Load existing transactions from file
        self.transactions = self.load_data()

# HELPER METHOD, creates directory if it doesn't exist
def _ensure_data_directory(self):
        # Extract directory path from filename
        directory = os.path.dirname(self.filename)
        
        # Only proceed if directory is not empty string AND doesn't already exist
        if directory and not os.path.exists(directory):
            # Create the directory (and any parent directories needed)
            os.makedirs(directory)

#Loading data from file
def load_data(self):
        # Check if the file exists before trying to read it
        if os.path.exists(self.filename):
            # Open the file in read mode ('r')
            with open(self.filename, 'r') as f:
                # json.load() reads the file and converts JSON to Python list
                return json.load(f)
        
        # If file doesn't exist, return empty list (brand new tracker)
        return []

#Saving data to file
def save_data(self):
        # Open file in write mode ('w') - creates file if it doesn't exist
        with open(self.filename, 'w') as f:
            # json.dump() converts Python list to JSON and writes to file
            json.dump(self.transactions, f, indent=2)

#Adding new transactions
def add_transaction(self, amount, trans_type, description=''):
        # Create a dictionary to represent this transaction
        transaction = {
            # Get current date and time, format as string: '2025-01-11 14:30:00'
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            
            # Store the type ('income' or 'expense')
            'type': trans_type,
            
            # Convert amount to float (handles if user passes int or string)
            'amount': float(amount),
            
            # Store the description (empty string if not provided)
            'description': description
        }
        
        # Add this transaction to our list of all transactions
        # self.transactions is a list, .append() adds to the end
        self.transactions.append(transaction)
        
        # Save to file immediately so data isn't lost
        self.save_data()
        
        # Return the transaction in case caller needs it
        return transaction

#Current total balance
def get_balance(self):
        # Start with balance of 0
        balance = 0
        
        # Loop through every transaction in our list
        # 't' is a temporary variable holding each transaction dictionary
        for t in self.transactions:
            # Check if this transaction is income
            if t['type'] == 'income':
                # Add income to balance
                balance += t['amount']
            else:  # Must be 'expense'
                # Subtract expense from balance
                balance -= t['amount']
        
        # Return the final calculated balance
        return balance

#Calculate balance for each day using ML
def get_daily_balances(self):
        # If no transactions exist, return empty lists
        if not self.transactions:
            return [], []
        
        # Sort transactions by date (earliest first)
        # lambda x: x['date'] means "sort by the 'date' field of each transaction"
        sorted_trans = sorted(self.transactions, key=lambda x: x['date'])
        
        # Get the date of the very first transaction
        # strptime() converts string '2025-01-11 14:30:00' to datetime object
        start_date = datetime.strptime(sorted_trans[0]['date'], '%Y-%m-%d %H:%M:%S')
        
        # Initialize empty lists to store our results
        dates = []  # Will hold date objects
        balances = []  # Will hold balance amounts
        
        # Start with balance of 0 and the first transaction's date
        current_balance = 0
        current_date = start_date.date()  # .date() extracts just the date (no time)
        
        # Process each transaction in chronological order
        for t in sorted_trans:
            # Get the date of this transaction
            trans_date = datetime.strptime(t['date'], '%Y-%m-%d %H:%M:%S').date()
            
            # Fill in all days BEFORE this transaction (days with no activity)
            # Example: If transaction on Jan 5 and we're on Jan 3, fill Jan 3 and 4
            while current_date < trans_date:
                # Record the current date and balance
                dates.append(current_date)
                balances.append(current_balance)
                
                # Move to next day (timedelta(days=1) = 1 day)
                current_date += timedelta(days=1)
            
            # Now apply this transaction to the balance
            if t['type'] == 'income':
                current_balance += t['amount']  # Add income
            else:
                current_balance -= t['amount']  # Subtract expense
        
        # Add the final day's balance (today)
        dates.append(current_date)
        balances.append(current_balance)
        
        # Return both lists as a tuple
        return dates, balances

#Get summary information and stats
def get_summary_stats(self):
        # Sum all amounts where type is 'income'
        # This is a "list comprehension" - compact way to filter and sum
        # It loops through transactions, picks only income ones, extracts amount, and sums
        total_income = sum(t['amount'] for t in self.transactions if t['type'] == 'income')
        
        # Same but for expenses
        total_expenses = sum(t['amount'] for t in self.transactions if t['type'] == 'expense')
        
        # Return all stats as a dictionary
        return {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'balance': self.get_balance(),  # Call our balance calculation method
            'transaction_count': len(self.transactions)  # len() returns list length
        }