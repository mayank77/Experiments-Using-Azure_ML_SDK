# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 16:29:27 2018

@author: mayank.khandelwal
"""

import os
import pyodbc
import pandas as pd
import sqlalchemy
from configparser import RawConfigParser 

def create_azure_dbserver_database(username_dbserver,
                                   password_dbserver,
                                   name_dbserver,
                                   resource_group_name,
                                   dbname,
                                   location_db = 'westeurope',
                                   startip = '0.0.0.0',
                                   endip = '0.0.0.0',
                                   serviceobjective = 'S0',
                                   saveconfig=True,
                                   config_name = 'default'
                                   ):
    
    file_path = os.path.join(os.getcwd(), 'batch_files\create_sql_server_db.bat')
    os.system("C:\Windows\System32\cmd.exe /c "+
              file_path +
              ' ' + username_dbserver +
              ' ' + password_dbserver +
              ' ' + name_dbserver +
              ' ' + resource_group_name +
              ' ' + location_db +
              ' ' + startip +
              ' ' + endip +
              ' ' + dbname +
              ' ' + serviceobjective
              )

    
    if saveconfig==True:
        if not os.path.exists("config"):
            os.mkdir("config")
        print("Saving Configuration to config/db_dbserver.ini \n Please Keep This File Secure.")
        config = RawConfigParser()
        config.read('config/db_dbserver.ini')
        config.add_section(config_name)
        config.set(config_name, 'username_dbserver', username_dbserver)
        config.set(config_name, 'password_dbserver', password_dbserver)
        config.set(config_name, 'name_dbserver', name_dbserver)
        config.set(config_name, 'resource_group_name', resource_group_name)
        config.set(config_name, 'location_db', location_db)
        config.set(config_name, 'startip', startip)
        config.set(config_name, 'endip', endip)
        config.set(config_name, 'dbname', dbname)
        config.set(config_name, 'serviceobjective', serviceobjective)
        with open('config/db_dbserver.ini', 'w') as f:
            config.write(f)


def create_sql_table(table_name, table_df, server="", database="", username="", password="", driver='{ODBC Driver 13 for SQL Server}',load_from_config=True, config_name = 'default'):
    
    if load_from_config:
        if os.path.exists('config/db_dbserver.ini'):
            config = RawConfigParser()
            config.read('config/db_dbserver.ini')
            server = str(config.get(config_name, 'name_dbserver')) + ".database.windows.net"
            database = config.get(config_name, 'dbname')
            username = config.get(config_name, 'username_dbserver')
            password = config.get(config_name, 'password_dbserver')
        else:
            print("config/db_dbserver.ini does not exist")
    
    cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()
    
    query = "CREATE TABLE " + table_name + " ("
    first_entry = 1
    for index, row in table_df.iterrows():
        if first_entry == 0:
            query = query + " , "
        query = query + row['Column_Name'] + " "
        query = query + row['DataType']
        if(row['Size']!=''):
            query = query + "(" + str(row['Size']) + ")"
        first_entry = 0
            
    query = query + ")"
    
    cursor.execute(query)
    
    cnxn.commit()
    cursor.close()
    cnxn.close()
    
'''
def select_query_sql(query, server, database, username, password,  driver='{ODBC Driver 13 for SQL Server}'):
        cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)      
        return pd.read_sql(query,cnxn)
'''
    
def select_query_sql(query, server="", database="", username="", password="",  driver='{ODBC Driver 13 for SQL Server}',load_from_config=True, config_name = 'default'):
    
    if load_from_config:
        if os.path.exists('config/db_dbserver.ini'):
            config = RawConfigParser()
            config.read('config/db_dbserver.ini')
            server = str(config.get(config_name, 'name_dbserver')) + ".database.windows.net"
            database = config.get(config_name, 'dbname')
            username = config.get(config_name, 'username_dbserver')
            password = config.get(config_name, 'password_dbserver')
        else:
            print("config/db_dbserver.ini does not exist")
    
    db_prefix = 'mssql+pyodbc://'
    connection_string = "{db_prefix}{user_name}:{password}@{uri}/{db_name}?Driver={driver}".format(
                    db_prefix=db_prefix, user_name=username, password=password, uri=server, db_name=database,
                    driver=driver)
    engine = sqlalchemy.engine.create_engine(connection_string)
    engine.connect() 
    return pd.read_sql(query, engine)


def insert_sql_table(table_name, insert_df, server="", database="", username="", password="", driver='{ODBC Driver 13 for SQL Server}', if_exists='append', index=False,load_from_config=True, config_name = 'default'):
        
    if load_from_config:
        if os.path.exists('config/db_dbserver.ini'):
            config = RawConfigParser()
            config.read('config/db_dbserver.ini')
            server = str(config.get(config_name, 'name_dbserver')) + ".database.windows.net"
            database = config.get(config_name, 'dbname')
            username = config.get(config_name, 'username_dbserver')
            password = config.get(config_name, 'password_dbserver')
        else:
            print("config/db_dbserver.ini does not exist")
    
        db_prefix = 'mssql+pyodbc://'
        connection_string = "{db_prefix}{user_name}:{password}@{uri}/{db_name}?Driver={driver}".format(
                        db_prefix=db_prefix, user_name=username, password=password, uri=server, db_name=database,
                        driver=driver)
        engine = sqlalchemy.engine.create_engine(connection_string)
        engine.connect() 
        insert_df.to_sql(name=table_name,con=engine, if_exists=if_exists,index=index)    
    


    
