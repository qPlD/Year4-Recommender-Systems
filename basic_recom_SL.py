'''
Base code is from https://github.com/maciejkula/spotlight
'''
import numpy as np
from spotlight.cross_validation import random_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel
from spotlight.interactions import Interactions
from csv_to_txt import assignSingleLabel
from graph_plotter import scatterPlotWithLegends
from tsne_python.tsne import tsne    

#Datasets options: https://grouplens.org/datasets/movielens/
dataset = get_movielens_dataset(variant='100K')

#Lists of all interactions where userIds[x], movieIds[x] and ratings[x] correspond
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

# Works for 5 iterations but crashes tsne for 10
model = ExplicitFactorizationModel(n_iter=500)
model.fit(train, verbose=True)



#predictions for any user are made for all items, matrix has shape (944, 1683)

predictions = np.empty((numUsers,numMovies))
for i in range (numUsers):
    predictions[i,:] = model.predict(i)

# We take the transpose for tsne formatting (should be more rows than columns)
predictions = predictions.T

#TEST TO CHECK IF PREDICTIONS PRESERVES ORDER
# Predictions had 1683 rows accessed by indexes 0 to 1682
#print(model.predict(10)[0])
#print(predictions[0,10])


'''
predict = 0
for i in range (32):
    predict = predict + model._net.user_embeddings.weight[78][i]*model._net.item_embeddings.weight[1602][i]
'''


# Each latent factor vector has 32 entries, type is torch tensor.
user0_LF = model._net.user_embeddings.weight[0]
item0_LF = model._net.item_embeddings.weight[0]

#dottest = np.dot(user0_LF.T,item0_LF)
#print(dottest, dottest.shape)
#Find way to add categories for items (use as labels).

#Project user into graph: user latent factor (dot product) item latent factor


#Measure the model's effectiveness (how good predictions are):
rmse = rmse_score(model, test)
train_rmse = rmse_score(model, train)
test_rmse = rmse_score(model, test)
print('Train RMSE {:.3f}, test RMSE {:.3f}'.format(train_rmse, test_rmse))


# Y is a numpy array with shape (1683,2)
Y = tsne(1500,predictions, 2, 4, 5.0)
# Predictions has 1683 rows but there are only 1682 items?!

'''
pylab.plot(x='Items',
           y='Users',
           data=Y,
           fit_reg=False,
           legend=True,
           size=9,
           hue='Label')
pylab.title('Overall result for user/item ratings',weight='bold').set_fontsize('16')

'''
possibleGenres = ['Action','Adventure','Animation','Children','Comedy','Crime',
                  'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
                  'Mystery','Romance','Sci-Fi','Thriller','War','Western']
#pylab.scatter(Y[:, 0], Y[:, 1], 10 ,'red','o')

labels = assignSingleLabel(uniqueMovieIds,"ml-latest-small/movielens_movies.txt")
#print(len(Y),len(predictions),len(labels),len(uniqueMovieIds))
scatterPlotWithLegends(Y,labels)
'''
plot1 = plt.scatter(Y[:, 0], Y[:, 1], 10 ,labels)

pylab.legend(('cornflowerblue','darkgrey','lightcoral','red','orangered','saddlebrown','orange',
              'darkgoldenrod','gold','darkkhaki','yellow','yellowgreen','lawngreen',
              'aqua','darkblue','indigo','violet','deeppink','black'),
             ('Action','Adventure','Animation','Children','Comedy','Crime',
             'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
             'Mystery','Romance','Sci-Fi','Thriller','War','Western'))

#plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), scatterpoints=1)
#plt.legend(plot,possibleGenres)
plt.legend((plot1,),('Action','Adventure','Animation','Children','Comedy','Crime',
             'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
             'Mystery','Romance','Sci-Fi','Thriller','War','Western'))

plt.show()
'''

