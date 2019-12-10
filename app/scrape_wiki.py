import wikipedia

# https://wikipedia.readthedocs.io/en/latest/code.html#api 
# To scrape wikipedia content from the web

from app import db
from app.models import places

class article():
    """
	This class contains all the attributes of an article
    """
    def __init__(self, place_name, place_id):
        self.place_id = place_id
        self.place = place_name
        self.page = wikipedia.page(title = self.place)
        self.content = self.page.content
        self.sections = self.page.sections
        self.summary = self.page.summary

    def set_description(self):
        place = places.query.filter_by(place_id = self.place_id).update(dict(descriptionLong = self.content, descriptionShort = self.summary))
	db.session.commit()

    def __repr__(self):
        return self.content
