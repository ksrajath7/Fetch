from flask import Flask, render_template, request, jsonify
import requests


from app import app

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

    
    # res = requests.get(f"https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?apikey={app.config['API_KEY']}&origin={origin}&destination={destination}&departure_date={date}&currency=INR")
    

    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    data = res.json()

    # data['results']['itineraries']['outbound']['duration']
    # origin
    # destination
    # date
    # data['results']['fare']['price_per_adult']['tax']
    # data['results']['fare']['price_per_adult']['total_fare']

    # flights = data['results']['itineraries']['outbound']['flights']
    # for flight in flights:
    #     flight['operating_airline']
    #     flight['flight_number']
    #     origin_airport = flight['origin']['airport']
    #     destination_airport = flight['destination']['airport']



    return jsonify(data)