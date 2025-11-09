#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge, LinearRegression
import lightgbm as lgb


ruta = "../Notebooks/inmuebles_bogota 2.csv"
df = pd.read_csv(ruta)

df_modelo = df[['Tipo', 'Habitaciones', 'Baños', 'Área', 'Barrio', 'Valor', 'UPZ']].copy()

# elimina signos de $ y puntos de miles, luego convierte a float)
df_modelo['Valor'] = df_modelo['Valor'].replace('[\$,\.]', '', regex=True).astype(float)

df_modelo['log_valorventa'] = np.log10(df_modelo['Valor'])
df_modelo['log_marea'] = np.log10(df_modelo['Área'])


X = df_modelo[['Tipo', 'Habitaciones', 'Baños', 'log_marea', 'Barrio']]
y = df_modelo['log_valorventa']


X = pd.get_dummies(X, columns=['Tipo', 'Barrio'], drop_first=True)

# Dividir dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Configurar MLflow 
#mlflow.set_tracking_uri("http://localhost:5000")
# registre el experimento
experiment = mlflow.set_experiment("modelos_inmuebles_bogota")

modelos = {
    "RandomForest": RandomForestRegressor(n_estimators=200, max_depth=6, max_features=8, random_state=42),
    "Ridge": Ridge(alpha=4.0),
    "LinearRegression": LinearRegression(n_jobs=-1),
    "LightGBM": lgb.LGBMRegressor(num_leaves=31, learning_rate=0.01, n_estimators=200)
}
for nombre, modelo in modelos.items():
    with mlflow.start_run(experiment_id=experiment.experiment_id, run_name=nombre):
        print(f"\nEntrenando modelo: {nombre}")

        # Entrenamiento
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

        # Métricas
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Registrar en MLflow
        mlflow.log_param("modelo", nombre)
        mlflow.log_params(modelo.get_params())
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
        mlflow.sklearn.log_model(modelo, f"modelo_{nombre.lower()}")

        print(f"✅ {nombre} | MSE: {mse:.4f} | MAE: {mae:.4f} | R²: {r2:.4f}")

print("\nTodos los modelos entrenados y registrados correctamente")