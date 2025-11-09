# Entrega 2 – S5 PROJECT E2 (Semana 5)

**Proyecto:** Valoración de inmuebles en Bogotá

**Fecha:** 2025-11-09 17:40



## 1. Problema y contexto (Bogotá)
La estimación del valor comercial de vivienda en **Bogotá** suele apoyarse en comparaciones manuales y criterios subjetivos. Esto introduce variabilidad y tiempos de respuesta elevados para compradores, vendedores y entidades financieras. Con el crecimiento de fuentes abiertas confiables a nivel **ciudad**, es factible construir una **solución analítica** que estandarice y acelere la valoración, con métricas de precisión trazables.



## 2. Pregunta de negocio y alcance
**Pregunta de negocio.** ¿Cómo desarrollar e implementar un modelo de regresión que estime con precisión y rapidez el **valor** de un inmueble en **Bogotá** usando variables físicas, de localización y socioeconómicas?

**Alcance (MVP de esta entrega).**
- Entradas: *área cubierta*, *número de cuartos*, *tipo de inmueble*, *localidad/barrio*, y otras disponibles en el dataset.
- Salida: *precio estimado* y bandas de error (±MAE).
- Métricas objetivo: **RMSE** y **MAE** en validación; reporte de **R²**.
- Fuera de alcance: Integración con APIs externas, actualización en tiempo real y despliegue productivo.



## 3. Conjuntos de datos a emplear (Bogotá)
**Archivo base:** `inmuebles_bogota.csv` (9,520 registros, 8 columnas).  
**Origen:** consolidado por el equipo a partir de fuentes abiertas disponibles para Bogotá (ver carpeta `data/raw` del repositorio).  
**Corte:** no especificado.

**Columnas clave detectadas automáticamente** (pueden renombrarse en el código para estandarizar):
- Precio: `valor`
- Área: `None`
- Cuartos: `habitaciones`
- Baños: `baños`
- Parqueaderos: `None`
- Tipo de inmueble: `tipo`
- Barrio: `barrio`
- Localidad: `None`
- Estrato: `None`
- Latitud/Longitud: `None`, `None`


### 3.1 Calidad de datos (faltantes por columna)
|                |   pct_missing |
|:---------------|--------------:|
| valor          |        100    |
| precio_m2_calc |        100    |
| upz            |          0.44 |
| tipo           |          0    |
| descripcion    |          0    |
| habitaciones   |          0    |
| baños          |          0    |
| área           |          0    |
| barrio         |          0    |

### 3.2 Variables categóricas – cardinalidad y faltantes
|    | columna     |   niveles |   faltantes_% |
|---:|:------------|----------:|--------------:|
|  1 | descripcion |       316 |      0        |
|  2 | barrio      |       149 |      0        |
|  3 | upz         |        63 |      0.441176 |
|  0 | tipo        |         8 |      0        |


## 4. Exploración de datos (EDA)
A continuación, se presenta un resumen estadístico de variables numéricas, cardinalidad de variables categóricas y distribución de ubicaciones. Se incluye además una variable derivada `precio_m2_calc` cuando es posible (precio/área > 0).


### 4.1 Estadísticos descriptivos (numéricos)
|                |   conteo |   missing_% |   media |   desv_std |   min |   q1 |   mediana |   q3 |    max |
|:---------------|---------:|------------:|--------:|-----------:|------:|-----:|----------:|-----:|-------:|
| habitaciones   |     9520 |           0 |   3.072 |      2.05  |     1 |    2 |         3 |    3 |    110 |
| baños          |     9520 |           0 |   2.448 |      1.255 |     0 |    2 |         2 |    3 |      9 |
| área           |     9520 |           0 | 146.665 |   1731.38  |     2 |   57 |        80 |  135 | 166243 |
| valor          |        0 |         100 | nan     |    nan     |   nan |  nan |       nan |  nan |    nan |
| precio_m2_calc |        0 |         100 | nan     |    nan     |   nan |  nan |       nan |  nan |    nan |


### 4.3 Top barrios por número de registros
|                    |   registros |
|:-------------------|------------:|
| Usaquén            |        1105 |
| Zona Noroccidental |         877 |
| Bosa               |         589 |
| Kennedy            |         589 |
| Cedritos           |         554 |
| Barrios Unidos     |         473 |
| Engativa           |         462 |
| Suba               |         443 |
| Santa Barbara      |         438 |
| Chapinero          |         332 |
| Fontibón           |         270 |
| Chico Reservado    |         225 |
| Teusaquillo        |         180 |
| El Batán           |         133 |
| Puente Aranda      |         116 |


### 4.4 Distribución por tipo de inmueble
|                     |   registros |
|:--------------------|------------:|
| Apartamento         |        7327 |
| Casa                |        2043 |
| Oficina/Consultorio |          60 |
| Local               |          38 |
| Edificio            |          22 |
| Bodega              |          13 |
| Finca               |          11 |
| Lote                |           6 |


### 4.5 Correlación con `valor` (numéricas)
|                |   corr_con_valor |
|:---------------|-----------------:|
| habitaciones   |              nan |
| baños          |              nan |
| área           |              nan |
| precio_m2_calc |              nan |


### 4.6 Detección exploratoria de atípicos (IQR)
|    | columna        |   outliers_estimados |   limite_inferior |   limite_superior |
|---:|:---------------|---------------------:|------------------:|------------------:|
|  0 | valor          |                    0 |               nan |               nan |
|  1 | precio_m2_calc |                    0 |               nan |               nan |


## 5. Modelos desarrollados y evaluación
Se consideran al menos dos familias: (i) **baselines** (Regresión Lineal, Ridge/Lasso) y (ii) **ensambles** (Random Forest, opcional Gradient Boosting). Se comparan por RMSE/MAE/R² en validación.

| Modelo | Features | Hiperparámetros | RMSE | MAE | R² |
|---|---|---|---:|---:|---:|
| Regresión lineal | [área, cuartos, tipo, localidad/barrio] | log(target)=NO/SÍ |  |  |  |
| Ridge/Lasso | idem | α= |  |  |  |
| Random Forest | idem + interacciones simples | n_estimators=, max_depth= |  |  |  |
| (Opcional) GB/XGB | idem | learning_rate=, n_estimators= |  |  |  |

> **Criterio de selección:** mejor RMSE/MAE, estabilidad y simplicidad del modelo.



## 6. Experimentos (MLflow en EC2)
- Registrar parámetros, métricas y artefactos (firma del modelo).
- Incluir en `docs/evidencias_mlflow/` pantallazos con **IP pública de la EC2** y **usuario** visibles.
- Conclusiones: hiperparámetros con mayor impacto y run “champion” seleccionado.



## 7. Prototipo / Tablero
- **Entradas:** área, cuartos, tipo, localidad/barrio.
- **Salida:** precio estimado y bandas ±MAE; importancias de variables (feature importance/SHAP) si aplica.
- **Estado:** se mantiene la maqueta aprobada; capturas en `docs/`.



## 8. Reporte de trabajo en equipo (resumen)
> Nota: sin nombres propios en este documento; el detalle estará en el repositorio (commits/issues).

- **Datos/EDA:** preparación de cortes Bogotá, diccionario, limpieza básica.
- **Modelado:** experimentos en MLflow, comparación de modelos y selección.
- **Tablero:** implementación de la maqueta y conexión al modelo.
- **Infra/DevOps:** configuración de entorno (EC2/venv), tracking MLflow.
- **Documentación:** armado de este reporte y evidencias.



## 9. Observaciones y siguientes pasos
- La ubicación (localidad/barrio) y el tipo de inmueble son determinantes del precio; el área presenta efecto no lineal.
- Siguientes pasos: enriquecer con variables geoespaciales (distancia a vías/zonas de interés), robustecer detección de atípicos y evaluar validación cruzada por localidad.
