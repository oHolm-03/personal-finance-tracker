from flask import Flask, render_template, request, redirect, url_for, jsonify
from src.tracker import FinanceTracker
from src.predictor import BalancePredictor
import plotly.graph_objs as go
import plotly.utils
import json