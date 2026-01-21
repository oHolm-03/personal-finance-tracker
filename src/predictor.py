import numpy as np
from datetime import timedelta
from sklearn.linear_model import LinearRegression

class BalancePredictor: 
    def __init__(self, tracker):
        # Store reference to the tracker so we can access its data
        self.tracker = tracker
        # Will hold the trained ML model
        self.model = None
