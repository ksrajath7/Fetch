import requests

from flask import Flask, render_template, request, jsonify
from app import app, db
from app.models import Flight, Itinerary, Journey

from app.helper import add_to_database, refactor_data

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/saved", methods=['GET'])
def saved():
    data = Journey.query.all()
    return render_template('save.html', data=list(data))

@app.route("/display", defaults={'journey_id': None}, methods=['GET','POST'])
@app.route("/display/<int:journey_id>", methods=['GET','POST'])
def display(journey_id):
    if request.method == 'POST':
        origin = request.form.get('source_city')    
        destination = request.form.get('destination_city')
        date = request.form.get('date_of_departure')
        update_db = request.form.get('add_to_database')
        currency = "INR"

        res = requests.get("https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search",
                            params={"apikey": app.config['API_KEY'], "origin": origin,
                            "destination": destination, "departure_date": date, "currency": currency})

        if res.status_code != 200:
            raise Exception("ERROR: API request unsuccessful.")

        data = res.json()

        if update_db == "yes":
            journey_id = add_to_database(origin, destination, date,  data)
            return render_template("display.html", data=Journey.query.get(journey_id).serialize)
        else:
            return render_template("display.html", data=refactor_data(origin, destination, date, data))
    else:
        if journey_id == None:
            return "<h1>Error in ID</h1>"
        
        return render_template("display.html", data=Journey.query.get(journey_id).serialize)


