import matplotlib.pyplot as plt

#Main Class (handles all visualization)
class FinanceVisualizer:
    def __init__(self, tracker, predictor):
        self.tracker = tracker
        self.predictor = predictor

#Prediction chart
def PlotPrediction(self, daysAhead=30):
    result = self.predictor.predict_future_balance(daysAhead)
    
    if result is None:
        print("Need at least 2 days to make a prediction")
        return
    
    #unpack tuple into 4 separate variables
    future_dates, predictions, hist_dates, hist_balances = result
    
    #Create new figure for charts
    plt.figure(figsize=(12,6))
    
    #Plot historical data
    plt.plot(hist_dates, hist_balances, 'b-', label='Historical Balance', linewidth=2)

    #Plot predictions
    plt.plot(future_dates, predictions, 'r--', label='Predicted Balance', linewidth=2)

    #labels and formatting
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Balance ($)', fontsize=12)
    plt.title('Personal Finance: Historical and Predicted Balance', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10)
    plt.grid(True, alpha=.3)
    plt.xticks(rotation=45)
    plt.show()

# Income vs Expenses chart
def plot_income_vs_expenses(self):
    stats = self.tracker.get_summary_stats()

    categories = ['Income', 'Expenses']
    values = [stats['total_income'], stats['total_expenses']]
    colors = ['green', 'red']

    plt.figure(figsize=(8,6))
    plt.bar(categories, values, color=colors, alpha=.7)

    plt.ylabel('Amount ($)', fontsize=12)
    plt.title('Total Income vs Expenses', fontsize=14, fontweight='bold')
    plt.grid(axis='y', alpha=.3)

    plt.tight_layout()
    plt.show()
