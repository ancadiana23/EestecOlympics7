from sklearn.neural_network import MLPClassifier
import scipy 
import numpy as np
from PIL import Image
from numpy import *
#from pylab import *
import os

def train():
	X_train = []
	y_train = []

	X_test = []
	y_test = []

	for (parent, X, y) in [('training_set/', X_train, y_train), ('test_set/', X_test, y_test)]:
		for dir_nr in [1, 2, 3]:
			directory = parent + str(dir_nr) + "/"
			for file in os.listdir(directory):
				im = Image.open(directory + file)

				new_image = list(im.getdata())
				
				X.append(new_image)
				y.append(dir_nr)

	y_train_1 = list(map(lambda x: int(x/3), y_train))
	y_test_1 = list(map(lambda x: int(x/3), y_test))

	hand_detector = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=1)
	hand_detector.fit(X_train, y_train_1)

	'''output = [hand_detector.predict([X_test[i]])[0] for i in range(len(X_test))]
	print(output)
	error = len(output) - [output[i] - y_test_1[i] for i in range(len(output))].count(0)
	print(error)'''

	nr_hands_train = y_train.count(1) + y_train.count(2)
	nr_hands_test  = y_test.count(1) + y_test.count(2)

	'''print("!!!", nr_hands_train)
	print("!!!", nr_hands_test)'''

	click_detector = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=1)
	click_detector.fit(X_train[0:nr_hands_train], y_train[0:nr_hands_train])

	'''output = [click_detector.predict([X_test[i]])[0] for i in range(nr_hands_test)]
	print(output)
	error = len(output) - [output[i] - y_test[i] for i in range(nr_hands_test)].count(0)
	print(error)'''

	return hand_detector, click_detector

