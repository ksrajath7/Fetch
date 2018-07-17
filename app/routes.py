import requests

from flask import Flask, render_template, request, jsonify, redirect, json
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

@app.route("/display", methods=['POST', 'GET'])
def display():
    if (request.method == 'POST'):
        origin = request.form.get('source_city')    
        destination = request.form.get('destination_city')
        date = request.form.get('date_of_departure')
        currency = "INR"

        res = requests.get("https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search",
                            params={"apikey": app.config['API_KEY'], "origin": origin,
                            "destination": destination, "departure_date": date, "currency": currency})

        if res.status_code != 200:
            return render_template("error.html"), 404

        data = res.json()

        
        journey_id = add_to_database(origin, destination, date,  data)
        return render_template("display.html", data=Journey.query.get(journey_id).serialize)
    else:
        return render_template('error.html'), 404
        

@app.route("/error", methods=['GET'])
def error():
    return render_template("error.html")

@app.route("/export/<int:journey_id>", methods=['GET'])
def export(journey_id):
    return render_template("export.html", data=Journey.query.get(journey_id).serialize)



@app.route("/delete", methods=['POST'])
def delete():
    try:
        id = request.json['jid']
        j = Journey.query.get(id)
        it = j.itineraries
        for i in it:
            f = i.flights
            for j in f:
                db.session.delete(j)
            db.session.delete(i)
        db.session.delete(j)
        db.session.commit()

        return "success", 200
    except:
        return "error", 404
    

