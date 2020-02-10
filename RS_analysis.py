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
# Used to fit the model multiple times at each step
modelIterations = 1
# If greater than 1, defines number of splits in which dataset is divided before fitting the model
# Otherwise the model will be fit on the entire dataset
numberDataSplits = 2
modelSteps = 1

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

# Since IDs range from 1 to 1682, number of Movies should be 1682, not 1683.
numMovies = dataset.num_items
fileOldFormat = "ml-latest-small/movielens_movies.txt"
file = "ml-100k/u.item"
fileTitles = "ml-100k/all_titles_100k.txt"
fileIds = "ml-100k/all_ids_100k.txt"
fileNeighbours = "ml-100k/neighbours_100k.txt"

userIds = dataset.user_ids
movieIds = dataset.item_ids # range from 1 to 1682
uniqueMovieIds = list(set(movieIds)) # list of movie ids removing repeated ids

# Call needed to extract movie titles (and format them) - needed for user preferences gathering.
assignMovieTitle100kData(file)
arrayOfGenres = assignMovieGenre(fileOldFormat,fileTitles)
#allRows = assignMovieTitle(file,True,movieIdArray=uniqueMovieIds)

#allRowTitles, allRowGenres = formatRows(allRows,numMovies)
#print(extractTitlesFromText())

'''
userRatings = get_user_pref(2,fileTitles)
'''
userRatings = ['Dracula: Dead and Loving It', 1,
               'Four Rooms', 3,
               'Clear and Present Danger', 4,
               'Farewell My Concubine', 5]




ratedIds, ratings = assignMovieIds(userRatings,fileTitles,fileIds)
ratedTitles = userRatings[0::2]

addRatingsToDB(dataset, ratedIds, ratings)
#print(len(dataset.user_ids),len(dataset.item_ids),len(dataset.ratings))

############################################################################ LABELLING



#Array used to get the label for each movieId
#We need to add 0 as it is not included in the IDs.
uniqueMovieIds = [0]
for currentId in movieIds:
    if currentId not in uniqueMovieIds:
        uniqueMovieIds += [currentId]
uniqueMovieIds = np.sort(uniqueMovieIds)
        
#assignSingleLabel(movieIdArray, file, showNone, showMultiple)
labelsAsColours, arrayOfIds, labelsAsGenres = assignSingleLabel(uniqueMovieIds,arrayOfGenres,fileIds, showNone)
#print("length ",len(arrayOfIds))
#print(len(Y),len(predictions),len(labels),len(uniqueMovieIds))

        
#print(numUsers,len(userIds)        944  100000
#print(numMovies,len(movieIds))    1683 100000
#print(ratings,len(ratings))                     100000

warnings.simplefilter(action='ignore', category=FutureWarning)
############################################################################ MODELLING
#Split the dataset to evaluate the model


#x = model.
#model._net.item_embeddings.weight[i].detach()

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
print(recommendedTitles,recommendedIds)
    

'''
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


assignClosestNeighbours(model, dataset, fileNeighbours, embedding_dim, tsneIterations, perplexity) 
explanationOne(dataset, ratedIds, recommendedTitles, fileNeighbours)

#print("closest ID MOVIES",distSmallestIndexes)
#CHANGE RATEDIDS to distSmallestIndexes)
rowTitles,rowGenres = getMovieTitleGenre(fileTitles, fileIds,ratedIds,labelsAsGenres)

print(rowTitles)
print(rowGenres)
'''
metadata = get_metadata(rowTitles,False, True)


#print(metadata)




############################################################# CALLING GUI FRAMES         
displayResults(rowTitles,rowGenres,metadata,userID,numberRec)
scatterPlotDisplay(fig)
histogramDisplay(nClosestGenres,nDiffGenres)
          
if(annotationsNeeded):
    add_annot(fig,ax,plot1,arrayOfIds,labelsAsGenres)

#savePlot(currentStep,rmseTest)
if (modelSteps==1):
    plt.show()


'''






