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

    # Add condition to update database
    if False:
        add_to_database(origin, destination, data)

    

    return jsonify(refactor_data(origin, destination, date, data))
    # return render_template("display.html", journey=j)



def add_to_database(origin, destination, date, data):
    j = Journey(origin=origin, destination=destination, date=str(date))
    db.session.add(j)
    db.session.commit()
    j.add_itinerary(data['results'])


def refactor_data(origin, destination, date, data):
    new_data = {'origin': origin, 'destination': destination,
                'date': date}

    results = data['results']
   
    new_itineraries = []

    for result in results:
        it = {'duration': result['itineraries'][0]['outbound']['duration'],
            'price_per_adult': result['fare']['price_per_adult']['total_fare'],
            'tax': result['fare']['price_per_adult']['tax']}
        
        flights = result['itineraries'][0]['outbound']['flights']
        new_flights = []
        for flight in flights:
            f = {'flight_number': flight['flight_number'],
                'airline': flight['operating_airline'],
                'origin': flight['origin']['airport'],
                'destination': flight['destination']['airport'],
                'departure_time': flight['departs_at'],
                'arrival_time': flight['arrives_at']}
            new_flights.append(f)
        it['flights'] =  new_flights
        new_itineraries.append(it)

    new_data['itineraries'] = new_itineraries

    return new_data


    
