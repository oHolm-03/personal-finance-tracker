import numpy as np
from datetime import timedelta
from sklearn.linear_model import LinearRegression

class BalancePredictor: 
    def __init__(self, tracker):
        # Store reference to the tracker so we can access its data
        self.tracker = tracker
        # Will hold the trained ML model
        self.model = None

        #MAIN PREDICTION METHOD
    def predict_future_balance(self, days_ahead = 30):
        #get historical daily balances from the tracker
        dates, balances = self.tracker.get_daily_balances()
        
        if len(dates) < 2:
            print("Need at least 2 days of data for predictions")
            return None
        
        #convert day numbers to numpy array
        X = np.array(range(len(dates))).reshape(-1,1)
        #convert balances to numpy array
        y = np.array(balances)

        #Training the ML Model
        self.model = LinearRegression()
        #Train the model on historical data
        self.model.fit(X, y)

        #Generate Future Predictions
        #create day numbers for future days
        future_day_numbers = range(len(dates), len(dates) + days_ahead)
        #convert to numpy array in correct format
        X_future = np.array(future_day_numbers).reshape(-1,1)
        predictions = self.model.predict(X_future)

        #Convert Day Numbers Back to Actual Dates
        last_date = dates[-1]

        #generate actual calendar dates for the future
        future_dates = [last_date + timedelta(days=i+1) for i in range(days_ahead)]

        return future_dates, predictions, dates, balances

    #HELPER METHOD- to get information about the trend
    def get_trend_info(self):
        if self.model is None:
            #train model with 1 day prediction to initialize
            self.predict_future_balance(1)

        #Double check if model exists
        if self.model is None:
            return None
    
        #get slop from the trained model
        daily_change = self.model.coef_[0]

        #determine if user is saving or spending
        trend_direction = 'saving' if daily_change > 0 else 'spending'
        monthly_change = daily_change *30

        return{
            'Daily Change': daily_change,
            'Trend Direction': trend_direction,
            'Monthly Change': monthly_change
        }