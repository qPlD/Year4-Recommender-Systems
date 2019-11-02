import pylab
import math
import operator
import matplotlib.pyplot as plt
import numpy as np
from tsne_python.tsne import tsne

def scatterPlotEntireModel(modelPredict, tsneIter, perplexity, labels):

    '''
    Creates a scatter plot with the list of movies along with a legend (single-labels prioritising alphabetical order).
    Each movie is plotted separately, and is given a legend only if the specific plot for this label has been created.
    Movies with IDs not found in the MovieLens DataSet will be assigned a None label

    modelPredict: matrix containing predicted ratings for all user/item combinations. Shape is items x users.
    tsneIter: number of iterations to plot tSNE's visualisation
    perplexity: setting for tSNE visualisation (see sources for more info).
    labels: array of colour values for each different genre (contains as many elements as there are items).
    '''

    # Predictions.shape = (1683,2)
    predictions = tsne(tsneIter,modelPredict, 2, 4, perplexity)
    # Predictions has 1683 rows but there are only 1682 items?!
    assignSingleLabels(predictions,labels)
    return False



def scatterPlotSingleUser(model, userIndex, numMovies, tsneIter, perplexity):


    allLatentFactors = np.empty((numMovies+1,32))

    # Each latent factor vector has 32 entries, type is torch tensor.
    for i in range (numMovies):
        allLatentFactors[i,:] = model._net.item_embeddings.weight[i].detach()

    allLatentFactors[numMovies,:] = model._net.user_embeddings.weight[userIndex].detach()

    dimReduc = tsne(tsneIter,allLatentFactors, 2, 4, perplexity)

    #ion()
    
    plot1 = plt.scatter(dimReduc[:numMovies, 0], dimReduc[:numMovies, 1], 10 ,'black')
    plot2 = plt.scatter(dimReduc[numMovies, 0], dimReduc[numMovies, 1], 10 ,'red','*')


    plt.legend([plot1,plot2],['items','user '+str(userIndex)],bbox_to_anchor=(1.1, 1.05))
    return (dimReduc, plot1, True)


def showClosestPoints(tsnePlot, labels, labelsAsGenres, pointNum, verbose):
    '''
    Represents the points that are most similar to a given user.

    tsnePlot: output produced after calling the tsne function (an array containing 2D coordinates).
    pointNum: number of closest points we want to represent
    labels: array of colour values for each different genre (contains as many elements as there are items).
    labelsAsGenres: array of genres (prioritised based on alphabetical order) corresponding to movies.
    verbose: if True, prints the genres and their number of occurences in closest points.
    '''
    
    userX = tsnePlot[len(tsnePlot)-1,0]
    userY = tsnePlot[len(tsnePlot)-1,1]
    distances = []

    #Exclude the last point as it is the user point so the distance will be 0
    for index in range (len(tsnePlot)-1):
        pointX = tsnePlot[index,0]
        pointY = tsnePlot[index,1]
        dist = math.sqrt((pointX-userX)**2+(pointY-userY)**2)

        distances += [dist]

    
    distSmallestIndexes = np.argpartition(distances, pointNum)
    distSmallestIndexes = distSmallestIndexes[:pointNum]
    #Finding the labels and point coordinates associated to the indexes
    closestPoints = np.empty((pointNum,2))
    labelsClosestPoints = []
    if (verbose):
        labelsGenresClosestPoints = []
    counter = 0
    for index in distSmallestIndexes:
        if (verbose):
            labelsGenresClosestPoints += [labelsAsGenres[index]]
        labelsClosestPoints += [labels[index]]
        closestPoints[counter] += tsnePlot[index,:]
        counter += 1

    if (verbose):
        labelsOccurence = {}
        for label in labelsGenresClosestPoints:
            if label not in labelsOccurence:
                labelsOccurence[label] = 1
            else:
                labelsOccurence[label] += 1
                
        sorted_labels = sorted(labelsOccurence.items(), key=operator.itemgetter(1))
        print("\nThe genres of the "+str(pointNum)+" closest points are:")
        i = len(sorted_labels)-1
        while(i>=0):
            print(sorted_labels[i][0]+": ",sorted_labels[i][1])
            i -= 1
            
            
    assignSingleLabels(closestPoints, labelsClosestPoints)


def assignSingleLabels(tsneArray, labels):

    validPlots = []
    validLabels = []
    for i in range (len(tsneArray)):
        if (labels[i]=='cornflowerblue'):
            plotA = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'cornflowerblue')
            if 'Action' not in validLabels:
                validLabels += ['Action']
                validPlots += [plotA]
        elif (labels[i]=='darkgrey'):
            plotB = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'darkgrey')
            if 'Adventure' not in validLabels:
                validLabels += ['Adventure']
                validPlots += [plotB]
        elif (labels[i]=='lightcoral'):
            plotC = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'lightcoral')
            if 'Animation' not in validLabels:
                validLabels += ['Animation']
                validPlots += [plotC]
        elif (labels[i]=='red'):
            plotD = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'red')
            if 'Children' not in validLabels:
                validLabels += ['Children']
                validPlots += [plotD]
        elif (labels[i]=='orangered'):
            plotE = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'orangered')
            if 'Comedy' not in validLabels:
                validLabels += ['Comedy']
                validPlots += [plotE]
        elif (labels[i]=='saddlebrown'):
            plotF = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'saddlebrown')
            if 'Crime' not in validLabels:
                validLabels += ['Crime']
                validPlots += [plotF]
        elif (labels[i]=='orange'):
            plotG = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'orange')
            if 'Documentary' not in validLabels:
                validLabels += ['Documentary']
                validPlots += [plotG]
        elif (labels[i]=='darkgoldenrod'):
            plotH = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'darkgoldenrod')
            if 'Drama' not in validLabels:
                validLabels += ['Drama']
                validPlots += [plotH]
        elif (labels[i]=='gold'):
            plotI = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'gold')
            if 'Fantasy' not in validLabels:
                validLabels += ['Fantasy']
                validPlots += [plotI]
        elif (labels[i]=='darkkhaki'):
            plotJ = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'darkkhaki')
            if 'Film-Noir' not in validLabels:
                validLabels += ['Film-Noir']
                validPlots += [plotJ]
        elif (labels[i]=='yellow'):
            plotK = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'yellow')
            if 'Horror' not in validLabels:
                validLabels += ['Horror']
                validPlots += [plotK]
        elif (labels[i]=='yellowgreen'):
            plotL = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'yellowgreen')
            if 'Musical' not in validLabels:
                validLabels += ['Musical']
                validPlots += [plotL]
        elif (labels[i]=='lawngreen'):
            plotM = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'lawngreen')
            if 'Mystery' not in validLabels:
                validLabels += ['Mystery']
                validPlots += [plotM]
        elif (labels[i]=='aqua'):
            plotN = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'aqua')
            if 'Romance' not in validLabels:
                validLabels += ['Romance']
                validPlots += [plotN]
        elif (labels[i]=='darkblue'):
            plotO = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'darkblue')
            if 'Sci-Fi' not in validLabels:
                validLabels += ['Sci-Fi']
                validPlots += [plotO]
        elif (labels[i]=='indigo'):
            plotP = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'indigo')
            if 'Thriller' not in validLabels:
                validLabels += ['Thriller']
                validPlots += [plotP]
        elif (labels[i]=='violet'):
            plotQ = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'violet')
            if 'War' not in validLabels:
                validLabels += ['War']
                validPlots += [plotQ]
        elif (labels[i]=='deeppink'):
            plotR = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'deeppink')
            if 'Western' not in validLabels:
                validLabels += ['Western']
                validPlots += [plotR]
        elif (labels[i]=='black'):
            plotS = plt.scatter(tsneArray[i, 0], tsneArray[i, 1], 10 ,'black')
            if 'None' not in validLabels:
                validLabels += ['None']
                validPlots += [plotS]

    '''
    plt.legend([plot1,plot2,plot3,plot4,plot5,plot6,plot7,
                plot8,plot9,plot10,plot11,plot12,plot13,
                plot14,plot15,plot16,plot17,plot18,plot19],
               ('Action','Adventure','Animation','Children','Comedy','Crime','Documentary',
                'Drama','Fantasy','Film-Noir','Horror','Musical','Mystery',
                'Romance','Sci-Fi','Thriller','War','Western','None'))
    '''
    
    plt.legend(validPlots,validLabels,bbox_to_anchor=(1.1, 1.05))
        






        
    
