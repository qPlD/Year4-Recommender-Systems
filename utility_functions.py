import csv
import math
import numpy as np
from tsne_python.tsne import tsne
import matplotlib.pyplot as plt
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel
from spotlight.cross_validation import random_train_test_split
#from GUI import firstFrame, startsWithNumb


'''
This File is meant to reduce clutter in the main program by defining utility functions.
'''
def stripRows(rowArray):

    rowTitles = []
    rowGenres = []
    for row in rowArray:
        numCount = 0    
        for letter in row:
            if(letter.isnumeric()):
                numCount += 1
            else:
                break
            
        stripIDLine = row[numCount+1:]

        startBracket = endBracket = 0
        firstBracket = True

        for i in range(len(stripIDLine)):
            if(stripIDLine[i]=='(') and (firstBracket):
                startBracket=i
                firstBracket = False

            elif(stripIDLine[i]==')') and (stripIDLine[i-4:i].isnumeric()):
                endBracket = i

            
        lineTitle = stripIDLine[:startBracket-1]
        lineGenre = stripIDLine[endBracket+2:]

        # Some titles have the starting word at the end, causing the movie to not be found       
        if(lineTitle[-4:]==' The'):
            lineTitle = lineTitle[:-4]
        if(lineTitle[-2:]==' A'):
            lineTitle = lineTitle[:-2]
        if(lineTitle[-3:]==' An'):
            lineTitle = lineTitle[:-3]        
            
        #print(lineTitle)
        #print(lineGenre)
        rowTitles += [lineTitle]
        rowGenres += [lineGenre]

    
    return rowTitles, rowGenres

def stripYears(rowTitleYear):

    rowTitles = []
    
    for row in rowTitleYear:
        startBracket = 0
        firstBracket = True
        
        for i in range(len(row)):
            if(row[i]=='(') and firstBracket:
                startBracket = i
                firstBracket = False
 
        lineTitle = row[:startBracket-1]

        # Some titles have the starting word at the end, causing the movie to not be found       
        if(lineTitle[-4:]==' The'):
            lineTitle = lineTitle[:-4]
        if(lineTitle[-2:]==' A'):
            lineTitle = lineTitle[:-2]
        endword=lineTitle[-3:]
        if(endword==' An')or(endword==' Il')or(endword==' Le')or(endword==' La')or(endword==' El'):
            lineTitle = lineTitle[:-3]

        rowTitles += [lineTitle]
    return rowTitles

'''            
t, i = stripRows(['87 Dunston Checks In The (1996) Children|Comedy',
           '137 Man of the Year (Homme anneee)(1995) Documentary',
           '210 Wild Bill (1995) Western',
           '416 Bad Girls (1994) Western',
           '454 Firm The (1993) Drama|Thriller',
           '458 Geronimo: An American Legend (Lamericanooooo) (1993) Drama|Western',
           '464 Hard Target (1993) Action|Adventure|Crime|Thriller',
           '493 Menace II Society (1993) Action|Crime|Drama'])
'''

def extractTitlesFromText(file):
    allTitles = []
    with open(file, "r") as outputFile:
        for row in csv.reader(outputFile):
            allTitles += row

        return(allTitles)
'''    
# Used to ensure that the user ID is a positive integer.
def validateID():
    
    firstWindow = firstFrame()
    try:
        userID = int(firstFrame.getUserID(firstWindow))
        entryNRec = int(firstFrame.getNumberRec(firstWindow))
        if(userID<0) or (entryNRec<0):
            print("Invalid Fields! Try Again.")
            userID,entryNRec = validateID()
        else:
            print("\nSelected User ID:",userID)
            print("Showing",entryNRec,"recommendations.\n")
    except:
        print("Invalid Fields! Try Again.")
        userID,entryNRec = validateID()
    return userID, entryNRec
'''
# Save the output graphs with the defined format.
def savePlot(currentStep,rmseTest,modelType):
    if(len(str(currentStep))==1):
        stepN = '0'+str(currentStep)
    else:
        stepN = str(currentStep)
    filename='Animations/step'+stepN+'.png'
    plt.title(("Plot type: "+modelType+", Step: "+stepN+", Test RMSE: ",rmseTest))
    plt.savefig(filename, dpi=96)
    plt.close()


def trainModelUntilOverfit(dataset, modelSteps, modelIterations, numberDataSplits, embedding_dim, learning_rate):

    numUsers = dataset.num_users
    numMovies = dataset.num_items
    train, test = random_train_test_split(dataset,0.2)

    print('Split into \n {} and \n {}.'.format(train, test))

    #add random seed    
    model = ExplicitFactorizationModel(n_iter=modelIterations, embedding_dim=embedding_dim, learning_rate=learning_rate)
    
    rmseResults = np.empty((modelSteps*numberDataSplits,2))
    indexPreviousClosest = ["0"]

    if (numberDataSplits > 1):
        arraySplits = dataSplit(train,numberDataSplits)
        print("Data set split into",len(arraySplits),"*",(arraySplits[1]))
    # Each model step fits the entire dataset
    arrayOfSteps = []
    splitCounter = 0
    fullStepCounter = 0   # increases each time the entire data set has been visited
    currentStep = 0       # increases at every split of the data set (does not reset)
    for i in range (modelSteps*numberDataSplits):
        print("\nStarting step",fullStepCounter)
        print("Data split",splitCounter)
        if (numberDataSplits == 1):
            model.fit(train, verbose=True)
        elif (numberDataSplits > 1):
            print(arraySplits[splitCounter])
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
        print("RMSE TEST:",rmseTest,"\n")
        rmseResults[i,:] = [rmseTrain, rmseTest]
        arrayOfSteps += [i]
        #print('Train RMSE {:.3f}, test RMSE {:.3f}'.format(rmseTrain, rmseTest))

        if(stopTraining(rmseResults,arrayOfSteps)):
            rmseResults = rmseResults[:len(arrayOfSteps)]
            break

        if (numberDataSplits > 1):
            splitCounter += 1
            if (splitCounter>=len(arraySplits)):
                splitCounter = 0
                fullStepCounter += 1
        
    currentStep += 1
    #print("\n",rmseResults,"\n")

    return(model, rmseResults)

def assignClosestNeighbours(model, dataset, fileNeighUsers, embedding_dim, perplexity):
    '''
    Creates a new file with the IDs of closest neighbours (in order from the closest to the farthest).

    '''

    #FIRST STEP: Assign neighbour users
    numUsers = dataset.num_users    
    allUserFactors = np.empty((numUsers,embedding_dim))
    
    for i in range (numUsers):
        allUserFactors[i,:] = model._net.user_embeddings.weight[i].detach()

    # We are interested in the last user that has been added to the dataset.
    participantPoints = allUserFactors[numUsers-1,:]
    distances = []

    #Compute the Euclidean distance for high dimensions (more accurate).
    for index in range (numUsers):
        userXPoints = allUserFactors[index,:]
        intermediateSum = 0
        for k in range(embedding_dim):
            intermediateSum += (participantPoints[k]-userXPoints[k])**2
            
        dist = math.sqrt(intermediateSum)
        distances += [dist]

    distIndexes = np.argsort(distances)

    with open(fileNeighUsers, 'w') as f:
        for item in distIndexes:
            f.write("%s\n" % item)
    f.close()


def getBestRecommendations(predictions, numberRec, titleFile, idFile):
    allRowTitles = []
    allIds = []
    recommendedTitles = []
    recommendedIds = []
    
    with open(titleFile, "r") as outputFile:
        for row in csv.reader(outputFile):
            allRowTitles += row
    outputFile.close()
    with open(idFile, "r") as outputFile2:
        for row in csv.reader(outputFile2):
            allIds += row
    outputFile2.close()

    sortedPred = np.argsort(predictions)
    topNPred = sortedPred[:4]

    for index in topNPred:
        recommendedTitles += [allRowTitles[index]]
        recommendedIds += [allIds[index]]

    return(recommendedTitles,recommendedIds)
    
# Incrementally split the training data in an equal number of splits.
def dataSplit(train,numberDataSplits):
    arrayOfSplits = []
    split1, split2 = random_train_test_split(train,1.0/numberDataSplits)
    arrayOfSplits += [split2]
    splitLength = len(split2.ratings)
    

    while (splitLength<len(split1.ratings)):
        splitPercentage = splitLength/len(split1.ratings)
        split1,split2 = random_train_test_split(split1,splitPercentage)
        arrayOfSplits += [split2]

    arrayOfSplits += [split1]
    return arrayOfSplits

# We stop the model when rmse Test Score begins to increase.
def stopTraining(rmseScores,arrayOfSteps):
    if (len(arrayOfSteps)<=1):
        return False
    else:
        lastIndex = arrayOfSteps[-1]
        secondLastIndex = arrayOfSteps[-2]

        
        secondLastTestScore = rmseScores[secondLastIndex,1]
        lastTestScore = rmseScores[lastIndex,1]

        if (lastTestScore <= secondLastTestScore):
            return False
        else:
            print("Model training stopped!\n")
            return True

def addRatingsToDB(dataset, ratedIds, ratings):

    ratedIds = np.asarray(ratedIds)
    ratings = np.asarray(ratings)
    ratedIds = ratedIds.astype(np.int32)
    ratings = ratings.astype(np.float32)

    userID = np.full(len(ratedIds),944)
    userID = userID.astype(np.int32)

    timestamps = np.full(len(ratedIds),879959583)
    timestamps = timestamps.astype(np.int32)

    
    dataset.item_ids = np.append(dataset.item_ids,ratedIds)
    dataset.ratings = np.append(dataset.ratings,ratings)
    dataset.user_ids = np.append(dataset.user_ids,userID)
    dataset.timestamps = np.append(dataset.timestamps,timestamps)

    
    dataset.num_users += 1


    
    
    
