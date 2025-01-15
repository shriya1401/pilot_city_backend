from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from api.jwt_authorize import token_required  # Assuming token authentication is required
from model.notifications import Notification  # Import the Notification model

# Create a Blueprint for the notifications API
notifications_api = Blueprint('notifications_api', __name__, url_prefix='/api')

# Use Flask-RESTful API
api = Api(notifications_api)

class NotificationAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new notification."""
            data = request.get_json()
            if not data or 'content' not in data or 'user_id' not in data:
                return {"message": "Missing required fields"}, 400

            try:
                # Create a Notification instance
                notification = Notification(
                    content=data['content'],
                    user_id=data['user_id']
                )
                notification.create()
                return jsonify(notification.read())
            except Exception as e:
                return {"message": str(e)}, 500

        @token_required()
        def get(self):
            """Retrieve a specific notification by ID."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Notification ID required"}, 400

            notification = Notification.query.get(data['id'])
            if not notification:
                return {"message": "Notification not found"}, 404

            return jsonify(notification.read())

        @token_required()
        def delete(self):
            """Delete a notification."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {"message": "Notification ID required"}, 400

            notification = Notification.query.get(data['id'])
            if not notification:
                return {"message": "Notification not found"}, 404

            try:
                notification.delete()
                return {"message": "Notification deleted successfully"}
            except Exception as e:
                return {"message": str(e)}, 500

    class _ALL(Resource):
        @token_required()
        def get(self):
            """Retrieve all notifications."""
            notifications = Notification.query.all()
            return jsonify([notification.read() for notification in notifications])

# Map API endpoints
api.add_resource(NotificationAPI._CRUD, '/notification')
api.add_resource(NotificationAPI._ALL, '/notifications')
