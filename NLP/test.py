import numpy as np
from sklearn import linear_model
import random

matrix = np.loadtxt('tfidf-spacy.csv', delimiter=",",skiprows=1,usecols = (2,), dtype= float)
random.shuffle(matrix)
value =  np.array([matrix[:,1]])
value = value.T
print value.ravel()
matrix = np.array(matrix[:,2:])
# matrix = np.concatenate((matrix,value.T),axis =1)

# print matrix.shape
# print value.shape

training_set = matrix[:200,:]
result_set = value[:200,:]
predict_set = matrix[201:,:]

# print training_set.shape
# print result_set.shape
#print lrClassifier
lrClassifier = linear_model.LogisticRegression()
#lrClassifier = linear_model.LogisticRegression(penalty='l2', multi_class='ovr', tol=0.001, C=1.0)
lrClassifier.fit(training_set,result_set.ravel())
prediction = lrClassifier.predict(predict_set)
print prediction.shape
expected =  value[201:].ravel()
print expected.shape
print prediction == expected
print (sum(prediction == expected))/78
# print prediction == value[201:]
# print prediction[206:210]
# print value[206:210]
#
# print prediction