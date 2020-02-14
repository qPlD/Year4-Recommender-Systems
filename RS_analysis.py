'''
Base code is from https://github.com/maciejkula/spotlight
'''
import numpy as np
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

perplexity = 20#5
# Iterations that will occur at each step (multiply by steps to get total iterations)
# Number of iterations to run when building the model
modelIterations = 1
# If greater than 1, defines number of splits in which dataset is divided before fitting the model
# Otherwise the model will be fit on the entire dataset
numberDataSplits = 2
modelSteps = 2
tsneIterations = 20

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

def initialise_files(fileOldFormat, file, fileTitles, fileIds, fileGenres):
    '''
    Creates files containing all movie tiles, ids and genres for the 100k dataset.
    '''
    assignMovieTitle100kData(file,fileTitles,fileIds)
    assignMovieGenre(fileOldFormat,fileTitles,fileGenres)

#Only need to run function once at the start of the project.
initialise_files(fileOldFormat, file, fileTitles, fileIds, fileGenres)

#allRowTitles, allRowGenres = formatRows(allRows,numMovies)
#print(extractTitlesFromText())

'''
userRatings = get_user_pref(6,fileTitles)

#FIX THIS ERROR
userRatings = ['Nadja', 4, 'Three Colors: White', 4, 'Remains of the Day', 3,
'Mystery Science Theater 3000: The Movie', 5, 'D3: The Mighty Ducks', 4,
'Wag the Dog', 3, 'Amityville II: The Possession', 2, 'First Wives Club',
4, "Wes Craven's New Nightmare", 4, 'Better Off Dead...', 5, 'Alaska',
2, 'Ma vie en rose', 1]
'''
userRatings = ['Dracula: Dead and Loving It', 1,
               "Wes Craven's New Nightmare", 4,
               'Mystery Science Theater 3000: The Movie', 5,
               'Four Rooms', 3,
               'Clear and Present Danger', 4,
               'Farewell My Concubine', 5]


print(userRatings)

ratedIds, ratings = assignMovieIds(userRatings,fileTitles,fileIds)
ratedTitles = userRatings[0::2]

addRatingsToDB(dataset, ratedIds, ratings)
#print(len(dataset.user_ids),len(dataset.item_ids),len(dataset.ratings))

############################################################################ LABELLING



#Array used to get the label for each movieId
#We need to add 0 as it is not included in the IDs.
uniqueMovieIds = np.arange(0,dataset.num_items)

#assignSingleLabel(movieIdArray, file, showNone, showMultiple)
arrayOfColours, arrayOfIds, arrayOfGenres = assignSingleLabel(uniqueMovieIds, fileIds, fileGenres, showNone)


        
#print(numUsers,len(userIds)        944  100000
#print(numMovies,len(movieIds))    1683 100000
#print(ratings,len(ratings))                     100000

warnings.simplefilter(action='ignore', category=FutureWarning)
############################################################################ MODELLING
#Split the dataset to evaluate the model


# WORK ON NEW EXPLANATION INTERFACES HERE.

'''
x = dataset.user_ids==8
ratingX = dataset.ratings[x]
print(len(ratingX))
'''

# Can be used to provide recommendations for a specific existing user in the database
#userID, numberRec = validateID()

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
print("\nPredictions:",recommendedTitles,recommendedIds,"\n")
     

#Creates 2 files with closest item and user neighbours to the participant.
assignClosestNeighbours(model, dataset, fileNeighUsers, embedding_dim, perplexity)


#print("closest ID MOVIES",distSmallestIndexes)
#CHANGE RATEDIDS to distSmallestIndexes)
rowTitles,rowSingleGenres = getMovieTitleGenre(fileTitles, fileIds,recommendedIds,arrayOfGenres)
metadata = get_metadata(rowTitles,False, True)

print("\nDisplaying Baseline Results...")
imagesRef = displayResults(rowTitles,arrayOfGenres,metadata,userID,numberRec)

explanationOne(dataset, recommendedIds, recommendedTitles, fileNeighUsers)
explanationTwo(model, dataset, arrayOfGenres, arrayOfColours, fileTitles, embedding_dim, tsneIterations, perplexity)
#print(metadata)

#tsne2dArray, plot1 = scatterPlotSingleUser(model, embedding_dim, userID, dataset.num_items, tsneIterations, perplexity)
#closestItemsIDs, closestItemsGenres, numberClosestItems = showClosestFarthestLabelPoints(tsne2dArray, labelsAsColours, labelsAsGenres, 10, 4, farthest, verbose)
#print("\nSecond Recommendation using TSNE Reduction:",closestItemsIDs, closestItemsGenres, numberClosestItems)
############################################################# CALLING GUI FRAMES         

#scatterPlotDisplay(fig)
#histogramDisplay(nClosestGenres,nDiffGenres)
          
#if(annotationsNeeded):
#    add_annot(fig,ax,plot1,arrayOfIds,labelsAsGenres)

'''
#savePlot(currentStep,rmseTest)
if (modelSteps==1):
    plt.show()


    

    ############################################################################ REPRESENTING
    
    
    if (modelType == "general"):
        title="Graph of all movies in the dataset"
        #scatterPlotEntireModel(modelPredict, tsneIter, perplexity, labels)
        annotationsNeeded = scatterPlotEntireModel(modelPredict,tsneIterations,perplexity,labelsAsColours)
    elif (modelType == "moviesUserX"):
        title="Graph of movies that match your preferences"
        #scatterPlotSingleUser(model, embedding_dim, idNoLabel, userIndex, numMovies, tsneIter, perplexity)
        tsnePlot ,plot1, annotationsNeeded = scatterPlotSingleUser(model,embedding_dim, userID, numMovies, tsneIterations, perplexity)
        #showClosestFarthestLabelPoints(tsnePlot, labels, labelsAsGenres, pointNum, farthest, verbose)
        distSmallestIndexes, nClosestGenres, nDiffGenres = showClosestFarthestLabelPoints(tsnePlot, labelsAsColours,labelsAsGenres,10, numberRec, True, True)
    
    elif (modelType == "neighboursUserX"):
        title="Graph of users with similar interests"
        
        if "0" in indexPreviousClosest:
            #scatterPlotAllUsers(model, embedding_dim, userIndex, numUsers, pointNum, tsneIter, perplexity, previousClosest=["0"])
            neighbourUsersIndexes, annotationsNeeded = scatterPlotAllUsers(model, embedding_dim, userID, numUsers, numberRec, tsneIterations, perplexity)
            indexPreviousClosest = neighbourUsersIndexes[:5]

        else:
            #scatterPlotAllUsers(model, embedding_dim, userIndex, numUsers, pointNum, tsneIter, perplexity, previousClosest=["0"])
            neighbourUsersIndexes, annotationsNeeded = scatterPlotAllUsers(model, embedding_dim, userID, numUsers, numberRec, tsneIterations, perplexity,indexPreviousClosest)
            indexPreviousClosest = neighbourUsersIndexes[:5]


    else:
        print("Invalid Model Type")
        break
    

    #if (i+1 != modelSteps):
    savePlot(currentStep,rmseTest,modelType)
        #currentStep += 1

    # The entire data set has been parsed, so we start again from the first split.
    splitCounter += 1
    if (splitCounter>=len(arraySplits)):
        splitCounter = 0
        fullStepCounter += 1
'''  




