# -*- coding: utf-8 -*-
"""
Created on Fri Nov  2 14:10:27 2018

@author: mayank.khandelwal
"""

'''
pip install --upgrade azureml-sdk[notebooks,automl]
pip install azureml-sdk[notebooks]

'''

from azureml.core import Workspace, Run
from azureml.core import Experiment
from azureml.core.model import Model
from azureml.core.compute import ComputeTarget, BatchAiCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.conda_dependencies import CondaDependencies 
from azureml.core.webservice import AciWebservice
from azureml.core.webservice import Webservice
from azureml.core.image import ContainerImage

def create_workspace(workspace_name, subscription_id, resource_group, location='westeurope', create_resource_group=False):

    ws = Workspace.create(name=workspace_name,
                          subscription_id=subscription_id,
                          resource_group=resource_group,
                          create_resource_group=create_resource_group,
                          location=location
                         )
    
    ws.write_config()

def create_experiment(experiment_name):
    workspace = Workspace.from_config()
    exp = Experiment(workspace=workspace, name=experiment_name)
    return exp




def create_cluster(batchai_cluster_name, vm_size="STANDARD_D2_V2", cluster_min_nodes=0, cluster_max_nodes=2, autoscale_enabled=True):
    workspace = Workspace.from_config()
    try:
        compute_target = ComputeTarget(workspace=workspace, name=batchai_cluster_name)
        if type(compute_target) is BatchAiCompute:
            print('found compute target {}, just use it.'.format(batchai_cluster_name))
        else:
            print('{} exists but it is not a Batch AI cluster. Please choose a different name.'.format(batchai_cluster_name))
        return compute_target
    except ComputeTargetException:
        print('creating a new compute target...')
        compute_config = BatchAiCompute.provisioning_configuration(vm_size=vm_size,
                                                                   autoscale_enabled=autoscale_enabled,
                                                                   cluster_min_nodes=cluster_min_nodes, 
                                                                   cluster_max_nodes=cluster_max_nodes)
    
        compute_target = ComputeTarget.create(workspace, batchai_cluster_name, compute_config) #Create Cluster
        compute_target.wait_for_completion(show_output=True, min_node_count=None, timeout_in_minutes=20)
        print(compute_target.status.serialize())
        return compute_target

def upload_files_training(src_dir, remote_folder_name):
    workspace = Workspace.from_config()
    ds = workspace.get_default_datastore()
    ds.upload(src_dir=src_dir, target_path=remote_folder_name, overwrite=True, show_progress=True)
    print("File Stored To Resource : " + ds.account_name + "\nFile Store : " + ds.container_name)
    return ds

def register_model(run, model_name, model_path):
    model = run.register_model(model_name='sklearn_iris', model_path=model_path)
    print("Model Name : " + str(model.name) + "; ID : " + str(model.id) + "; Version : " + str(model.version))
    
def download_model(model_name):
    workspace = Workspace.from_config()
    model=Model(workspace, model_name)
    model.download(target_dir = '.')
    return model

def create_yaml_file():
    myenv = CondaDependencies()
    myenv.add_conda_package("scikit-learn")
    myenv.add_conda_package("pandas")
    
    with open("myenv.yml","w") as f:
        f.write(myenv.serialize_to_string())
        
    with open("myenv.yml","r") as f:
        print(f.read())
        
def create_deployment_config_file(cpu_cores=1, memory_gb=1, tags={"data" : "data"}, description=''):

    return AciWebservice.deploy_configuration(cpu_cores=1, 
                                                   memory_gb=1, 
                                                   tags={"data": "Iris",  "method" : "sklearn_SVM"}, 
                                                   description='Predict Iris with sklearn')
    
def deploy_service(execution_script, conda_file, aciconfig, service_name, model, workspace, runtime="python"):

    image_config = ContainerImage.image_configuration(execution_script=execution_script, 
                                                      runtime=runtime, 
                                                      conda_file=conda_file)
    
    service = Webservice.deploy_from_model(workspace=workspace,
                                           name=service_name,
                                           deployment_config=aciconfig,
                                           models=[model],
                                           image_config=image_config)
    service.wait_for_deployment(show_output=True)
    print(service.scoring_uri)
    return service
    