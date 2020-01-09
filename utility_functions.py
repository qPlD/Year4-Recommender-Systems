import numpy as np
import matplotlib.pyplot as plt
from spotlight.cross_validation import random_train_test_split
from GUI import firstFrame, startsWithNumb


'''
This File is meant to reduce clutter in the main program by defining utility functions.
'''
def formatRows(rows):
    formattedRows = []
    currentRow = ""
    counter = 0
    try:
        while (counter<len(rows)):
            
            if (startsWithNumb(rows[counter])):
                currentRow = rows[counter]

                if (counter+1<len(rows)):
                    while (startsWithNumb(rows[counter+1]) == False):
                        currentRow += rows[counter+1]
                        counter += 1
                        if (counter+1<len(rows)):
                            break
                    
                formattedRows += [currentRow]
                counter += 1
    except:
        return formattedRows
    return formattedRows


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

    
    
