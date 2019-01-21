@echo OFF
cls
call az login
SET accountname=%1
SET resource_group_name=%2
SET location_cosmos=%3
SET cosmos_consistency=%4
SET cosomos_kind=%5
SET multiple_write_locations=%6

az cosmosdb create --resource-group %resource_group_name% --name %accountname% --kind %cosomos_kind% --locations %location_cosmos%=0 --default-consistency-level %cosmos_consistency% --enable-multiple-write-locations %multiple_write_locations%