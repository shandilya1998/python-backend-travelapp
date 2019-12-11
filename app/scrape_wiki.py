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

import pickle

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

user_data = 'users_visit_data.csv'
df_u = pd.read_csv(user_data)
m_user = np.array()

def create_m(place):
    # places_list.csv should contain data in this format
    place_name, place_id = place
    v = pd.Series(place_vec(place_name, place_id).create_freq_vec())).values
    m = np.append(m, [list(v)])
    # Add code to store df_p and df_u later
    return place_name, place_id, v

def create_m_user(self, U):
    """
        This function creates the matrix of user and visit frequency values
        user is the user_id as stored in the database
        data is a dict with all the tags as keys and the normalized number of times 
        the user has visited a place with the said tag as values
    """
    user, data = U
    m_user = np.append(m_user, [list(pd.Series(data).values)])

# store the list of initial dimensions ie all the tags, maintaining the order
f = 'matrix_place_tag.pickle'
pkl = open(f, 'wb')
pickle.dump(m, pkl)
pkl.close()

logged_apply(df_p, create_m)

# Applying SVD to the matrix
u, s, v = np.linalg.svd(m, full_matrices=True)
# Choice of the dimensions can be trained as a hyperparameter with the network on top of it or the similarity metric computation above it.
m_ = np.matmul(np.matmul(u, s), v)

f = 'matrix_user_tag.pickle'
pkl = open(f, 'wb')
pickle.dump(m_user, pkl)
pkl.close()

u_user, s_user, v_user = np.linalg.svd(m_user, full_matrices = True)
# The number of dimensions for the latent space here will also be a hyperparameter for the system training

m_user_ = np.matmul(np.matmul(u_user, s_user), v_user)

#R = np.matmul(m_, m_user_)
R = np.matmul(m, m_user)
f = 'place_user_relationship.pickle'
pkl = open(f, 'wb')
pickle.load(R, pkl)
pkl.close()

import tensorflow
import keras
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.datasets import mnist
from keras.models import Model, Sequential
from keras.layers import Dense, Conv2D, Dropout, BatchNormalization, Input, Reshape, Flatten, Deconvolution2D, Conv2DTranspose, MaxPooling2D, UpSampling2D
from keras.layers.advanced_activations import LeakyReLU
from keras.optimizers import adam

def get_data():
    return "This function returns the data available"

class CNN:
    def __init__(self, x, train = True):
        self.input = Input(tensor = x)
        if train:
            self.h = self.encode()
            self.decoded = self.decode()
            self.model = self.get_model()
            print(self.model.summary())
            self.data = get_data()


    def encode(self):
        self.l1_conv = Conv2D(32, (3, 3), activation='relu')(self.input)
        self.l2_pool = MaxPooling2D((2, 2))(self.l1_conv)
        self.l3_conv = Conv2D(64, (3, 3), activation='relu')(self.l2_pool)
        self.l4_pool = MaxPooling2D((2, 2))(self.l3_conv)
        self.l5_conv = Conv2D(64, (3, 3), activation='relu')(self.l4_pool)
        self.l6_flat = Flatten()(self.l5_conv)
        return Dense(49, activation='softmax')(self.l6_flat)
    
    def decode(self):
        self.l1_reshape = Reshape((7,7,1))(self.h)
        self.l2_convT = Conv2DTranspose(64,(3, 3), strides=2, activation='relu', padding='same')(self.l1_reshape)
        self.l3_bn = BatchNormalization()(self.l2_convT)
        self.l4_convT = Conv2DTranspose(64,(3, 3), strides=2, activation='relu', padding='same')(self.l3_bn)
        self.l5_bn = BatchNormalization()(self.l4_convT)
        self.l6_convT = Conv2DTranspose(32,(3, 3), activation='relu', padding='same')(self.l5_bn)
        return Conv2D(1, (3, 3), activation='sigmoid', padding='same')(self.l6_convT)

    def get_model(self):
        return Model(self.input, self.decoded)

    def train(self):
        # Compile model using adam optimizer
        self.model.compile(optimizer="adam", loss="mse")
        
        # Train model by providing training data
        self.model.fit(self.train_data(), epochs=2)
        
        # To save the model
        model_json = self.to_json()
        with open("model_tex.json", "w") as json_file:
            json_file.write(model_json)

        ae.save_weights("model_tex.h5")
        print("Saved model")

    def train_data(self):
        return "This function returns training data"




"""
    u - number of users
    p - number of places
    t - number of tags

    Since the significance of the latent space vectors is not known, 
    nothing can be claimed about what the elements of the matrix obtained
    by the aforementioned matrix multiplications signify.
    Training a neural network with an input matrix () obtained by the dot product
    of  user vector and all place vectors can provide with the model of what 
    a user's preferences are.
"""



