'''
Base code is from https://github.com/maciejkula/spotlight
'''
import numpy as np
import random
import matplotlib.pyplot as plt
import warnings
from spotlight.cross_validation import random_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.interactions import Interactions
from csv_to_txt import *
from omdb import get_metadata
from graph_plotter import scatterPlotEntireModel
from graph_plotter import scatterPlotSingleUser
from graph_plotter import scatterPlotAllUsers
from graph_plotter import showClosestFarthestLabelPoints
from graph_interactive import add_annot
from utility_functions import *
from GUI import *



'''
PROGRAM PARAMETERS FOR TESTING ----------------------------------------------------------------
'''
showNone = False
loadRatings = False

perplexity = 40#5
# Iterations that will occur at each step (multiply by steps to get total iterations)
# Number of iterations to run when building the model
modelIterations = 1
# If greater than 1, defines number of splits in which dataset is divided before fitting the model
# Otherwise the model will be fit on the entire dataset
numberDataSplits = 10
modelSteps = 10
tsneIterations = 200

# Current types are general, neighboursUserX, moviesUserX
modelType = "moviesUserX"

embedding_dim = 10
learning_rate = 5e-3#1e-2

'''
END OF TESTING PARAMETERS ----------------------------------------------------------------------
'''

#Datasets options: https://grouplens.org/datasets/movielens/
dataset = get_movielens_dataset(variant='100K')
#Number of DIFFERENT users and movies per list (!= length of lists)

fileOldFormat = "ml-latest-small/movielens_movies.txt"
file = "ml-100k/u.item"
fileTitles = "ml-100k/all_titles_100k.txt"
fileIds = "ml-100k/all_ids_100k.txt"
fileGenres = "ml-100k/all_genres_100k.txt"
fileNeighUsers = "ml-100k/neighbours_users100k.txt"
fileParticipantRatings = "ml-100k/participant_ratings.txt"

def initialise_files(fileOldFormat, file, fileTitles, fileIds, fileGenres):
    '''
    Creates files containing all movie tiles, ids and genres for the 100k dataset.
    '''
    assignMovieTitle100kData(file,fileTitles,fileIds)
    assignMovieGenre(fileOldFormat,fileTitles,fileGenres)

#Only need to run function once at the start of the project.
#initialise_files(fileOldFormat, file, fileTitles, fileIds, fileGenres)





userRatings = get_user_pref(6,fileTitles,fileGenres)

#Used for testing
'''
userRatings = ['GoldenEye', 4, 'Twelve Monkeys', 4,
               'Seven', 4, 'Il Postino', 3,
               'Braveheart', 4, 'Taxi Driver', 5,
               'Belle de jour', 1, 'Legends of the Fall', 5,
               'Pulp Fiction', 5, 'Three Colors: Red', 4,
               'Three Colors: Blue', 4, 'Three Colors: White', 4,
               'Germinal', 4, 'Nightwatch', 3,
               'The Outlaw', 4, 'Gabbeh', 1,
               'Forrest Gump',4,'The Firm',4]

'''
#Save the ratings in case of unexpected crash
if (loadRatings):
    userRatings = loadRatings(fileParticipantRatings)
else:
    saveParticipantData(fileParticipantRatings, userRatings, "Ratings:",'w')


print("Provided Ratings: ",userRatings)

ratedIds, ratings = assignMovieIds(userRatings,fileTitles,fileIds)
ratedTitles = userRatings[0::2]

addRatingsToDB(dataset, ratedIds, ratings)
############################################################################ LABELLING

uniqueMovieIds = np.arange(1,dataset.num_items)

#assignSingleLabel(movieIdArray, file, showNone, showMultiple)
arrayOfColours, arrayOfIds, arrayOfGenres = assignSingleLabel(uniqueMovieIds, fileIds, fileGenres, showNone)


warnings.simplefilter(action='ignore', category=FutureWarning)
############################################################################ MODELLING
#Split the dataset to evaluate the model


# Can be used to provide recommendations for a specific existing user in the database

userID = 944 #Corresponds to the ID of the added user
numberRec = 4



#Train the model until either:
#   1. The model overfits (RMSE Test Score starts to increase again).
#   2. We have reached the number of model iterations * step.
model, rmseTableResults = trainModelUntilOverfit(dataset,
                                                 modelSteps,
                                                 modelIterations,
                                                 numberDataSplits,
                                                 embedding_dim,
                                                 learning_rate)
# We make predictions for the participant:
predictions = model.predict(userID)


recommendedTitles, recommendedIds = getBestRecommendations(predictions, numberRec, fileTitles, fileIds)
shuffledIds,shuffledTitles,shuffledRanks = shufflePredictions(recommendedTitles, recommendedIds)
print("\nShuffled Titles:",shuffledTitles)
print("\nShuffled Ids:",shuffledIds)

#Creates 2 files with closest item and user neighbours to the participant.
assignClosestNeighbours(model, dataset, fileNeighUsers, embedding_dim, perplexity)

rowSingleGenres = getMovieTitleGenre(fileTitles, fileIds,shuffledIds,arrayOfGenres)
metadata = get_metadata(shuffledTitles,False, True)

#Display baseline results for first 4 picks
print("\nDisplaying Baseline Results...")
imagesRef = displayResults(shuffledTitles[0:4],arrayOfGenres,metadata[0:4],userID,numberRec,True)

#random shuffle order of explanations:
order=[1,2,3]
random.shuffle(order)
#1: Table
#2: Scatterplot
#3: Boxplot
order=[1,2,3]
nxIndex=4
for expl in order:
    imagesRef2 = displayResults(shuffledTitles[nxIndex:nxIndex+4],arrayOfGenres,
                               metadata[nxIndex:nxIndex+4],userID,numberRec,False)
    print("Showing Explanation Method N°{}".format(expl))
    if (expl==1):
        explanationOne(dataset, shuffledIds[nxIndex:nxIndex+4], shuffledTitles[nxIndex:nxIndex+4],
                       fileNeighUsers,fileTitles)
    elif(expl==2):
        explanationTwo(model, dataset, shuffledIds[nxIndex:nxIndex+4], arrayOfGenres, arrayOfColours, fileTitles,
                       embedding_dim, tsneIterations, perplexity)
    else:
        explanationThree(dataset, shuffledIds[nxIndex:nxIndex+4], shuffledTitles[nxIndex:nxIndex+4])
    nxIndex += 4


saveParticipantData(fileParticipantRatings, order, "Order of explanations:",'a')
saveParticipantData(fileParticipantRatings, shuffledIds, "ID / Title / Rank",'a',shuffledTitles,shuffledRanks)




