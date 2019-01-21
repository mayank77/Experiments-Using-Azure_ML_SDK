# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:24:03 2018

@author: mayank.khandelwal
"""

import os
from azure.storage.blob import BlockBlobService, PublicAccess
from configparser import RawConfigParser 

def create_storage_account(storagename,
                           resource_group_name,
                           location_storage = 'westeurope',
                           sku = 'Standard_LRS',
                           storage_kind = 'StorageV2',
                           config_name = 'default',
                           saveconfig=True
                           ):
    
    file_path = os.path.join(os.getcwd(), 'batch_files\create_storage_account.bat')
    os.system("C:\Windows\System32\cmd.exe /c "+
              file_path +
              ' ' + storagename +
              ' ' + resource_group_name +
              ' ' + location_storage +
              ' ' + sku +
              ' ' + storage_kind
              )
    
    if saveconfig==True:
        if not os.path.exists("config"):
            os.mkdir("config")
        print("Saving Configuration to config/blob.ini \n Please Keep This File Secure.")
        config = RawConfigParser()
        config.read('config/blob.ini')
        config.add_section(config_name)
        config.set(config_name, 'storagename', storagename)
        config.set(config_name, 'resource_group_name', resource_group_name)
        config.set(config_name, 'location_storage', location_storage)
        config.set(config_name, 'sku', sku)
        config.set(config_name, 'storage_kind', storage_kind)
        with open('config/blob.ini', 'w') as f:
            config.write(f)

def save_storage_sas(sas_token, config_name = 'default'):
    if os.path.exists('config/blob.ini'):
        config = RawConfigParser()
        config.read('config/blob.ini')
        config.set(config_name, 'sas_token', sas_token)
        with open('config/blob.ini', 'w') as f:
            config.write(f)
    else:
        print("First Create config/blob.ini")
    
def create_container_storage(container_name, storagename="", sas_token="",load_from_config=True, config_name = 'default'):

    if load_from_config:
        if os.path.exists('config/blob.ini'):
            config = RawConfigParser()
            config.read('config/blob.ini')
            storagename = config.get(config_name, 'storagename')
            sas_token = config.get(config_name, 'sas_token')
        else:
            print("config/blob.ini does not exist")
    
    file_path = os.path.join(os.getcwd(), 'batch_files\create_container_storage.bat')
    os.system("C:\Windows\System32\cmd.exe /c "+
              file_path +
              ' ' + storagename +
              ' \"' + sas_token + '\"' +
              ' ' + container_name
              )

def list_files_blob(container_name, sas_token="", storagename="",load_from_config=True, config_name = 'default'):
    
    if load_from_config:
        if os.path.exists('config/blob.ini'):
            config = RawConfigParser()
            config.read('config/blob.ini')
            storagename = config.get(config_name, 'storagename')
            sas_token = config.get(config_name, 'sas_token')
        else:
            print("config/blob.ini does not exist")
    
    if sas_token[0]=='?':
        sas_token = sas_token[1:]
            
    block_blob_service = BlockBlobService(account_name=storagename, account_key = None, sas_token=sas_token)
    print("\nList blobs in the container: "+container_name)
    try:
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)
    except:
        print("Incorrect SAS Key")
        
        
        
def upload_file_blob(container_name, file_name_on_blob, full_path_to_file, sas_token="", storagename="", load_from_config=True, config_name = 'default'):

    if load_from_config:
        if os.path.exists('config/blob.ini'):
            config = RawConfigParser()
            config.read('config/blob.ini')
            storagename = config.get(config_name, 'storagename')
            sas_token = config.get(config_name, 'sas_token')
        else:
            print("config/blob.ini does not exist")
    
    if sas_token[0]=='?':
        sas_token = sas_token[1:]    
    
    block_blob_service = BlockBlobService(account_name=storagename, account_key = None, sas_token=sas_token)
    try:
        block_blob_service.create_blob_from_path(container_name, file_name_on_blob , full_path_to_file)
    except:
        print("Incorrect SAS Key")
        
def download_all_files_blob(container_name, storagename="", sas_token="", load_from_config=True, config_name = 'default'):

    if load_from_config:
        if os.path.exists('config/blob.ini'):
            config = RawConfigParser()
            config.read('config/blob.ini')
            storagename = config.get(config_name, 'storagename')
            sas_token = config.get(config_name, 'sas_token')
        else:
            print("config/blob.ini does not exist")
    
    if sas_token[0]=='?':
        sas_token = sas_token[1:]  
        
    if not os.path.exists("downloaded_from_blob"):
        os.mkdir("downloaded_from_blob")
    os.chdir(os.getcwd()+ "/downloaded_from_blob")
    block_blob_service = BlockBlobService(account_name=storagename, account_key = None, sas_token=sas_token)
    generator = block_blob_service.list_blobs(container_name)
    
    for blob in generator:
        if "/" in "{}".format(blob.name):
            head, tail = os.path.split("{}".format(blob.name))
            if (os.path.isdir(os.getcwd()+ "/" + head)):
                block_blob_service.get_blob_to_path(container_name,blob.name,os.getcwd()+ "/" + head + "/" + tail)
            else:
                os.makedirs(os.getcwd()+ "/" + head, exist_ok=True)
                block_blob_service.get_blob_to_path(container_name,blob.name,os.getcwd()+ "/" + head + "/" + tail)
        else:
            block_blob_service.get_blob_to_path(container_name,blob.name,blob.name)
    os.chdir(os.path.dirname(os.getcwd()))
    print("Files Are Downloaded in the \"downloaded_from_blob\" Directory")