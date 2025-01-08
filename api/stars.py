import jwt
from flask import Blueprint, request, jsonify, current_app, g
from flask_restful import Api, Resource
from __init__ import app
from api.jwt_authorize import token_required
from model.post import Post  # Import the Post model

# Blueprint for Star API
star_api = Blueprint('star_api', __name__, url_prefix='/api')
api = Api(star_api)

class StarRatingAPI(Resource):
    @token_required()
    def post(self):
        """Store a star rating for a post."""
        current_user = g.current_user
        data = request.get_json()
        
        # Check for required fields
        if not data or 'stars' not in data or 'post_id' not in data:
            return {'message': 'Missing required fields (stars, post_id)'}, 400
        
        stars = data['stars']
        
        # Validate star rating range
        if not isinstance(stars, int) or stars < 1 or stars > 5:
            return {'message': 'Invalid star rating. Must be an integer between 1 and 5.'}, 400
        
        post = Post.query.get(data['post_id'])
        if not post:
            return {'message': 'Post not found'}, 404
        
        # Update the post with the new star rating
        post._stars = stars  # Overwrite or set the new rating
        post.update()  # Commit changes to the database
        
        return {'message': 'Rating submitted successfully'}, 201

    @token_required()
    def get(self):
        """Retrieve the star rating for a post."""
        data = request.get_json()
        if not data or 'post_id' not in data:
            return {'message': 'Post ID is required'}, 400
        
        post = Post.query.get(data['post_id'])
        if not post:
            return {'message': 'Post not found'}, 404
        
        return jsonify({
            "post_id": post.id,
            "stars": post._stars  # Return the star rating for the post
        })

# Map resources to endpoints
api.add_resource(StarRatingAPI, '/rating')

