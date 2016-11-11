from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import numpy as np
import pandas

print('!@!')
# Data sets
IRIS_TRAINING = "iris_training.csv"
IRIS_TEST = "iris_test.csv"

# Load datasets.
train = pandas.read_csv(IRIS_TRAINING, header=None)
print(train)

X_train, y_train = train[2], train[0]

test = pandas.read_csv(IRIS_TEST, header=None)
X_test, y_test = test[2], test[0]

y_train = [round(x) for x in y_train]
print(X_train)
X_train = [round(x) for x in X_train]

#training_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TRAINING,
#                                                       target_dtype=np.int)
#test_set = tf.contrib.learn.datasets.base.load_csv(filename=IRIS_TEST,
#                                                   target_dtype=np.int)
# Specify that all features have real-value data
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=4)]

# Build 3 layer DNN with 10, 20, 10 units respectively.
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=3,
                                            model_dir="/tmp/iris_model")

# Fit model.
classifier.fit(x=X_train,
               y=y_train,
               steps=2000)

# Evaluate accuracy.
accuracy_score = classifier.evaluate(x=X_test,
                                     y=y_test)["accuracy"]
print('Accuracy: {0:f}'.format(accuracy_score))

# Classify two new flower samples.
new_samples = np.array(
    [[6.4, 3.2, 4.5, 1.5], [5.8, 3.1, 5.0, 1.7]], dtype=float)
y = classifier.predict(new_samples)
print('Predictions: {}'.format(str(y)))