'''
Base code is from https://github.com/maciejkula/spotlight
'''
from spotlight.cross_validation import random_train_test_split
from spotlight.datasets.movielens import get_movielens_dataset
from spotlight.evaluation import rmse_score
from spotlight.factorization.explicit import ExplicitFactorizationModel

#Datasets options: https://grouplens.org/datasets/movielens/
dataset = get_movielens_dataset(variant='100K')
print(dataset)

#Split the dataset to evaluate the model
train, test = random_train_test_split(dataset)
print('Split into \n {} and \n {}.'.format(train, test))


model = ExplicitFactorizationModel(n_iter=5)
model.fit(train, verbose=True)

#Measure the model's effectiveness (how good predictions are):
rmse = rmse_score(model, test)
train_rmse = rmse_score(model, train)
test_rmse = rmse_score(model, test)
print('RMSE {:.3f}, Train RMSE {:.3f}, test RMSE {:.3f}'.format(rmse,train_rmse, test_rmse))
