from app import models, db
from app.models import Journey

def add_to_database(origin, destination, date, data):
    j = Journey(origin=origin, destination=destination, date=str(date))
    db.session.add(j)
    db.session.commit()
    j.add_itinerary(data['results'])
    return j.id


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


