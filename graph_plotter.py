import pylab
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
    
    validPlots = []
    validLabels = []
    for i in range (len(predictions)):
        if (labels[i]=='cornflowerblue'):
            plot1 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'cornflowerblue')
            if 'Action' not in validLabels:
                validLabels += ['Action']
                validPlots += [plot1]
            #plt.legend(plot1,'Action')
        elif (labels[i]=='darkgrey'):
            plot2 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'darkgrey')
            if 'Adventure' not in validLabels:
                validLabels += ['Adventure']
                validPlots += [plot2]
            #plt.legend(plot2,'Adventure')
        elif (labels[i]=='lightcoral'):
            plot3 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'lightcoral')
            if 'Animation' not in validLabels:
                validLabels += ['Animation']
                validPlots += [plot3]
            #plt.legend(plot3,'Animation')
        elif (labels[i]=='red'):
            plot4 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'red')
            if 'Children' not in validLabels:
                validLabels += ['Children']
                validPlots += [plot4]
            #plt.legend(plot4,'Children')
        elif (labels[i]=='orangered'):
            plot5 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'orangered')
            if 'Comedy' not in validLabels:
                validLabels += ['Comedy']
                validPlots += [plot5]
            #plt.legend(plot5,'Comedy')
        elif (labels[i]=='saddlebrown'):
            plot6 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'saddlebrown')
            if 'Crime' not in validLabels:
                validLabels += ['Crime']
                validPlots += [plot6]
            #plt.legend(plot6,'Crime')
        elif (labels[i]=='orange'):
            plot7 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'orange')
            if 'Documentary' not in validLabels:
                validLabels += ['Documentary']
                validPlots += [plot7]
            #plt.legend(plot7,'Documentary')
        elif (labels[i]=='darkgoldenrod'):
            plot8 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'darkgoldenrod')
            if 'Drama' not in validLabels:
                validLabels += ['Drama']
                validPlots += [plot8]
            #plt.legend(plot8,'Drama')
        elif (labels[i]=='gold'):
            plot9 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'gold')
            if 'Fantasy' not in validLabels:
                validLabels += ['Fantasy']
                validPlots += [plot9]
            #plt.legend(plot9,'Fantasy')
        elif (labels[i]=='darkkhaki'):
            plot10 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'darkkhaki')
            if 'Film-Noir' not in validLabels:
                validLabels += ['Film-Noir']
                validPlots += [plot10]
            #plt.legend(plot10,'Film-Noir')
        elif (labels[i]=='yellow'):
            plot11 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'yellow')
            if 'Horror' not in validLabels:
                validLabels += ['Horror']
                validPlots += [plot11]
            #plt.legend(plot11,'Horror')
        elif (labels[i]=='yellowgreen'):
            plot12 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'yellowgreen')
            if 'Musical' not in validLabels:
                validLabels += ['Musical']
                validPlots += [plot12]
            #plt.legend(plot12,'Musical')
        elif (labels[i]=='lawngreen'):
            plot13 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'lawngreen')
            if 'Mystery' not in validLabels:
                validLabels += ['Mystery']
                validPlots += [plot13]
            #plt.legend(plot13,'Mystery')
        elif (labels[i]=='aqua'):
            plot14 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'aqua')
            if 'Romance' not in validLabels:
                validLabels += ['Romance']
                validPlots += [plot14]
            #plt.legend(plot14,'Romance')
        elif (labels[i]=='darkblue'):
            plot15 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'darkblue')
            if 'Sci-Fi' not in validLabels:
                validLabels += ['Sci-Fi']
                validPlots += [plot15]
            #plt.legend(plot15,'Sci-Fi')
        elif (labels[i]=='indigo'):
            plot16 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'indigo')
            if 'Thriller' not in validLabels:
                validLabels += ['Thriller']
                validPlots += [plot16]
            #plt.legend(plot16,'Thriller')
        elif (labels[i]=='violet'):
            plot17 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'violet')
            if 'War' not in validLabels:
                validLabels += ['War']
                validPlots += [plot17]
            #plt.legend(plot17,'War')
        elif (labels[i]=='deeppink'):
            plot18 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'deeppink')
            if 'Western' not in validLabels:
                validLabels += ['Western']
                validPlots += [plot18]
            #plt.legend(plot18,'Western')
        elif (labels[i]=='black'):
            plot19 = plt.scatter(predictions[i, 0], predictions[i, 1], 10 ,'black')
            if 'None' not in validLabels:
                validLabels += ['None']
                validPlots += [plot19]
            #plt.legend(plot19,'None')

    '''
    plt.legend([plot1,plot2,plot3,plot4,plot5,plot6,plot7,
                plot8,plot9,plot10,plot11,plot12,plot13,
                plot14,plot15,plot16,plot17,plot18,plot19],
               ('Action','Adventure','Animation','Children','Comedy','Crime','Documentary',
                'Drama','Fantasy','Film-Noir','Horror','Musical','Mystery',
                'Romance','Sci-Fi','Thriller','War','Western','None'))
    '''
    
    plt.legend(validPlots,validLabels,bbox_to_anchor=(1.1, 1.05))
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
    plot2 = plt.scatter(dimReduc[numMovies, 0], dimReduc[numMovies, 1], 10 ,'red')


    plt.legend([plot1,plot2],['items','user '+str(userIndex)],bbox_to_anchor=(1.1, 1.05))
    return (plot1, True)






        
    
