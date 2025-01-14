# events.py

# imports from flask
import logging
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from __init__ import app, db  # Assuming __init__.py initializes app and db
from datetime import datetime

# Event Model
class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)  # Primary key for the event
    name = db.Column(db.String(255), nullable=False)  # Event name
    description = db.Column(db.Text, nullable=True)  # Event description
    location = db.Column(db.String(255), nullable=False)  # Event location
    start_date = db.Column(db.DateTime, nullable=False)  # Event start date
    end_date = db.Column(db.DateTime, nullable=False)  # Event end date

    def __init__(self, name, description, location, start_date, end_date):
        self.name = name
        self.description = description
        self.location = location
        self.start_date = start_date
        self.end_date = end_date

    def __repr__(self):
        return f"Event(id={self.event_id}, name={self.name}, location={self.location}, start_date={self.start_date}, end_date={self.end_date})"

    def create(self):
        """Creates a new event in the database."""
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error creating event '{self.name}': {str(e)}")
            return None
        return self

    def read(self):
        """Returns a dictionary representation of the event."""
        return {
            "event_id": self.event_id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat()
        }

    def update(self, data):
        """Updates the event with new data."""
        self.name = data.get('name', self.name)
        self.description = data.get('description', self.description)
        self.location = data.get('location', self.location)
        self.start_date = data.get('start_date', self.start_date)
        self.end_date = data.get('end_date', self.end_date)

        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error updating event '{self.name}': {str(e)}")
            return None
        return self

    def delete(self):
        """Deletes the event from the database."""
        try:
            db.session.delete(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error deleting event '{self.name}': {str(e)}")
            return None
        return self

# Initialize sample events
def initEvents():
    """Initialize some sample events in the database."""
    events = [
    Event(name='Tech Conference 2025', description='A conference about the future of technology with industry leaders and innovators.',
          location='San Francisco Convention Center, San Francisco, CA', 
          start_date=datetime(2025, 3, 12, 9, 0), end_date=datetime(2025, 3, 12, 17, 0)),
    
    Event(name='Cooking Masterclass', description='A hands-on cooking masterclass with a Michelin star chef.',
          location='Culinary Institute of America, Napa Valley, CA',
          start_date=datetime(2025, 4, 5, 10, 0), end_date=datetime(2025, 4, 5, 14, 0)),
    
    Event(name='AI and Machine Learning Workshop', description='A deep dive into the applications of AI in the modern world.',
          location='MIT Media Lab, Cambridge, MA', 
          start_date=datetime(2025, 6, 10, 13, 0), end_date=datetime(2025, 6, 10, 17, 0)),
    
    Event(name='Music Festival 2025', description='A three-day music festival featuring top bands, food trucks, and a vibrant atmosphere.',
          location='Central Park, New York City, NY', 
          start_date=datetime(2025, 7, 1, 14, 0), end_date=datetime(2025, 7, 3, 22, 0))
]


    for event in events:
        try:
            db.session.add(event)
            db.session.commit()
            print(f"Event created: {event.name}")
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Failed to create event: {event.name}. Error: {str(e)}")

# API routes to interact with events

@app.route('/events', methods=['GET'])
def get_events():
    """Returns a list of all events."""
    events = Event.query.all()
    return jsonify([event.read() for event in events])

@app.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Returns a specific event by its ID."""
    event = Event.query.get(event_id)
    if event:
        return jsonify(event.read())
    return jsonify({'error': 'Event not found'}), 404

@app.route('/event', methods=['POST'])
def create_event():
    """Creates a new event."""
    data = request.get_json()
    event = Event(
        name=data.get('name'),
        description=data.get('description'),
        location=data.get('location'),
        start_date=datetime.fromisoformat(data.get('start_date')),
        end_date=datetime.fromisoformat(data.get('end_date'))
    )
    event.create()
    return jsonify(event.read()), 201

@app.route('/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    """Updates an existing event."""
    event = Event.query.get(event_id)
    if event:
        data = request.get_json()
        event.update(data)
        return jsonify(event.read())
    return jsonify({'error': 'Event not found'}), 404

@app.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    """Deletes an event."""
    event = Event.query.get(event_id)
    if event:
        event.delete()
        return jsonify({'message': 'Event deleted successfully'}), 200
    return jsonify({'error': 'Event not found'}), 404

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
