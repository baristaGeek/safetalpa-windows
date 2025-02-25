# Train model and make predictions
import numpy
from numpy import argmax
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)

# load dataset
dataframe = pandas.read_csv("modifiedBinaryRandomizedProcesses.csv", keep_default_na=False, header=None)
print ("df before procesing: ")
print (dataframe)

# Process Name
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[1])],axis=1).drop([1],axis=1)

# Process ID
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[2], prefix='PID')],axis=1).drop([2],axis=1)
# TODO: Have a statistical argument for dropping or not this column

# Session Name
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[3])],axis=1).drop([3],axis=1)

# Memmory Usage
df_min_4 = dataframe[4].min()
df_max_4 = dataframe[4].max()

# Status
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[5], prefix='status')],axis=1).drop([5],axis=1)

# Username
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[6], prefix='state')],axis=1).drop([6],axis=1)

# CPU Time
df_min_7 = dataframe[7].min()
df_max_7 = dataframe[7].max()

# Window T
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[8], prefix='window_T')],axis=1).drop([8],axis=1)

# normalize dataset 
dataframe[4] = dataframe[4].apply(lambda x: ((x - df_min_4) / (df_max_4 - df_min_4)))
dataframe[7] = dataframe[7].apply(lambda x: ((x - df_min_7) / (df_max_7 - df_min_7)))

# print("dataframe before loop:")
# print(dataframe)

# Change each column name for its index
for column in dataframe:
	dataframe.rename(columns={column: dataframe.columns.get_loc(column)}, inplace=True)
#	print (column)
#	print("dataframe after loop:")
#	print(dataframe)

# Make input size variable because one-hot encoding generates a dataset with a variable amount of dimensions
input_size = (len(dataframe.columns) - 1)

dataset = dataframe.values
X = dataset[:,0:input_size].astype(float)
Y = dataset[:,0]

# print("X and Y: ")
# print(X)
# print(Y)		

# This was done in the multiclass-classiffication example. However, we can probably just say '0' is malign and '1' is benign
# encode benign and malign as integers
# encoder = LabelEncoder()
# encoder.fit(Y)
# encoded_Y = encoder.transform(Y)

# convert integers to dummy variables (i.e. one hot encoded)
# dummy_y = np_utils.to_categorical(encoded_Y)


# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=input_size, activation='relu')) #input_dim must be variable due to one-hot encoding
	model.add(Dense(2, activation='softmax')) # 2 because it's either malign or benign
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)

kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
# dummy_y was used when we were one-hot encoding our output variable
# results = cross_val_score(estimator, X, dummy_y, cv=kfold)
results = cross_val_score(estimator, X, Y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))