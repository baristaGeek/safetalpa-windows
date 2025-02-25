# Train model and make predictions
import numpy
from numpy import argmax
import pandas
import os
import shutil
import sys
import importlib
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
def job():
	current_directory = os.getcwd() + "\\data-analysis\\data_colection"
	def find_first_directory():
		for direct in os.listdir(current_directory):
			if not (str(direct)) == 'Analyzing':
				return str(direct)
	oldes_direc = find_first_directory()
	os.rename(os.path.join(current_directory, oldes_direc),
			os.path.join(current_directory, "Analyzing"))
	# fix random seed for reproducibility
	seed = 7
	numpy.random.seed(seed)

	# load dataset
	# plain_dataframe is used to later save the plain malign data entries
	plain_dataframe = pandas.read_csv(
		current_directory + "\\Analyzing\\conectionPorts.csv",header=None)
	# dataframe and test_dataframe are the ones used for fitting and classiffication
	dataframe = pandas.read_csv(
		os.getcwd() + "\\data-analysis\\training_sets\\training_connections.csv", header=None)
	test_dataframe = pandas.read_csv(
		current_directory + "\\Analyzing\\conectionPorts.csv", header=None)

	# Protocol
	dataframe = pandas.concat(
		[dataframe, pandas.get_dummies(dataframe[0])], axis=1).drop([0], axis=1)
	test_dataframe = pandas.concat([test_dataframe, pandas.get_dummies(
		test_dataframe[0])], axis=1).drop([0], axis=1)

	# Local Address
	dataframe = dataframe.drop([1], axis=1)
	test_dataframe = test_dataframe.drop([1], axis=1)
	# dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[1], prefix='local_address')],axis=1).drop([1],axis=1)
	# test_dataframe = pandas.concat([test_dataframe,pandas.get_dummies(test_dataframe[1], prefix='local_address')],axis=1).drop([1],axis=1)

	# Foreign address
	dataframe = dataframe.drop([2], axis=1)
	test_dataframe = test_dataframe.drop([2], axis=1)
	# dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[2], prefix='foreign_address')],axis=1).drop([2],axis=1)
	# test_dataframe = pandas.concat([test_dataframe,pandas.get_dummies(test_dataframe[2], prefix='foreign_address')],axis=1).drop([2],axis=1)

	# State
	dataframe = pandas.concat([dataframe, pandas.get_dummies(
		dataframe[3], prefix='state')], axis=1).drop([3], axis=1)
	test_dataframe = pandas.concat([test_dataframe, pandas.get_dummies(
		test_dataframe[3], prefix='state')], axis=1).drop([3], axis=1)

	# PID
	dataframe = dataframe.drop([4], axis=1)
	test_dataframe = test_dataframe.drop([4], axis=1)
	# dataframe = pandas.concat([dataframe,pandas.get_dummies(dataframe[4], prefix='PID')],axis=1).drop([4],axis=1)
	# test_dataframe = pandas.concat([test_dataframe,pandas.get_dummies(test_dataframe[4], prefix='PID')],axis=1).drop([4],axis=1)
	# TODO: Have a statistical argument for dropping or not this column


	# Offload state
	dataframe = pandas.concat([dataframe, pandas.get_dummies(
		dataframe[5], prefix='offload_state')], axis=1).drop([5], axis=1)
	test_dataframe = pandas.concat([test_dataframe, pandas.get_dummies(
		test_dataframe[5], prefix='offload_state')], axis=1).drop([5], axis=1)

	# Change each column name for its index
	for column in dataframe:
		dataframe.rename(
			columns={column: dataframe.columns.get_loc(column)}, inplace=True)
			# print (column)

	for column in test_dataframe:
		test_dataframe.rename(
			columns={column: test_dataframe.columns.get_loc(column)}, inplace=True)

	# Make input size variable because one-hot encoding generates a dataset with a variable amount of dimensions
	training_input_size = (len(dataframe.columns) - 1)
	print("training input size:")
	print(training_input_size)
	test_input_size = (len(test_dataframe.columns) - 1)

	training_dataset = dataframe.values
	training_X = training_dataset[:, 1:training_input_size].astype(
		float)  # changed :,0 to :,1
	training_Y = training_dataset[:, 0]

	test_dataset = test_dataframe.values
	test_X = test_dataset[:, 1:test_input_size].astype(float)
	test_Y = test_dataset[:, 0]

	model = Sequential()
	# input_dim must be variable due to one-hot encoding
	model.add(Dense(8, input_dim=(training_input_size-1), activation='relu'))
	# 1 because it's either malign or benign, so we can use binary_crossentropy
	model.add(Dense(1, activation='softmax'))
	# Compile model
	model.compile(loss='binary_crossentropy',
				optimizer='adam', metrics=['accuracy'])
	model.fit(training_X, training_Y, epochs=4)

	print("training_dataset")
	print(training_dataset)
	print("test_dataset")
	print(test_dataset)

	# TODO Juan: Make changes to capturing scripts in order to not have dimensionality problem
	print("test_X")
	print(test_X)
	print("test_Y")
	print(test_Y)
	val_loss, val_acc = model.evaluate(test_X, test_Y)
	# val_loss, val_acc = model.evaluate(test_X, test_Y)
	print("metrics:")
	print(val_loss)
	print(val_acc)  # current accuracy is 27.5% because we need a bigger a training set

	# TODO Esteban: Classiffy packets are malign (0) or benign (1), not just benign (1)
	current_directory = os.getcwd()
	folder_name = 'data-analysis\\Malware detected'
	final_directory = os.path.join(current_directory, folder_name)
	for idx, prediction in enumerate(model.predict(test_X)):
		if (prediction == 0):
			process_running_file = open(
				final_directory + "\\malwareConections.csv", "a+")
			process_running_file.write(str(plain_dataframe.iloc[[idx]]))
			process_running_file.close()


	def deleteDirectory():
		directory_to_erase = None
		for direct in os.listdir(current_directory + "\\data-analysis\\data_colection"):
			if (str(direct)) == 'Analyzing':
				directory_to_erase = direct
				break
		if not directory_to_erase == None:
			shutil.rmtree(os.path.join(current_directory+ "\\data-analysis\\data_colection", directory_to_erase))

	deleteDirectory()
	#TODO Esteban: model.save(connection_ports.model)
	print("execution done")
