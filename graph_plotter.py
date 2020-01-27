import pylab
import math
import operator
import matplotlib.pyplot as plt
import numpy as np
from sklearn.decomposition import PCA
from tsne_python.tsne import tsne

def scatterPlotEntireModel(modelPredict, tsneIter, perplexity, labels):
    '''
    Creates a scatter plot with the list of movies along with a legend (single-labels prioritising alphabetical order).
    Each movie is plotted separately, and is given a legend only if the specific plot for this label has been created.
    Movies with IDs not found in the MovieLens DataSet will be assigned a None label

    modelPredict: matrix containing predicted ratings for all user/item combinations. Shape is items x users.
    tsneIter: number of iterations to plot tSNE's visualisation.
    perplexity: setting for tSNE visualisation (see sources for more info).
    labels: array of colour values for each different genre (contains as many elements as there are items).
    '''

    # Predictions.shape = (1683,2)
    pca = PCA(n_components=10)
    modelPredict = pca.fit_transform(modelPredict)
    
    predictions = tsne(tsneIter,modelPredict, 2, 10, perplexity)
    # Predictions has 1683 rows but there are only 1682 items?!
    assignSingleLabels(predictions,labels)
    return False



def scatterPlotSingleUser(model, embedding_dim, idNoLabel, userIndex, numMovies, tsneIter, perplexity):
    '''
    Creates a visualisation of a single-user along with all the items of the dataset (using latent factors).
    This shows the items that are most similar and least similar to that user's tastes.

    model: the prediction model built by spotlight (from which we get the item and user latent factors).
    idNoLabel: Movies with no corresponding Id in the dataset
    userIndex: the user whose taste we wish the visualise.
    tsneIter: number of iterations to plot tSNE's visualisation.
    perplexity: setting for tSNE visualisation (see sources for more info).
    '''
    
    numMoviesWithLabel = numMovies-len(idNoLabel)
    allLatentFactors = np.empty((numMoviesWithLabel+1,embedding_dim))

    count = 0
    for i in range (numMovies):
        if i not in (idNoLabel):
            allLatentFactors[count,:] = model._net.item_embeddings.weight[i].detach()
            count += 1

    allLatentFactors[numMoviesWithLabel,:] = model._net.user_embeddings.weight[userIndex].detach()

    pca = PCA(n_components=10)
    allLatentFactors = pca.fit_transform(allLatentFactors)
    
    dimReduc = tsne(tsneIter,allLatentFactors, 2, 10, perplexity)
    
    plot1 = plt.scatter(dimReduc[:numMoviesWithLabel, 0], dimReduc[:numMoviesWithLabel, 1], 10 ,'black')
    plot2 = plt.scatter(dimReduc[numMoviesWithLabel, 0], dimReduc[numMoviesWithLabel, 1], 20 ,'red','*')


    plt.legend([plot1,plot2],['items','user '+str(userIndex)],bbox_to_anchor=(1.1, 1.05))
    return (dimReduc, plot1, True)


def scatterPlotAllUsers(model, embedding_dim, userIndex, numUsers, pointNum, tsneIter, perplexity, previousClosest=["0"]):
    '''
    Creates a visualisation of all users from the dataset.
    This is useful to find neighbour users to a specific user.

    model: the prediction model built by spotlight (from which we get the item and user latent factors).
    userIndex: the user for which we will plot the closest points.
    numUsers: number of total users in the model.
    pointNum: number of closest points (or users) we want to represent.
    tsneIter: number of iterations to plot tSNE's visualisation.
    perplexity: setting for tSNE visualisation (see sources for more info).
    '''
    
    allUserFactors = np.empty((numUsers,embedding_dim))

    for i in range (numUsers):
        allUserFactors[i,:] = model._net.user_embeddings.weight[i].detach()

    pca = PCA(n_components=10)
    allUserFactors = pca.fit_transform(allUserFactors)
    
    allUsersReduction = tsne(tsneIter,allUserFactors, 2, 10, perplexity)

    userX = allUsersReduction[userIndex,0]
    userY = allUsersReduction[userIndex,1]
    distances = []

    for index in range (numUsers):
        pointX = allUsersReduction[index,0]
        pointY = allUsersReduction[index,1]
        dist = math.sqrt((pointX-userX)**2+(pointY-userY)**2)

        
        distances += [dist]

    distIndexes = np.argsort(distances)
    #The first index will be the index of the chosen user (distance to itself is 0)
    distSmallestIndexes = distIndexes[1:pointNum+1]
    closestPoints = np.empty((pointNum,2))

    counter = 0
    for index in distSmallestIndexes:
        closestPoints[counter] = allUsersReduction[index,:]
        counter += 1
    
    plot1 = plt.scatter(allUsersReduction[:, 0], allUsersReduction[:, 1], 10 ,'black')
    plot2 = plt.scatter(closestPoints[:, 0], closestPoints[:, 1], 10 ,'lime')
    plot3 = plt.scatter(allUsersReduction[userIndex, 0], allUsersReduction[userIndex, 1], 20 ,'red','*')
    if "0" in previousClosest:
        plt.legend([plot1,plot2,plot3],['Other Users',
                                        'Closest '+str(pointNum)+' Users',
                                        'user '+str(userIndex)],bbox_to_anchor=(1.1, 1.05))
        
    else:
        previousClosestPoints = np.empty((pointNum,2))
        counter = 0
        for index in previousClosest:
            previousClosestPoints[counter]= allUsersReduction[index,:]
            counter += 1
            
        plot4 = plt.scatter(previousClosestPoints[:, 0], previousClosestPoints[:, 1], 10 ,'deeppink')
        plt.legend([plot1,plot2,plot3,plot4],['Other Users',
                                              'Current neighbours',
                                              'user '+str(userIndex),
                                              'Previous neighbours'],bbox_to_anchor=(1.1, 1.05))

        

    
    
    '''
    plot1 = plt.scatter(allUsersReduction[:, 0], allUsersReduction[:, 1], 10 ,'black')
    plot2 = plt.scatter(closestPoints[:, 0], closestPoints[:, 1], 10 ,'lime')


    plt.legend([plot1,plot2],['Other Users','Closest '+str(pointNum)+' Users'])
    '''
    print("The users most similar to user",userIndex,"are:",distSmallestIndexes)
    return (distSmallestIndexes, False)
    


def showClosestFarthestLabelPoints(tsnePlot, labels, labelsAsGenres, pointNum, numRec, farthest, verbose):
    '''
    Represents the points that are most similar to a given user.

    tsnePlot: output produced after calling the tsne function (an array containing 2D coordinates).
    pointNum: number of closest points we want to represent.
    numRec: number of displayed recommendations.
    labels: array of colour values for each different genre (contains as many elements as there are items).
    labelsAsGenres: array of genres (prioritised based on alphabetical order) corresponding to movies.
    farthest: if True, will also show the N farthest points from the user.
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

    
    #distIndexes = np.argpartition(distances, pointNum)
    distIndexes = np.argsort(distances)
    distSmallestIndexes = distIndexes[:pointNum]
    closestPoints = np.empty((pointNum,2))
    labelsClosestPoints = []
    
    #Finding the labels and point coordinates associated to the indexes
    if (verbose):
        labelsGenresClosestPoints = []
        labelsGenresFarthestPoints = []
    counter = 0
    for index in distSmallestIndexes:
        if (verbose):
            labelsGenresClosestPoints += [labelsAsGenres[index]]
        labelsClosestPoints += [labels[index]]
        closestPoints[counter] += tsnePlot[index,:]
        counter += 1

    if (farthest):
        distFarthestIndexes = distIndexes[-pointNum:]
        farthestPoints = np.empty((pointNum,2))
        labelsFarthestPoints = []
        counter = 0
        
        for index in distFarthestIndexes:
            if (verbose):
                labelsGenresFarthestPoints += [labelsAsGenres[index]]
                labelsFarthestPoints += [labels[index]]
                farthestPoints[counter] += tsnePlot[index,:]
                counter += 1

    

    if (verbose):
        closestLabelsOccurence = {}
        for label in labelsGenresClosestPoints:
            if label not in closestLabelsOccurence:
                closestLabelsOccurence[label] = 1
            else:
                closestLabelsOccurence[label] += 1
                
        closestLabelsSorted = sorted(closestLabelsOccurence.items(), key=operator.itemgetter(1))
        print("\nThe genres of the "+str(pointNum)+" closest points are:")
        i = len(closestLabelsSorted)-1
        while(i>=0):
            print(closestLabelsSorted[i][0]+": ",closestLabelsSorted[i][1])
            i -= 1

        if (farthest):
            farthestLabelsOccurence = {}
            for label in labelsGenresFarthestPoints:
                if label not in farthestLabelsOccurence:
                    farthestLabelsOccurence[label] = 1
                else:
                    farthestLabelsOccurence[label] += 1

            farthestLabelsSorted = sorted(farthestLabelsOccurence.items(), key=operator.itemgetter(1))
            print("\nThe genres of the "+str(pointNum)+" farthest points are:")
            i = len(farthestLabelsSorted)-1
            while(i>=0):
                print(farthestLabelsSorted[i][0]+": ",farthestLabelsSorted[i][1])
                i -= 1
            
    distSmallestIndexes = distSmallestIndexes[:numRec]
    assignSingleLabels(closestPoints, labelsClosestPoints)
    assignSingleLabels(farthestPoints, labelsFarthestPoints)
    return(distSmallestIndexes, labelsGenresClosestPoints,len(closestLabelsSorted))
    


def assignSingleLabels(tsneArray, labels):

    validPlots = []
    validLabels = []
    for i in range (len(labels)):
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
    
    plt.legend(validPlots,validLabels,loc="upper right")#bbox_to_anchor=(1.1, 1.05))
        






        
    
