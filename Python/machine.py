import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.multiclass import OneVsRestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import json
import uuid
import pickle
import joblib
import pandas as pd 

data = pd.read_excel ('base de datos.xlsx')
df=pd.DataFrame(data)
data=df.values
x1=data[:,:-2]
x=np.array(x1)
y1=data [:,-1]
y=np.array(y1)
y2=data [:,-2]



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
# example_dict = {1:modelo,2:X_test,3:Y_test}
# filename = 'prueba.sav'
# pickle.dump(example_dict, open(filename, 'wb'))


# # save the model to disk
# filename = 'prueba1.sav'
# joblib.dump(example_dict, filename)

