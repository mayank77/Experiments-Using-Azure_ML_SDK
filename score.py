# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 19:01:44 2018

@author: mayank.khandelwal
"""

import json
import numpy as np
import os
import pickle
import pandas as pd
from sklearn.externals import joblib
from sklearn import metrics
from sklearn import svm

from azureml.core.model import Model

def init():
    global model
    # retreive the path to the model file using the model name
    model_path = Model.get_model_path('sklearn_iris')
    model = joblib.load(model_path)

def run(raw_data):
    data = np.array(json.loads(raw_data)['data'])
    y_hat = model.predict(data)
    return json.dumps(y_hat.tolist())