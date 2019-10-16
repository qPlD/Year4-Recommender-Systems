'''
Base code is from https://github.com/maciejkula/spotlight
'''
import numpy as np
import pylab
from spotlight.cross_validation import random_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel
from spotlight.interactions import Interactions
from tsne_python.tsne import tsne

#Datasets options: https://grouplens.org/datasets/movielens/
dataset = get_movielens_dataset(variant='100K')
print(dataset)

#Lists of all interactions where userIds[x], movieIds[x] and ratings[x] correspond
userIds = dataset.user_ids
movieIds = dataset.item_ids
#ratings = dataset.ratings

#Number of DIFFERENT users and movies per list (!= length of lists)
numUsers = dataset.num_users
numMovies = dataset.num_items

#print(userIds,numUsers,len(userIds)        944  100000
#print(movieIds,numMovies,len(movieIds))    1683 100000
#print(ratings,len(ratings))                     100000
#Split the dataset to evaluate the model
train, test = random_train_test_split(dataset)
print('Split into \n {} and \n {}.'.format(train, test))

# Works for 5 iterations but crashes tsne for 10
model = ExplicitFactorizationModel(n_iter=20)
model.fit(train, verbose=True)


# METHOD 2
'''
predictions = np.dot(userIds, movieIds)
print (predictions)
'''
# METHOD 3
#Proof to verify that predictions for any user are made for all items
'''
user196 = model.predict(196)
user186 = model.predict(186)
user22 = model.predict(22)
user13 = model.predict(13)

print(user196,len(user196))
print(user186,len(user186))
print(user22,len(user22))
print(user13,len(user13))
'''
predictions = np.empty((numUsers,numMovies))
for i in range (numUsers):
    predictions[i,:] = model.predict(i)

print("Shape of Prediction matrix:",predictions.shape)
#print(predictions[1])

#Measure the model's effectiveness (how good predictions are):
rmse = rmse_score(model, test)
train_rmse = rmse_score(model, train)
test_rmse = rmse_score(model, test)
print('Train RMSE {:.3f}, test RMSE {:.3f}'.format(train_rmse, test_rmse))

# We take the transpose for tsne formatting (should be more rows than columns)
Y = tsne(200,predictions.T, 2, 4, 20.0)

pylab.scatter(Y[:, 0], Y[:, 1], 20)
pylab.show()


