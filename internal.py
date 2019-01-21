# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 10:53:25 2018

@author: mayank.khandelwal
"""
import os
from azure.storage.blob import BlockBlobService, PublicAccess

from blob import *
from database import *
from workspace import *

'''    
Create an Azure Database
'''
create_azure_dbserver_database(username_dbserver = 'username_dbserver',
                               password_dbserver = 'password_dbserver',
                               name_dbserver = 'name_dbserver',
                               resource_group_name = 'resource_group_name',
                               dbname = 'database-dbname',
                               startip = 'x.x.x.x',
                               endip = 'x.x.x.x'
                               )

'''
Create a Storage Account
'''
create_storage_account(storagename = 'storagename', resource_group_name = 'resource_group_name')

'''
Save SAS Token For Storage Account
'''
save_storage_sas("?sv=xxx")

'''
Create Containers Inside Storage
'''
create_container_storage(container_name = 'testcontainersas')


'''
Upload a File To Blob
'''
local_file_name="internal.py"
full_path_to_file = os.path.join(os.getcwd(), local_file_name)
        
upload_file_blob(container_name = "testcontainersas",
                file_name_on_blob = "test/"+local_file_name,
                full_path_to_file=full_path_to_file,
                )

'''    
Get a List of Files Inside Blob
'''
list_files_blob(container_name = "testcontainersas", config_name='default')




'''
Download All Files in Directory Structure
'''         
download_all_files_blob(container_name = "testcontainersas")   

'''
Create SQL Table Using Pandas Dataframe
'''
table_creation = {'Column_Name': ['PersonID', 'LastName', 'FirstName', 'Address', 'City'],
                  'DataType': ['int', 'varchar', 'varchar', 'varchar', 'varchar'],
                  'Size': ['',255,255,255,255]
                  }
table_df = pd.DataFrame(data=table_creation)

create_sql_table(table_name = 'Persons', table_df = table_df)


'''
Insert Data Into SQL Using Pandas Dataframe
'''
table_insert = {'PersonID': [2, 3],
                'LastName': ['DEF','XYZ'],
                'FirstName': ['ABC','PQR'],
                'Address': ['test1','test2'],
                'City': ['helsinki','espoo']
                  }

insert_df = pd.DataFrame(data=table_insert)

insert_sql_table(table_name = 'Persons', insert_df = insert_df)
    
'''
Select Statements From SQL Table
'''
selection_df = select_query_sql(query = "SELECT * FROM Persons")

'''
Create Machine Learning Workspace
'''
create_workspace(workspace_name='myworkspace',
                 subscription_id='subscription_id',
                 resource_group='resource_group',
                 create_resource_group=False,
                 location='westeurope'
                 )

'''
Create Machine Learning Experiment
'''
exp = create_experiment(experiment_name = 'sklearn-iris')


'''
Create Azure Cluster
'''
compute_target = create_cluster(batchai_cluster_name="traincluster")


'''
Upload (Data) Files to Azure
'''

ds = upload_files_training(src_dir='./data', remote_folder_name='iris')


'''
Create a Script Folder to Put Training Code in
'''

script_folder = './iris_scripts'
os.makedirs(script_folder, exist_ok=True)


'''
An estimator object is used to submit the run. Creation Below
'''

from azureml.train.estimator import Estimator

script_params = {
    '--data-folder': ds.as_mount(),
}

est = Estimator(source_directory=script_folder,
                script_params=script_params,
                compute_target=compute_target,
                entry_script='train.py',
                conda_packages=['scikit-learn','pandas'])

run = exp.submit(config=est)
run.wait_for_completion()

'''
Register The Model
'''

register_model(run, model_name='sklearn_iris', model_path='outputs/sklearn_iris_model.pkl')

'''
Download The Model From Azure
'''
model = download_model(model_name='sklearn_iris')

'''
Create YAML File
'''
create_yaml_file()

'''
Create ACI Configuration File
'''

aciconfig = create_deployment_config_file(cpu_cores=1, memory_gb=1, tags={"data": "Iris",  "method" : "sklearn_SVM"}, description='Predict Iris with sklearn')

'''
Deploy The Service
'''
service = deploy_service(execution_script="score.py", conda_file="myenv.yml", aciconfig=aciconfig, service_name='sklearn-mnist-svc', model=model, workspace=ws)





'''
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn import metrics
from sklearn import svm
import argparse
from sklearn import metrics
from sklearn import svm
from sklearn.externals import joblib
from azureml.core import Run
import numpy as np

parser = argparse.ArgumentParser()
args = parser.parse_args()


data_folder = os.path.join(os.getcwd(), 'data')

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

run = exp.start_logging()

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
'''


'''
iris = pd.read_csv("iris.csv", names=["Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width", "Class"], sep = ",")

iris[iris.Class=="Iris-setosa"] = 1
iris[iris.Class=="Iris-versicolor"] = 2
iris[iris.Class=="Iris-virginica"] = 3

if not os.path.exists('data'):
    os.makedirs('data')

train, test = train_test_split(iris, test_size = 0.3)
train_X = train[["Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width"]]
train_Y = train[["Class"]]
test_X = test[["Sepal_Length", "Sepal_Width", "Petal_Length", "Petal_Width"]]
test_Y = test[["Class"]]

train.to_csv("./data/iris_train.csv", sep = ",", index=False)
test.to_csv("./data/iris_test.csv", sep = ",", index= False, header=None)

test_svm = svm.SVC()
test_svm.fit(train_X, train_Y.Class)
y_hat = test_svm.predict(test_X)
metrics.accuracy_score(y_hat, test_Y)
'''




