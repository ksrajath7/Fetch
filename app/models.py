from app import db
from sqlalchemy import and_, or_

# Possible itineraries
class Journey(db.Model):
    __tablename__ = "journeys"
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

    itineraries = db.relationship("Itinerary", backref="journey", lazy=True)

    def add_itinerary(self, results):
        for result in results:
            i = Itinerary(duration=result['itineraries'][0]['outbound']['duration'],
                        price_per_adult=result['fare']['price_per_adult']['total_fare'],
                        tax=result['fare']['price_per_adult']['tax'], journey_id=self.id)
            db.session.add(i)
            db.session.commit()
            i.add_flight(result['itineraries'][0]['outbound']['flights'])




class Itinerary(db.Model):
    __tablename__ = "itineraries"
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.String, nullable=False)
    price_per_adult = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, nullable=False)

    journey_id = db.Column(db.Integer, db.ForeignKey("journeys.id"), nullable=False)

    flights = db.relationship("Flight", backref="itinerary", lazy=True)

    def add_flight(self, flights):
        for flight in flights:
            f = Flight(flight_number=str(flight['flight_number']),
                        airline=str(flight['operating_airline']),
                        origin=str(flight['origin']['airport']),
                        destination=str(flight['destination']['airport']),
                        departure_time=str(flight['departs_at']),
                        arrival_time=str(flight['arrives_at']),
                        itinerary_id=self.id)
            db.session.add(f)
            db.session.commit()


class Flight(db.Model):
    __tablename__ = "flights"
    id = db.Column(db.Integer, primary_key=True)
    flight_number = db.Column(db.String, nullable=False)
    airline = db.Column(db.String, nullable=False)
    origin = db.Column(db.String, nullable=False)
    destination = db.Column(db.String, nullable=False)
    departure_time = db.Column(db.String, nullable=False)
    arrival_time = db.Column(db.String, nullable=False)

    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False)



