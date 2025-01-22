import logging
from sqlalchemy.exc import IntegrityError
from __init__ import db


# SearchHistory Model
class SearchHistory(db.Model):
    __tablename__ = 'search_history'

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    user = db.Column(db.String(255), nullable=False)  # User performing the search
    query = db.Column(db.String(255), nullable=True)  # Search query string
    tags = db.Column(db.JSON, nullable=True)  # JSON to store associated tags
    item_clicked = db.Column(db.String(255), nullable=True)  # Item the user clicked on

    def __init__(self, user, query=None, tags=None, item_clicked=None):
        self.user = user
        self.query = query
        self.tags = tags
        self.item_clicked = item_clicked

    def __repr__(self):
        return (f"SearchHistory(user={self.user}, query={self.query}, "
                f"tags={self.tags}, item_clicked={self.item_clicked})")

    def create(self):
        """
        Adds a new SearchHistory entry to the database.
        """
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            logging.warning(f"Error creating SearchHistory entry: {self.query}. Error: {str(e)}")
            return None
        return self

    def read(self):
        """
        Converts a SearchHistory object to a dictionary for JSON serialization.
        """
        return {
            "id": self.id,
            "user": self.user,
            "query": self.query,
            "tags": self.tags,
            "item_clicked": self.item_clicked
        }

    @staticmethod
    def init_search_history():
        """
        Ensures the SearchHistory table is created and ready for use.
        """
        try:
            db.create_all()  # Create table if it doesn't already exist
            logging.info("SearchHistory table initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to initialize SearchHistory table: {str(e)}")

    @staticmethod
    def get_user_preferences(user):
        """
        Retrieves a user's preferences based on their search and click history.
        """
        try:
            user_history = SearchHistory.query.filter_by(user=user).all()
            if not user_history:
                return {"message": f"No history found for user: {user}"}

            # Aggregate tags and clicked items
            tag_counts = {}
            clicked_items = {}

            for entry in user_history:
                # Aggregate tags
                if entry.tags:
                    for tag, count in entry.tags.items():
                        tag_counts[tag] = tag_counts.get(tag, 0) + count

                # Track clicked items
                if entry.item_clicked:
                    clicked_items[entry.item_clicked] = clicked_items.get(entry.item_clicked, 0) + 1

            return {
                "tags": tag_counts,
                "clicked_items": clicked_items
            }
        except Exception as e:
            logging.error(f"Error retrieving preferences for user {user}: {str(e)}")
            return {"error": str(e)}


