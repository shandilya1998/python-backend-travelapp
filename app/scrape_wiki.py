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

def logged_apply(g, func, *args, **kwargs):
    """
        g - dataframe
        func - function to apply to the dataframe
        *args, **kwargs are the arguments to func
        The method applies the function to all the elements of the dataframe and shows progress
    """
    step_percentage = 100. / len(g)
    import sys
    sys.stdout.write('apply progress:   0%')
    sys.stdout.flush()

    def logging_decorator(func):
        def wrapper(*args, **kwargs):
            progress = wrapper.count * step_percentage
            sys.stdout.write('\033[D \033[D' * 4 + format(progress, '3.0f') + '%')
            sys.stdout.flush()
            wrapper.count += 1
                return func(*args, **kwargs)
        wrapper.count = 0
        return wrapper

    logged_func = logging_decorator(func)
    res = g.apply(logged_func, *args, **kwargs)
    sys.stdout.write('\033[D \033[D' * 4 + format(100., '3.0f') + '%' + '\n')
    sys.stdout.flush()
    return res


places_lst = 'places_list.csv'
df_p = pd.read_csv(places_lst)
m = np.array()
#data_p = np.array([list(df_p.loc[:, col]) for col in df_p.columns])

def create_m(place):
    place_name, place_id = place
    v = pd.Series(place_vec(place_name, place_id).create_freq_vec())).values
    m = np.append(m, [list(v)])
    




logged_apply(df_p, create_m)

t = place_vec('place', 'place_id').create_freq_vec() # t is a numpy matrix, change in the code above

u, s, v = np.linalg.svd(t, full_matrices=True)
# Choice of the dimensions can be trained as a hyperparameter with the network on top of it or the similarity metric computation above it.




