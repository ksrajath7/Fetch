from app import models
from app.models import Journey

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

def dictify(journey_id):
    journey = Journey.query.get(journey_id)
    data = {'origin': journey.origin, 'destination': journey.destination,
            'date': journey.date}
    new_list = []
    for it in journey.itineraries:
        new_dict = {'duration': it.duration, 'price_per_adult': it.price_per_adult,
                    'tax': it.tax}
        flight_list = []
        for flight in it.flights:
            flight_dict = {'flight_number': flight.flight_number,
                            'airline': flight.airline,
                            'origin': flight.origin,
                            'destination': flight.destination,
                            'departure_time': flight.departure_time,
                            'arrival_time': flight.arrival_time}
            flight_list.append(flight_dict)
        new_dict['flights'] = flight_list
        new_list.append(new_dict)
    data['itineraries'] =  new_list
    return data
    
    
