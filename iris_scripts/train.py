import argparse
import os
import pandas as pd
import numpy as np

#from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn import svm
from sklearn.externals import joblib

from azureml.core import Run


# In case user wishes to feed parameters
parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
args = parser.parse_args()

data_folder = os.path.join(args.data_folder, 'iris')
print('Data folder:', data_folder)


train = pd.read_csv(os.path.join(data_folder, 'iris_train.csv'), sep = ",")
test = pd.read_csv(os.path.join(data_folder, 'iris_test.csv'), names=["Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width", "Class"], sep = ",")
X_train = train[["Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width"]]
y_train = train[["Class"]]
y_train = y_train.values
y_train = y_train.ravel()
X_test= test[["Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width"]]
y_test = test[["Class"]]
y_test = y_test.values
y_test = y_test.ravel()

print(X_train.shape, y_train.shape, X_test.shape, y_test.shape, sep = '\n')
print(train.shape, test.shape)

# get hold of the current run
run = Run.get_context()

print('Train a SVM model')
clf = svm.SVC()
clf.fit(X_train, y_train)

print('Predict the test set')
y_hat = clf.predict(X_test)

# calculate accuracy on the prediction
acc = np.average(y_hat == y_test)
print('Accuracy is', acc)

#run.log('regularization rate', np.float(args.reg))
run.log('accuracy', np.float(acc))

os.makedirs('outputs', exist_ok=True)
# note file saved in the outputs folder is automatically uploaded into experiment record
joblib.dump(value=clf, filename='outputs/sklearn_iris_model.pkl')