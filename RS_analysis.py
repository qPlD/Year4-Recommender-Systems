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
from csv_to_txt import assignSingleLabel
from graph_plotter import scatterPlotEntireModel
from graph_plotter import scatterPlotSingleUser
from graph_plotter import scatterPlotAllUsers
from graph_plotter import showClosestFarthestLabelPoints
from graph_interactive import add_annot

def savePlot(currentStep,rmseTest):
    if(len(str(currentStep))==1):
        stepN = '0'+str(currentStep)
    else:
        stepN = str(currentStep)
    filename='Animations/step'+stepN+'.png'
    plt.title(("Plot type: "+modelType+", Step: "+stepN+", Test RMSE: ",rmseTest))
    plt.savefig(filename, dpi=96)
    plt.close() 

'''
PROGRAM PARAMETERS FOR TESTING ----------------------------------------------------------------
'''
showNone = False
showMultiple = False

perplexity = 30
#Iterations that will occur at each step (multiply by steps to get total iterations)
modelIterations = 1
modelSteps = 50


tsneIterations = 500

# Current types are general, neighboursUserX, moviesUserX
modelType = "neighboursUserX"
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

        
#print(numUsers,len(userIds)        944  100000
#print(numMovies,len(movieIds))    1683 100000
#print(ratings,len(ratings))                     100000

warnings.simplefilter(action='ignore', category=FutureWarning)
############################################################################ MODELLING
#Split the dataset to evaluate the model
train, test = random_train_test_split(dataset,0.2)
print('Split into \n {} and \n {}.'.format(train, test))

model = ExplicitFactorizationModel(n_iter=modelIterations)

currentStep = 0
rmseResults = np.empty((modelSteps,2))
arrayOfSteps = []
indexPreviousClosest = ["0"]
for i in range (modelSteps):
    print("\nStarting step",currentStep)
    fig,ax = plt.subplots()
    model.fit(train, verbose=True)

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


    ############################################################################ REPRESENTING
    
    if (modelType == "general"):
        #scatterPlotEntireModel(modelPredict, tsneIter, perplexity, labels)
        annotationsNeeded = scatterPlotEntireModel(modelPredict,tsneIterations,perplexity,labelsAsColours)
    elif (modelType == "moviesUserX"):
        #scatterPlotSingleUser(model, userIndex, numMovies, tsneIter, perplexity)
        tsnePlot ,plot1, annotationsNeeded = scatterPlotSingleUser(model, idNoLabel, 1, numMovies, tsneIterations, perplexity)
        #showClosestFarthestLabelPoints(tsnePlot, labels, labelsAsGenres, pointNum, farthest, verbose)
        showClosestFarthestLabelPoints(tsnePlot, labelsAsColours,labelsAsGenres, 5, True, True)
    
    elif (modelType == "neighboursUserX"):
        
        if "0" in indexPreviousClosest:
            neighbourUsersIndexes, annotationsNeeded = scatterPlotAllUsers(model, 60, numUsers, 5, tsneIterations, perplexity)
            indexPreviousClosest = neighbourUsersIndexes[:5]

        else:
            print("The 5 previous closest users are:",indexPreviousClosest)

            #scatterPlotAllUsers(model, userIndex, numUsers, pointNum, tsneIter, perplexity)
            neighbourUsersIndexes, annotationsNeeded = scatterPlotAllUsers(model, 60, numUsers, 5, tsneIterations, perplexity,indexPreviousClosest)
            indexPreviousClosest = neighbourUsersIndexes[:5]


    else:
        print("Invalid Model Type")
    

    if (i+1 != modelSteps):
        savePlot(currentStep,rmseTest)
        currentStep += 1




                
if(annotationsNeeded):
    add_annot(fig,ax,plot1,arrayOfIds,labelsAsGenres)

savePlot(currentStep,rmseTest)
if (modelSteps==1):
    plt.show()
'''
if(len(str(currentStep))==1):
    stepN = '0'+str(currentStep)
else:
    stepN = str(currentStep)
filename='Animations/step'+stepN+'.png'
plt.title("Plot type: "+modelType+", Step: "+stepN)
plt.savefig(filename, dpi=96)
'''
print(rmseResults)
plt.plot(arrayOfSteps,rmseResults[:,0],color='red',label='RMSE Train')
plt.plot(arrayOfSteps,rmseResults[:,1],color='blue',label='RMSE Test')
plt.legend()
plt.show()






