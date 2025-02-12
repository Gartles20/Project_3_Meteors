import pandas as pd
from flask import Flask, jsonify, render_template, redirect, request
from sql_helper import SQLHelper
import os 
from flask_sqlalchemy import SQLAlchemy

# Initialize Flask app
app = Flask(__name__)

# Flask app config
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database", "meteorites.sqlite")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DATABASE_PATH}"

# SQL Helper
sql_helper = SQLHelper()

# STATIC ROUTES

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/works_cited")
def works_cited():
    return render_template("works_cited.html")

# API ROUTES

@app.route("/api/v1.0/meteorite_counts")
def meteorite_counts():
    # Execute the query to get meteorite counts
    results = sql_helper.query_meteorite_counts()

    # Convert the DataFrame to a List of Dictionaries
    data = results.to_dict(orient="records")

    # Return the data as a JSON response
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)



