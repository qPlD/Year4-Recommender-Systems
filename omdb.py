"""
Functions used to retrieve movie metadata from following database:
http://omdbapi.com/
"""

import os
import requests
import numpy as np
import h5py
import json 
from spotlight.datasets import _transport

def download_url(url, dest_path):

    req = requests.get(url, stream=True)
    req.raise_for_status()

    with open(dest_path, 'wb') as fd:
        for chunk in req.iter_content(chunk_size=2**20):
            fd.write(chunk)

def extract_metadata(filePath):
    with open(filePath, 'r') as data:
        metadataString = data.read()
        try:
            metadata = json.loads(metadataString)
        except:
            print("Incorrect file format. Expected Dictionnary as String")
    
    return(metadata)   

def get_metadata(movieTitles):
    """
    Retrieve movie metadata given a list of movie titles (or IMBd IDs)
    """

    url = 'http://www.omdbapi.com/?t={}&apikey=c1f95a2e'
    path = 'movie_metadata/{}.h5py' #'Github/Year4-Recommender-Systems/

    allMetadata = []

    for title in movieTitles:
        currentMovie = []
        '''
        path = _transport.get_data(url.format(title),
                                   os.path.join('movie_metadata'),#path,
                                   'omdb_{}{}'.format(title,'.hdf5'))
        '''
        filePath = path.format(title)
        download_url(url.format(title),filePath)
        
        metadata = extract_metadata(filePath)

        if (metadata['Response'] == 'False'):
            print('Movie not found!')
            currentMovie.append((None))
        else:
            currentMovie.append((metadata['Year'],metadata['Runtime'],metadata['Poster']))

        allMetadata.append(currentMovie)

        

        
      

    return(allMetadata)


metadata = get_metadata(['star_wars','qfffsq'])
print(metadata)
print(metadata[0])
