@echo OFF
cls
call az login
SET AZURE_STORAGE_ACCOUNT=%1
SET AZURE_STORAGE_SAS_TOKEN=%2
SET container_name=%3
az storage container create --name %container_name% --sas-token %AZURE_STORAGE_SAS_TOKEN%