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
from graph_plotter import showClosestFarthestPoints

'''
PROGRAM PARAMETERS FOR TESTING
'''
perplexity = 50
modelIterations = 300
tsneIterations = 2000
'''
END OF TESTING PARAMETERS
'''
#Datasets options: https://grouplens.org/datasets/movielens/
dataset = get_movielens_dataset(variant='100K')

userIds = dataset.user_ids
movieIds = dataset.item_ids # range from 1 to 1682

#Number of DIFFERENT users and movies per list (!= length of lists)
numUsers = dataset.num_users

# Since IDs range from 1 to 1682, number of Movies should be 1682, not 1683.
numMovies = dataset.num_items
#Array used to get the label for each movieId
#We need to add 0 as it is not included in the IDs.
uniqueMovieIds = [0]
for currentId in movieIds:
    if currentId not in uniqueMovieIds:
        uniqueMovieIds += [currentId]

#print(np.amax(dataset.item_ids),np.amin(dataset.item_ids),numMovies)
#print(np.amax(dataset.num_users),np.amin(dataset.num_users),numUsers)
        
#print(numUsers,len(userIds)        944  100000
#print(numMovies,len(movieIds))    1683 100000
#print(ratings,len(ratings))                     100000
#Split the dataset to evaluate the model
train, test = random_train_test_split(dataset)
print('Split into \n {} and \n {}.'.format(train, test))

model = ExplicitFactorizationModel(n_iter=modelIterations)
model.fit(train, verbose=True)

#predictions for any user are made for all items, matrix has shape (944, 1683)
modelPredict = np.empty((numUsers,numMovies))
for i in range (numUsers):
    modelPredict[i,:] = model.predict(i)

# We take the transpose for tsne formatting (should be more rows than columns)
modelPredict = modelPredict.T

#TEST TO CHECK IF PREDICTIONS PRESERVES ORDER
# Predictions had 1683 rows accessed by indexes 0 to 1682
#print(model.predict(10)[0])
#print(predictions[0,10])


'''
predict = 0
for i in range (32):
    predict = predict + model._net.user_embeddings.weight[78][i]*model._net.item_embeddings.weight[1602][i]
'''


#dottest = np.dot(user0_LF.T,item0_LF)
#print(dottest, dottest.shape)
#Find way to add categories for items (use as labels).

#Project user into graph: user latent factor (dot product) item latent factor


#Measure the model's effectiveness (how good predictions are):
rmse = rmse_score(model, test)
train_rmse = rmse_score(model, train)
test_rmse = rmse_score(model, test)
print('Train RMSE {:.3f}, test RMSE {:.3f}'.format(train_rmse, test_rmse))



file = "ml-latest-small/movielens_movies.txt"
#assignSingleLabel(movieIdArray, file, showNone, showMultiple)
labelsAsColours, arrayOfIds, labelsAsGenres, idNoLabel = assignSingleLabel(uniqueMovieIds,file , False, False)
print("length ",len(arrayOfIds))
#print(len(Y),len(predictions),len(labels),len(uniqueMovieIds))
fig,ax = plt.subplots()



'''
#scatterPlotEntireModel(modelPredict, tsneIter, perplexity, labels)
annotationsNeeded = scatterPlotEntireModel(modelPredict,tsneIterations,perplexity,labelsAsColours)

'''
#scatterPlotSingleUser(model, userIndex, numMovies, tsneIter, perplexity)
tsnePlot ,plot1, annotationsNeeded = scatterPlotSingleUser(model, idNoLabel, 1, numMovies, tsneIterations, perplexity)

#showClosestFarthestPoints(tsnePlot, labels, labelsAsGenres, pointNum, farthest, verbose)
showClosestFarthestPoints(tsnePlot, labelsAsColours,labelsAsGenres, 50, True, True)








annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annot.set_visible(False)

#Making the plot interactive with event handlers displaying annotations
def update_annot(ind):

    pos = plot1.get_offsets()[ind["ind"][0]]
    annot.xy = pos
    text = "{}, {}".format(" ".join([arrayOfIds[n] for n in ind["ind"]]),
                           " ".join([labelsAsGenres[n] for n in ind["ind"]]))
    annot.set_text(text)
    #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
    annot.get_bbox_patch().set_alpha(0.4)

def hover(event):
    vis = annot.get_visible()
    if event.inaxes == ax:
        cont, ind = plot1.contains(event)
        if cont:
            update_annot(ind)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if vis:
                annot.set_visible(False)
                fig.canvas.draw_idle()
                
if(annotationsNeeded):
    fig.canvas.mpl_connect("motion_notify_event", hover)
plt.show()




