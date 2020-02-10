import csv
import numpy as np
import matplotlib.pyplot as plt
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
        if(lineTitle[-3:]==' An'):
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

    print(ratedIds)
    print(dataset.num_items)

    
    dataset.item_ids = np.append(dataset.item_ids,ratedIds)
    dataset.ratings = np.append(dataset.ratings,ratings)
    dataset.user_ids = np.append(dataset.user_ids,userID)
    dataset.timestamps = np.append(dataset.timestamps,timestamps)

    
    dataset.num_users += 1


    
    
    
