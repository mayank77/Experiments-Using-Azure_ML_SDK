@echo OFF
cls
call az login
SET adminlogin=%1
SET password=%2
SET servername=%3
SET resource_group_name=%4
SET location_db=%5
SET startip=%6
SET endip=%7
SET dbname=%8
SET serviceobjective=%9

call az sql server create --name %servername% --resource-group %resource_group_name% --location %location_db%  --admin-user %adminlogin% --admin-password %password%

call az sql server firewall-rule create --resource-group %resource_group_name% --server %servername% -n AllowYourIp --start-ip-address %startip% --end-ip-address %endip%

call az sql db create --resource-group %resource_group_name% --server %servername% --name %dbname% --service-objective %serviceobjective%