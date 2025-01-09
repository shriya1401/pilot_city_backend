import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource  # used for REST API building
from __init__ import app, db  # Import db from __init__.py to use it for commit
from api.jwt_authorize import token_required
from model.post import Post 

# Blueprint for Post API
star_api = Blueprint('star_api', __name__, url_prefix='/api')
api = Api(star_api)

class PostAPI:
    class _CRUD(Resource):
        @token_required()
        def post(self):
            """Create a new post."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'title' not in data or 'comment' not in data or 'channel_id' not in data:
                return {'message': 'Missing required fields'}, 400

            post = Post(data['title'], data['comment'], current_user.id, data['channel_id'], data.get('content', {}))
            post.create()
            return jsonify(post.read())

        @token_required()
        def get(self):
            """Retrieve a single post by ID."""
            data = request.get_json()
            if not data or 'id' not in data:
                return {'message': 'Post ID not found'}, 400

            post = Post.query.get(data['id'])
            if not post:
                return {'message': 'Post not found'}, 404

            return jsonify(post.read())

    class _RANKING(Resource):
        @token_required()
        def post(self):
            """Submit a star rating for a post."""
            current_user = g.current_user
            data = request.get_json()

            if not data or 'stars' not in data or 'post_id' not in data:
                return {'message': 'Missing required fields (stars, post_id)'}, 400

            stars = data['stars']
            if not isinstance(stars, int) or stars < 1 or stars > 5:
                return {'message': 'Invalid star ranking. Must be an integer between 1 and 5.'}, 400

            post = Post.query.get(data['post_id'])
            if not post:
                return {'message': 'Post not found'}, 404

            # Update the star rating of the post
            post._stars = stars
            db.session.commit()  # Commit the changes to the database

            return {'message': 'Post rating updated successfully'}, 201

        @token_required()
        def get(self):
            """Retrieve the star rating of a post."""
            data = request.get_json()

            if not data or 'post_id' not in data:
                return {'message': 'Post ID is required'}, 400

            post = Post.query.get(data['post_id'])
            if not post:
                return {'message': 'Post not found'}, 404

            return jsonify({
                "stars": post._stars
            })
    
    # Map resources to endpoints
    api.add_resource(_CRUD, '/post')
    api.add_resource(_RANKING, '/ranking')
