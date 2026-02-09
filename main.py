#imports 
import json
import os
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from src import FinanceTracker, BalancePredictor, FinanceVisualizer, FinanceUI

def main():
    tracker = FinanceTracker()

    predictor = BalancePredictor(tracker)

    visualizer = FinanceVisualizer(tracker, predictor)

    ui = FinanceUI(tracker, predictor, visualizer)

    ui.run()

    if __name__ == "__main__":
        main()
