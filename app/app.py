import pandas as pd
from flask import Flask, jsonify, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

# Flask Setup
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # Remove caching
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///C:\Users\vsanh\OneDrive\Data Analysis HW\Projects\Project_3_Meteors\Database\meteorites.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Meteorite model
class Meteorites(db.Model):
    __tablename__ = "meteorites"  # Make sure this matches your actual table name
    id = db.Column(db.Integer, primary_key=True)
    rec_class = db.Column(db.String(50))
    year = db.Column(db.Integer)
    mass = db.Column(db.Float)
    rec_lat = db.Column(db.Float)
    rec_long = db.Column(db.Float)

# Route: Get all meteorites
@app.route("/api/meteorites", methods=["GET"])
def get_meteorites():
    results = Meteorites.query.all()
    return jsonify([{
        "rec_class": m.rec_class,
        "year": m.year,
        "mass": m.mass,
        "lat": m.rec_lat,
        "lon": m.rec_long
    } for m in results])

# Test route
@app.route("/")
def home():
    return "Meteorite API is running!"

if __name__ == "__main__":
    app.run(debug=True)


