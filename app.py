from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.tracker import FinanceTracker
from src.predictor import BalancePredictor
import plotly.graph_objs as go
import plotly.utils
import json

# create Flask application
app = Flask(__name__)

# create instances of the classes
tracker = FinanceTracker()
predictor = BalancePredictor(tracker)

# ROUTES
@app.route('/')
def index():
    #get summary stats
    stats = tracker.get_summary_stats()

    #get recent transactions
    recent_transactions = tracker.transactions[-10:][::-1]

    #render the HTML tempalte and pass data to it
    return render_template('index.html', stats=stats, transactions=recent_transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    #get form data, request.form is a dictionary with the form fields
    trans_type = request.form.get('type') # income or expense
    amount = float(request.form.get('amount'))
    description = request.form.get('description', '')

    #add transaction using our tracker
    tracker.add_transaction(amount, trans_type, description)

    return redirect(url_for('index'))

@app.route('/predictions')
def predictions():
    #get num days from URL parameter (def 30)
    days = request.args.get('days', 30, type=int)

    #get predictions from predictor
    result = predictor.predict_future_balance(days)

    chart_json = None
    trend_info = None

    if result:
        future_dates, predictions, hist_dates, hist_balances = result
        trend_info = predictor.get_trend_info()

        historical_trace = go.Scatter(
            x=hist_dates,
            y=hist_balances,
            mode='lines',
            name='Historical Balance',
            line=dict(color='blue', width=2)
        )

        prediction_trace = go.Scatter(
            x=future_dates,
            y=predictions,
            mode='lines',
            name='Predicted Balance',
            line=dict(color='red', width=2, dash='dash')
        )

        data = [historical_trace, prediction_trace]

        layout = go.Layout(
            title='Balance History and Predictions',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Balance ($)'),
            hovermode='closest',
            template='plotly_white'
        )

        fig = go.Figure(data=data, layout=layout)

        chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return render_template('predictions.html', chart_json=chart_json, trend_info=trend_info, days=days)
    
@app.route('/analytics')
def analytics():
    stats = tracker.get_summary_stats()

    data = [
        go.Bar(
            x=['Income', 'Expenses'],
            y=[stats['total_income'], stats['total_expenses']],
            marker=dict(color=['green', 'red']),
            text=[f"${stats['total_income']:,.2f}", f"${stats['total_expenses']:,.2f}"],
            textposition='outside'
        )
    ]

    layout = go.Layout(
        title='Income vs Expenses',
        yaxis=dict(title='Amount ($)'),
        template='plotly_white'
    )

    fig = go.Figure(data=data, layout=layout)
    chart_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('analytics.html', chart_json=chart_json, stats=stats)
    
@app.route('/delete_transaction/<int:index>')
def delete_transaction(index):
    if 0 <= index < len(tracker.transactions):
        tracker.transactions.pop(index)
        tracker.save_data()

        return redirect(url_for('index'))
    
# Run the server
if __name__ == '__main__':
    print("\n" + "="*60)
    print("Starting Personal Finance Tracker Web App")
    print("="*60)
    print("Open your browser and go to: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)