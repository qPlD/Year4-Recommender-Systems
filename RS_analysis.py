'''
Base code is from https://github.com/maciejkula/spotlight
'''
import numpy as np
import matplotlib.pyplot as plt
from spotlight.cross_validation import random_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel
from spotlight.interactions import Interactions
from csv_to_txt import assignSingleLabel
from graph_plotter import scatterPlotEntireModel
from graph_plotter import scatterPlotSingleUser
from graph_plotter import scatterPlotAllUsers
from graph_plotter import showClosestFarthestLabelPoints
from graph_interactive import add_annot

def savePlot(currentStep):
    if(len(str(currentStep))==1):
        stepN = '0'+str(currentStep)
    else:
        stepN = str(currentStep)
    filename='Animations/step'+stepN+'.png'
    plt.title("Plot type: "+modelType+", Step: "+stepN)
    plt.savefig(filename, dpi=96)

'''
PROGRAM PARAMETERS FOR TESTING ----------------------------------------------------------------
'''
showNone = False
showMultiple = False

perplexity = 15
#Iterations that will occur at each step (multiply by steps to get total iterations)
modelIterations = 5
modelSteps = 5

tsneIterations = 40

# Current types are general, neighboursUserX, moviesUserX
modelType = "moviesUserX"
'''
END OF TESTING PARAMETERS ----------------------------------------------------------------------
'''

#Datasets options: https://grouplens.org/datasets/movielens/
dataset = get_movielens_dataset(variant='100K')

userIds = dataset.user_ids
movieIds = dataset.item_ids # range from 1 to 1682

#Number of DIFFERENT users and movies per list (!= length of lists)
numUsers = dataset.num_users

# Since IDs range from 1 to 1682, number of Movies should be 1682, not 1683.
numMovies = dataset.num_items
userRatings = dataset.ratings

print(len(userRatings))
############################################################################ LABELLING
file = "ml-latest-small/movielens_movies.txt"

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
fig,ax = plt.subplots()

        
#print(numUsers,len(userIds)        944  100000
#print(numMovies,len(movieIds))    1683 100000
#print(ratings,len(ratings))                     100000


############################################################################ MODELLING
#Split the dataset to evaluate the model
train, test = random_train_test_split(dataset)
print('Split into \n {} and \n {}.'.format(train, test))

model = ExplicitFactorizationModel(n_iter=modelIterations)

currentStep = 0
for i in range (modelSteps):
    model.fit(train, verbose=True)

    #predictions for any user are made for all items, matrix has shape (944, 1683)
    modelPredict = np.empty((numUsers,numMovies))
    for userIndex in range (numUsers):
        modelPredict[userIndex,:] = model.predict(userIndex)

    # We take the transpose for tsne formatting (should be more rows than columns)
    modelPredict = modelPredict.T

    #Measure the model's effectiveness (how good predictions are):
    rmse = rmse_score(model, test)
    train_rmse = rmse_score(model, train)
    test_rmse = rmse_score(model, test)
    print('Train RMSE {:.3f}, test RMSE {:.3f}'.format(train_rmse, test_rmse))


    ############################################################################ REPRESENTING
    if (modelType == "general"):
        #scatterPlotEntireModel(modelPredict, tsneIter, perplexity, labels)
        annotationsNeeded = scatterPlotEntireModel(modelPredict,tsneIterations,perplexity,labelsAsColours)
    elif (modelType == "moviesUserX"):
        #scatterPlotSingleUser(model, userIndex, numMovies, tsneIter, perplexity)
        tsnePlot ,plot1, annotationsNeeded = scatterPlotSingleUser(model, idNoLabel, 1, numMovies, tsneIterations, perplexity)
        #showClosestFarthestLabelPoints(tsnePlot, labels, labelsAsGenres, pointNum, farthest, verbose)
        showClosestFarthestLabelPoints(tsnePlot, labelsAsColours,labelsAsGenres, 50, True, True)
    
    elif (modelType == "neighboursUserX"):
        #scatterPlotAllUsers(model, userIndex, numUsers, pointNum, tsneIter, perplexity)
        neighbourUsersIndexes, annotationsNeeded = scatterPlotAllUsers(model, 60, numUsers, 5, tsneIterations, perplexity)

    else:
        print("Invalid Model Type")
    

    if (i+1 != modelSteps):
        savePlot(currentStep)
        currentStep += 1



                
if(annotationsNeeded):
    add_annot(fig,ax,plot1,arrayOfIds,labelsAsGenres)

savePlot(currentStep)
'''
if(len(str(currentStep))==1):
    stepN = '0'+str(currentStep)
else:
    stepN = str(currentStep)
filename='Animations/step'+stepN+'.png'
plt.title("Plot type: "+modelType+", Step: "+stepN)
plt.savefig(filename, dpi=96)
#plt.show()
'''





