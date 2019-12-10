import wikipedia
import os 
import copy
import pandas as pd

# https://wikipedia.readthedocs.io/en/latest/code.html#api 
# To scrape wikipedia content from the web

from app import db
from app.models import places

tag_file = '../data/tags.csv' # This file needs to be created  

import spacy
nlp = spacy.load('en_core_web_sm')
from nltk.corpus import wordnet 

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
        place = places.query.filter_by(place_id = self.place_id).first_or_404(description='There is no data with {}'.format(self.place)).update(dict(descriptionLong = self.content, descriptionShort = self.summary))
	db.session.commit()

    def __repr__(self):
        return self.content

class place_vec():
    def __init__(self, place_name, place_id):
        self.place = place_name
        self.place_id = place_id
        self.tags = pd.read_csv(tag_file)
        self.article = article(self.place, self.place_id)
        
    def create_freq_vec(self):
        doc = nlp(self.article.content)
        series = {}
        total = 0
        for tag in self.tags:
            synonyms = [tag]
	    for syn in wordnet.synsets("good"): 
                for l in syn.lemmas(): 
                    synonyms.append(l.name())
            i = 0
            for word in synonym:
                 for token in doc:
                     if token.lemma_ == word:
                         i+=1
            series[tag] = copy.deepcopy(i)
            total = total + i
	for key in series:
	    series[key] = series[key]/total
        return series




