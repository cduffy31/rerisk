from flask import Flask, render_template, url_for, request
from risk_engine.risk import RiskModel as re
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy()
db.init_app(app)



class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Request %r>' % self.ticker


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about_risk')
def about():
    return render_template('about_risk.html')


@app.route('/req/', methods=['POST', 'GET'])
def req():
    if request.method == 'GET':
        return f"wrong url"
    if request.method == 'POST':
        ticker = request.form['ticker']
        risk = re(ticker,"2020-12-06", "1d")
        return render_template("test_input.html", b5=risk.bottom_five(), nd=risk.norm_dist())


if __name__ == "__main__":
    app.run( debug=True)
