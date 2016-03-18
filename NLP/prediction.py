import numpy as np
from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
import random
import sys,json,pprint

matrix = np.loadtxt('tfidf-nltk.csv', delimiter=",",skiprows=1,dtype= float)
with open('file_look_up.json') as data_file:    
    look_up = json.load(data_file)
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
expectation_set =[]
unselected = []
while len(selected)< 250:
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
        unselected.append(num)
        prediction_set.append(data[num])
        expectation_set.append(value[num])
prediction_set = np.array(prediction_set)
expectation_set = np.array(expectation_set)

# print prediction_set
# print expectation_set

#default classifier
classifier = linear_model.LogisticRegression()

if sys.argv[1] == 'lr':
    classifier = linear_model.LogisticRegression()

elif sys.argv[1] == 'nb':
    classifier = GaussianNB()

elif sys.argv[1] == 'dt':
    classifier = tree.DecisionTreeClassifier()
# # #print lrClassifier

# # lrClassifier = linear_model.LogisticRegression(penalty='l2', multi_class='ovr', tol=0.001, C=1.0)
classifier.fit(training_set,result_set)
prediction = classifier.predict(prediction_set)
# ans = (prediction == expectation_set)
# print sum(ans)
# print ans
tp = 0
fp = 0
tn = 0
fn = 0
fn_file = []
fp_file = []
for i in range(len(prediction)):
    if prediction[i]==1 and expectation_set[i]==1:
        tp +=1
    elif prediction[i]==0 and expectation_set[i]==1:
        fn += 1
        fn_file.append(look_up[str(unselected[i])]["type"]+":"+look_up[str(unselected[i])]["name"])
    elif prediction[i]==0 and expectation_set[i]==0:
        tn +=1
    elif prediction[i]==1 and expectation_set[i]==0:
        fp +=1
        fp_file.append(look_up[str(unselected[i])]["type"]+":"+look_up[str(unselected[i])]["name"])
print "precison=",float(tp)/float(tp+fp), " tp=",tp, " fp=",fp
print "recall=",float(tp)/float(tp+fn), " fn=",fn
print "False Positive Files are: "
for art in fp_file:
    print art
print "False Negative Files are: "
for art in fn_file:
    print art
