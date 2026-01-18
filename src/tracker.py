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