class FinanceUI:
    def __init__(self, tracker, predictor, visualizer):
        #store references to all three components
        self.tracker = tracker
        self.predictor = predictor
        self.visualizer = visualizer

    #Menu Display
    def display_menu(self):
        
        
        # Print title
        print()
        print("PERSONAL FINANCE TRACKER")
        print()
        
        # Print all menu options (numbered 1-8)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View Summary")
        print("5. Predict Future Balance")
        print("6. Visualize Predictions")
        print("7. View Income vs Expenses Chart")
        print("8. Exit")

    #Input Handling
    def add_income(self):
        try:
            amount = float(input("Enter income amount: $"))

            if amount <= 0:
                print("Amount must be positive")
                return
            
            #get optional description
            desc = input ("Description (optional): ")

            #add transaction to tracker
            self.tracker.add_transaction(amount, "income", desc)

            #confirm success to user
            print(f"Income of ${amount:.2f} recorded successfully!")

        # Catch ValueError if user enters non-numeric input
        except ValueError:
            print("Invalid amount. Please enter a number.")

    def add_expense(self):
        try:
            #get amount from user
            amount = float(input("Enter expense amount: $"))

            if amount <= 0:
                print("Amount must be positive.")
                return
            
            #get optional description
            desc = input("Description (optional): ")

            #add as expense
            self.tracker.add_transaction(amount, 'expense', desc)

            print(f"Expense of ${amount:.2f} recorded successfully!")
        
        except ValueError:
            print("Invalid amount. Please enter a number.")

    #Display - show current balance
    def show_balance(self):
        #get current balance
        balance = self.tracker.get_balance()

        print(f"Current Balance: ${balance:,.2f}")

    #Display - show detailed summary
    def show_summary(self): 
        #get summary of stats from tracker
        stats = self.tracker.get_summary_stats()
        
        # Display formatted summary
        print("\nFINANCIAL SUMMARY")

        # Print each statistic
        print(f"Total Income:       ${stats['total_income']:>12,.2f}")
        print(f"Total Expenses:     ${stats['total_expenses']:>12,.2f}")
        print(f"Current Balance:    ${stats['balance']:>12,.2f}")

        # Transaction count (no $ sign, no decimals)
        print(f"Total Transactions: {stats['transaction_count']:>12}")

        #SHOW Predictions
        def show_text_predictions(self):
            try: 
                #get number of days to predict
                #pressing enter defaults to using 30 days
                days = int(input("How many days ahead to predict? (default 30): ") or "30")
                #Get predictions from predictor
                result = self.predictor.predict_future_balance(days)

                if result is None:
                    print("Need at least 2 days of data for predictions")
                    return
                
                #unpack the results tuple
                future_dates, predictions, _, _ = result

                print("Predicted Balances")

                #show predictions weekly
                #zip() pairs up dates with their predictions
                for date, pred in zip(future_dates[::7], predictions[::7]):
                    print(f"{date}: ${pred:,.2f}")

                #Show trend information
                trend = self.predictor.get_trend_info()

                if trend:
                    #display trend direction (saving/spending)
                    print(f"Trend: {trend['trend_direction'].capitalize()}")

                    #show daily change
                    print(f"Daily change: ${trend['daily_change']:.2f}")

                    #show estimated monthly change
                    print(f"Monthly change: ${trend['monthly_change']:.2f}\n")
                #catch if user enters non-int for days
            except ValueError:
                print("Invalid number of days")

# MAIN APPLICATION LOOP
def run(self):
    print("\n Welcome to your Personal Finance Tracker!")

    #infinite loop, keeps running until its broken out of
    while True:
        self.display_menu()

        #get user's choice
        choice = input("\nSelect option (1-8): ").strip()

        if choice == '1':
            # User chose: Add Income
            self.add_income()
            
        elif choice == '2':
            # User chose: Add Expense
            self.add_expense()
        
        elif choice == '3':
            # User chose: View Balance
            self.show_balance()
        
        elif choice == '4':
            # User chose: View Summary
            self.show_summary()
        
        elif choice == '5':
            # User chose: Predict Future Balance (text)
            self.show_text_predictions()

        elif choice == '6':
                # User chose: Visualize Predictions (chart)
                # Get number of days (with default of 30)
                days = int(input("How many days ahead to predict? (default 30): ") or "30")
                # Call visualizer to create and show chart
                self.visualizer.plot_predictions(days)
            
        elif choice == '7':
            # User chose: View Income vs Expenses Chart
            self.visualizer.plot_income_vs_expenses()
        
        elif choice == '8':
            # User chose: Exit
            print("\nThank you for using Finance Tracker. Goodbye!")
            break  # Exit the while loop (ends program)
        
        else:
            # User entered invalid option (not 1-8)
            print("Invalid option. Please select 1-8.")