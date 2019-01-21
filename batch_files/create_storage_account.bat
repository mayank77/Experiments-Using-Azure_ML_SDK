@echo OFF
cls
call az login
SET storagename=%1
SET resource_group_name=%2
SET location_storage=%3
SET sku_val=%4
SET storage_kind=%5

az storage account create --name %storagename% --resource-group %resource_group_name% --location %location_storage% --sku %sku_val% --kind %storage_kind%