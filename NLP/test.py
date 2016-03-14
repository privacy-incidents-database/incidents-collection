import numpy as np
from sklearn import linear_model
import random

matrix = np.loadtxt('tfidf-spacy.csv', delimiter=",",skiprows=1,dtype= float)

# # matrix = np.concatenate((matrix,value.T),axis =1)
data = matrix[:,2:]
value = matrix[:,1]
# Selection of data
selected = []

#Training set 

training_set = []
result_set = [] 

#Prediction Set
prediction_set = []
expection_set =[] 
while len(selected)< 50:
    num =  int(random.random()*data.shape[0])
    if num not in selected:
        training_set.append(data[num])
        result_set.append(value[num])
        selected.append(num)
    # print num
training_set = np.array(training_set)
result_set = np.array(result_set)
print training_set.shape
print result_set.shape
for num in range(data.shape[0]):
    if num not in selected:
        prediction_set.append(data[num])
        expection_set.append(value[num])
prediction_set = np.array(prediction_set)
expection_set = np.array(expection_set)

# # #print lrClassifier
lrClassifier = linear_model.LogisticRegression()
# # lrClassifier = linear_model.LogisticRegression(penalty='l2', multi_class='ovr', tol=0.001, C=1.0)
lrClassifier.fit(training_set,result_set)
prediction = lrClassifier.predict(prediction_set)
ans = (prediction == expection_set)
# print sum(ans)
# print ans
tp = 0
fp = 0
tn = 0
fn = 0
for i in range(len(prediction)):
    if prediction[i]==1 and expection_set[i]==1:
        tp +=1
    elif prediction[i]==0 and expection_set[i]==1:
        fn += 1
    elif prediction[i]==0 and expection_set[i]==0:
        tn +=1
    elif prediction[i]==1 and expection_set[i]==0:
        fp +=1
print "precison=",float(tp)/float(tp+fp), " tp=",tp, " fp=",fp
print "recall=",float(tp)/float(tp+fn), " fn=",fn
