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
