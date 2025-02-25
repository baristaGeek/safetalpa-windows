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
dataframe = pandas.read_csv("randomizedSet.csv", header=None)
dataset = dataframe.values
X = dataset[:,2:11].astype(float) # excluding the process name and ID features
Y = dataset[:,11]

print("dataframe.head(): ")
print(dataframe.head())

# Process name and ID are dataframe indexes 0 and 1 respectively

# Session name
# session_encoder = LabelEncoder()
# integer_encoded_sessions = session_encoder.fit_transform(dataframe[2])
# print("dataframe[2]: ")
# print(dataframe[2])
# print("integer_encoded_sessions:")
# print(integer_encoded_sessions)
# session_onehot_encoder = OneHotEncoder(sparse=False)
# integer_encoded_sessions = integer_encoded_sessions.reshape(len(integer_encoded_sessions), 1)
# onehot_encoded_sessions = session_onehot_encoder.fit_transform(integer_encoded_sessions)
# print("onehot_encoded_sessions:")
# print(onehot_encoded_sessions)
# inverted = session_encoder.inverse_transform([argmax(onehot_encoded_sessions[0, :])])
# print("inverted: (should print 'Services')")
# print(inverted)

# print(pandas.get_dummies(dataframe[2],prefix='session'))

dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[2], prefix='session')],axis=1).drop([2],axis=1)
print("new df:")
print(dataframe.head())
print("df[sessin console")
print(dataframe['session_Console'])

# Memmory Usage
df_min_3 = dataframe[3].min()
df_max_3 = dataframe[3].max()

# Status
# status_encoder = LabelEncoder()
# integer_encoded_status = status_encoder.fit_transform(dataframe[4])
# status_onehot_encoder = OneHotEncoder(sparse=False)
# integer_encoded_status = integer_encoded_status.reshape(len(integer_encoded_status), 1)
# onehot_encoded_status = status_onehot_encoder.fit_transform(integer_encoded_status)
# inverted = status_encoder.inverse_transform([argmax(onehot_encoded_status[0, :])])
# print ("inverted status:")
# print(inverted)
# print ("dataframe[4]:")
# print(dataframe[4])
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[4], prefix='status')],axis=1).drop([4],axis=1)
print("new df:")
print(dataframe.head())
print("df[status unknown]")
print(dataframe['status_Unknown'])

# Username
# username_encoder = LabelEncoder()
# integer_encoded_username = username_encoder.fit_transform(dataframe[5])
# username_onehot_encoder = OneHotEncoder(sparse=False)
# integer_encoded_username = integer_encoded_username.reshape(len(integer_encoded_username), 1)
# onehot_encoded_username = username_onehot_encoder.fit_transform(integer_encoded_username)
# inverted = username_encoder.inverse_transform([argmax(onehot_encoded_username[0, :])])
# print ("inverted username:")
# print(inverted)
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[5], prefix='username', dummy_na=True)],axis=1).drop([5],axis=1)
# for some reason N/A is being treated as nan in this column, so dummy_na=True had to be added
print("new df:")
print(dataframe.head())
print("df[username Esteban]")
print(dataframe['username_Esteban'])

# CPU Time - TODO: Convert to a quantity
df_min_6 = dataframe[6].min()
df_max_6 = dataframe[6].max()

# Window T
# windowT_encoder = LabelEncoder()
# integer_encoded_windowT = windowT_encoder.fit_transform(dataframe[7])
# windowT_onehot_encoder = OneHotEncoder(sparse=False)
# integer_encoded_windowT = integer_encoded_windowT.reshape(len(integer_encoded_windowT), 1)
# onehot_encoded_windowT = windowT_onehot_encoder.fit_transform(integer_encoded_windowT)
# inverted = windowT_encoder.inverse_transform([argmax(onehot_encoded_windowT[0, :])])
# print ("inverted Window T:")
# print(inverted)
dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[7], prefix='windowT')],axis=1).drop([7],axis=1)
print("new df:")
print(dataframe.head())
print("df[window T]")
print(dataframe['windowT_N/A'])

# normalize dataset 
dataframe[3] = dataframe[3].apply(lambda x: ((x - df_min_3) / (df_max_3 - df_min_3)))
dataframe[6] = dataframe[6].apply(lambda x: ((x - df_min_6) / (df_max_6 - df_min_6)))

# encode benign and malign as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)

# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)


# define baseline model
def baseline_model():
	# create model
	model = Sequential()
	model.add(Dense(8, input_dim=12, activation='relu')) #input_dim must me variable due to one-hot encoding
	model.add(Dense(3, activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)

kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
results = cross_val_score(estimator, X, dummy_y, cv=kfold)
print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))