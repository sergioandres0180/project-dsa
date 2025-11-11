import pickle
import pandas as pd
import numpy as np


ruta = "../Notebooks/inmuebles_bogota 2.csv"
df = pd.read_csv(ruta) 

X_model = df[['Tipo', 'Barrio', 'Habitaciones', 'Baños', 'Área']].copy()

# Crear log_marea y dummies como en entrenamiento
X_model['log_marea'] = np.log10(X_model['Área'])

X_model = pd.get_dummies(X_model, columns=['Tipo', 'Barrio'], drop_first=True)

# Solo dejar columnas que entraron al modelo (sin 'Área' original)
X_model = X_model.drop(columns=['Área'])

columnas_modelo = X_model.columns

with open("columnas_modelo.pkl", "wb") as f:
    pickle.dump(columnas_modelo, f)
