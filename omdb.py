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
    fd.close()

def extract_metadata(filePath):

    with open(filePath, 'r') as data:
        try:
            metadataString = data.read()
            metadata = json.loads(metadataString)
        except:
            metadata['Response']=False
    #data.close()
    
    return(metadata)   

def get_metadata(movieTitles, details, wipeFile):
    """
    Retrieve movie metadata given a list of movie titles (or IMBd IDs)
    movieTitles: Array of formatted movie titles (no dates or genres).
    wipeFile: if True, will empty the contents of the metadata folder.
    """

    # 2 keys as each has a daily limit of 1000 requests: c1f95a2e | 19cc0456
    url = 'http://www.omdbapi.com/?t={}&apikey=19cc0456'
    path = 'movie_metadata/{}.h5py' #'Github/Year4-Recommender-Systems/
    folder = 'movie_metadata'

    allMetadata = []
    for title in movieTitles:
        currentMovie = []

        filePath = path.format(title)
        download_url(url.format(title),filePath)
        
        metadata = extract_metadata(filePath)

        if (metadata['Response'] == 'False') and (title!=""):
            print('Did not find "{}"'.format(title))
            currentMovie.append(None)
        elif(title != ""):
            currentMovie.append(metadata['Year'])
            currentMovie.append(metadata['Runtime'])
            currentMovie.append(metadata['Poster'])
            if(details):
                currentMovie.append(metadata['Genre'])
                currentMovie.append(metadata['Rated'])
                currentMovie.append(metadata['Director'])
                currentMovie.append(metadata['Actors'])
                currentMovie.append(metadata['Plot'])
                                 

        allMetadata.append(currentMovie)
      
    if(wipeFile):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

                
    return(allMetadata)



