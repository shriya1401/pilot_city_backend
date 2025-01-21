import logging
from sqlalchemy.exc import IntegrityError
from __init__ import db  # Assuming __init__.py initializes db

# SearchHistory Model
class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user = db.Column(db.String(255), nullable=False)  # User performing the search
    query = db.Column(db.String(255), nullable=False)  # Search query string
    tags = db.Column(db.JSON, nullable=True)  # JSON to store associated tags

    def __init__(self, user, query, tags):
        self.user = user
        self.query = query
        self.tags = tags

    def __repr__(self):
        return f"SearchHistory(user={self.user}, query={self.query}, tags={self.tags})"

# Initialize SearchHistory table with sample data
def initSearchHistory():
    """Add sample data to the SearchHistory table."""
    sample_searches = [
        SearchHistory(user="guest", query="teddy bear", tags={"all": 1, "teddy": 0, "bear": 0, "toys": 0}),
        SearchHistory(user="guest", query="lego set", tags={"all": 1, "lego": 0, "set": 0, "toys": 0}),
        SearchHistory(user="guest", query="holiday candles", tags={"all": 1, "holiday": 0, "candles": 0, "home-decor": 0}),
    ]

    for search_entry in sample_searches:
        try:
            db.session.add(search_entry)
            db.session.commit()
            print(f"SearchHistory entry created: {search_entry.query}")
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error adding SearchHistory entry: {search_entry.query}. Error: {str(e)}")
