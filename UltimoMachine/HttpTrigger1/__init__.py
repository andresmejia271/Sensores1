import logging
import azure.functions as func
import json
import pyodbc
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.naive_bayes import CategoricalNB
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import pandas as pd
import uuid
import os
# Definicion de la funcion de traseo de error.
def traceDB(cnxnAzure,uuid,message):
    query = "INSERT INTO [dbo].[logs] ([ID],[Fecha],[Descripcion]) VALUES ('{}',GETDATE(),'{}')".format(uuid,message)
    cnxnAzure.execute(query)
    cnxnAzure.commit()
    return(True)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Seteo de variables globales.')
    ID = str(uuid.uuid1())
    logging.info(ID)
    driverAzure = os.environ["DriverAzure"]
    serverAzure = os.environ["ServerBdAzure"]
    databaseAzure = os.environ["DataBaseAzure"]
    usernameAzure = os.environ["UserNameBdAzure"]
    passwordAzure = os.environ["PassWordBdAzure"]
    SQL_audicion = os.environ["SQL_audicion"]
    SQL_X = os.environ["X"]
    SQL_Y = os.environ["Y"]
    logging.info(SQL_audicion)

    logging.info('Establece conexión con la base de datos Conectados.')
    logging.warning('Establece conexión con la base de datos Conectados.')
    logging.error('Establece conexión con la base de datos Conectados.')
    conStringAzure = "DRIVER={{{}}};SERVER={};DATABASE={};UID={};PWD={}".format(driverAzure,serverAzure,databaseAzure,usernameAzure,passwordAzure)
    logging.info(conStringAzure)
    cnxnAzure = pyodbc.connect(conStringAzure)
    logging.info('Conexión establecida con la base de datos Azure.')
    traceDB(cnxnAzure,ID,'Inicio servicio web.')

    logging.info('Obtiene parámetros del JSON.')
    traceDB(cnxnAzure,ID,'Parámetros del servicio recibidos.')
    req_body = req.get_json()
    variable1 = req_body.get('variable1')
    logging.info(variable1)

    query = (SQL_audicion)
    df_datos = pd.read_sql_query(query,cnxnAzure)
    diccionario = df_datos.to_dict('dict')
    json_response = json.dumps(diccionario,indent=2)


    query2 = (SQL_X)
    df_datos2 = pd.read_sql_query(query2,cnxnAzure)
    diccionario2 = df_datos2.to_dict('dict')
    json_response2 = json.dumps(diccionario2,indent=2)
    
    query3 = (SQL_Y)
    df_datos3 = pd.read_sql_query(query3,cnxnAzure)
    diccionario3 = df_datos3.to_dict('dict')
    json_response3 = json.dumps(diccionario3,indent=2)

    x=df_datos2
    y=df_datos3
    
    logging.info(x)
    logging.info(y)




    X_train, X_test, Y_train, Y_test = train_test_split(x,y,test_size=0.3,random_state=42)

    modelo = SVC(gamma='auto')
    modelo.fit(X_train, Y_train)
    predicciones = modelo.predict(X_test)

    
    modelo2 = OneVsRestClassifier(SVC()).fit(x, y)
    predicciones2=modelo2.predict(X_test)

    modelo3= MultinomialNB()
    modelo3.fit(x, y)
    predicciones3= modelo3.predict(X_test)

    json_response4= json.dumps(classification_report(Y_test, predicciones),indent=2)
    json_response5 = json.dumps(classification_report(Y_test, predicciones2),indent=2)
    json_response6 = json.dumps(classification_report(Y_test, predicciones3),indent=2)

    if variable1 == 5:
        return func.HttpResponse(json_response4)
    elif variable1 == 6:
        return func.HttpResponse(json_response5)
    elif variable1 == 7:
        return func.HttpResponse(json_response6)
    else:
        return func.HttpResponse("Puede que se ingresara in valor mal en el postman pero la funcion se ejecuto meleramente",status_code=200)