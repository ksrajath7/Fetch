import requests

from flask import Flask, render_template, request, jsonify
from app import app, db
from app.models import Flight, Itinerary, Journey

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/display", methods=['POST'])
def display():

    origin = request.form.get('source_city')    
    destination = request.form.get('destination_city')
    date = request.form.get('date_of_departure')
    currency = "INR"

    res = requests.get("https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search",
                        params={"apikey": app.config['API_KEY'], "origin": origin,
                        "destination": destination, "departure_date": date, "currency": currency})

    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()

    # Check for duplicates?

    j = Journey(origin=origin, destination=destination, date=str(date))
    db.session.add(j)
    db.session.commit()

    j.add_itinerary(data['results'])




    return jsonify(data)