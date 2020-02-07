'''
Base code is from https://github.com/maciejkula/spotlight
'''
import numpy as np
import matplotlib.pyplot as plt
import warnings
from spotlight.cross_validation import random_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel
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
showMultiple = True

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
numUsers = dataset.num_users
# Since IDs range from 1 to 1682, number of Movies should be 1682, not 1683.
numMovies = dataset.num_items
file = "ml-latest-small/movielens_movies.txt"

userIds = dataset.user_ids
movieIds = dataset.item_ids # range from 1 to 1682
uniqueMovieIds = list(set(movieIds)) # list of movie ids removing repeated ids



#allRowTitles, allRowGenres = formatRows(allRows,numMovies)
#print(extractTitlesFromText())


userRatings = get_user_pref(5)
'''
userRatings = ['Dracula: Dead and Loving It', 1,
               'Four Rooms', 3,
               'Clear and Present Danger', 4,
               'Farewell My Concubine', 5]
'''

ratedIds, ratings = assignMovieTitle(file,True,movieIdArray=uniqueMovieIds,ratings=userRatings)

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
labelsAsColours, arrayOfIds, labelsAsGenres, idNoLabel = assignSingleLabel(uniqueMovieIds,file , showNone, showMultiple)
#print("length ",len(arrayOfIds))
#print(len(Y),len(predictions),len(labels),len(uniqueMovieIds))

        
#print(numUsers,len(userIds)        944  100000
#print(numMovies,len(movieIds))    1683 100000
#print(ratings,len(ratings))                     100000

warnings.simplefilter(action='ignore', category=FutureWarning)
############################################################################ MODELLING
#Split the dataset to evaluate the model

train, test = random_train_test_split(dataset,0.2)

print('Split into \n {} and \n {}.'.format(train, test))

model = ExplicitFactorizationModel(n_iter=modelIterations, embedding_dim=embedding_dim, learning_rate=learning_rate)

#x = model.
#model._net.item_embeddings.weight[i].detach()

# WORK ON NEW EXPLANATION INTERFACES HERE.
print("DATATSET RATINGS:")
'''
x = dataset.user_ids==8
ratingX = dataset.ratings[x]
print(len(ratingX))
'''


# Can be used to provide recommendations for a specific existing user in the database
#userID, numberRec = validateID()

userID = 944 #Corresponds to the ID of the added user
numberRec = 4

rmseResults = np.empty((modelSteps*numberDataSplits,2))
arrayOfSteps = []
indexPreviousClosest = ["0"]

#if (numberDataSplits > 1):
arraySplits = dataSplit(train,numberDataSplits)
print("Data set split into",len(arraySplits),"*",(arraySplits[1]))


# Each model step fits the entire dataset
splitCounter = 0
fullStepCounter = 0   # increases each time the entire data set has been visited
currentStep = 0       # increases at every split of the data set (does not reset)
for i in range (modelSteps*numberDataSplits):
    print("\nStarting step",fullStepCounter)
    print("Data split",splitCounter)
    fig,ax = plt.subplots()
    if (numberDataSplits == 1):
        model.fit(train, verbose=True)
    elif (numberDataSplits > 1):
        model.fit(arraySplits[splitCounter], verbose=True)

    else:
        print("Invalid number of data splits")
        break
        

    #predictions for any user are made for all items, matrix has shape (944, 1683)
    modelPredict = np.empty((numUsers,numMovies))
    for userIndex in range (numUsers):
        modelPredict[userIndex,:] = model.predict(userIndex)

    # We take the transpose for tsne formatting (should be more rows than columns)
    modelPredict = modelPredict.T

    #Measure the model's effectiveness (how good predictions are):
    rmse = rmse_score(model, test)
    rmseTrain = rmse_score(model, train)
    rmseTest = rmse_score(model, test)
    rmseResults[i,:] = [rmseTrain, rmseTest]
    arrayOfSteps += [i]
    #print('Train RMSE {:.3f}, test RMSE {:.3f}'.format(rmseTrain, rmseTest))

    if(stopTraining(rmseResults,arrayOfSteps)):
        rmseResults = rmseResults[:len(arrayOfSteps)]
        break
    


    ############################################################################ REPRESENTING
    
    if (modelType == "general"):
        title="Graph of all movies in the dataset"
        #scatterPlotEntireModel(modelPredict, tsneIter, perplexity, labels)
        annotationsNeeded = scatterPlotEntireModel(modelPredict,tsneIterations,perplexity,labelsAsColours)
    elif (modelType == "moviesUserX"):
        title="Graph of movies that match your preferences"
        #scatterPlotSingleUser(model, embedding_dim, idNoLabel, userIndex, numMovies, tsneIter, perplexity)
        tsnePlot ,plot1, annotationsNeeded = scatterPlotSingleUser(model,embedding_dim, idNoLabel, userID, numMovies, tsneIterations, perplexity)
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
        
    currentStep += 1



#print("closest ID MOVIES",distSmallestIndexes)
print(distSmallestIndexes)   
rowTitles,rowGenres = assignMovieTitle(file,False,movieIdArray=distSmallestIndexes)
metadata = get_metadata(rowTitles,False, True)

#print(rowTitles)
#print(rowGenres)
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
print(rmseResults)
plt.plot(arrayOfSteps,rmseResults[:,0],color='red',label='RMSE Train')
plt.plot(arrayOfSteps,rmseResults[:,1],color='blue',label='RMSE Test')
plt.legend()
plt.show()
'''





