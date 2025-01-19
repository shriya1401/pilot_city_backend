from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.events import Event  # Import the Event model

# Create a Blueprint for the event API
event_api = Blueprint('event_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(event_api)

class EventAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new event."""
            data = request.get_json()
            if not data or 'name' not in data or 'location' not in data or 'date' not in data:
                return {"message": "Missing required fields"}, 400

            try:
                # Validate the date format (YYYY-MM-DD)
                try:
                    event_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                except ValueError:
                    return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

                # Create an Event instance
                event = Event(
                    name=data['name'],
                    location=data['location'],
                    date=event_date
                )
                event.create()
                return jsonify(event.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def get(self):
            """Retrieve a specific event by ID."""
            data = request.get_json()
            if not data or 'event_id' not in data:
                return {"message": "Event ID required"}, 400

            event = Event.query.get(data['event_id'])
            if not event:
                return {"message": "Event not found"}, 404

            return jsonify(event.read())

        @token_required()
        def put(self):
            """Update an existing event."""
            data = request.get_json()
            if not data or 'event_id' not in data:
                return {"message": "Event ID required"}, 400

            event = Event.query.get(data['event_id'])
            if not event:
                return {"message": "Event not found"}, 404

            try:
                if 'name' in data:
                    event.name = data['name']
                if 'location' in data:
                    event.location = data['location']
                if 'date' in data:
                    try:
                        event.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
                    except ValueError:
                        return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

                event.update()
                return jsonify(event.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def delete(self):
            """Delete an event."""
            data = request.get_json()
            if not data or 'event_id' not in data:
                return {"message": "Event ID required"}, 400

            event = Event.query.get(data['event_id'])
            if not event:
                return {"message": "Event not found"}, 404

            try:
                event.delete()
                return {"message": "Event deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all events."""
            events = Event.query.all()
            return jsonify([event.read() for event in events])

# Map API endpoints
api.add_resource(EventAPI._CRUD, '/event')
api.add_resource(EventAPI._ALL, '/events')
