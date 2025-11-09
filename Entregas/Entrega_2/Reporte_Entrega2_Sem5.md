![Banner Simulación](imagenes/Banner.png)

# Entrega 2 – S5 PROJECT E2 (Semana 5)

**Proyecto:** Valoración de inmuebles en Bogotá

## Integrantes del equipo

- Diego Alejandro Lemus Guzman
- Valeria Iglesias Miranda
- Sergio Andres Perdomo Murcia
- Danilo Suarez Vargas


## 1. Problema y contexto (Bogotá)
La estimación del valor comercial de vivienda en **Bogotá** suele apoyarse en comparaciones manuales y criterios subjetivos. Esto introduce variabilidad y tiempos de respuesta elevados para compradores, vendedores y entidades financieras. Con el crecimiento de fuentes abiertas confiables a nivel **ciudad**, es factible construir una **solución analítica** que estandarice y acelere la valoración, con métricas de precisión trazables. La propuesta integra un modelo supervisado con un tablero web para que actores no técnicos consulten avalúos consistentes en segundos.

Esta situación reduce la transparencia y la comparabilidad de los avalúos e impacta la toma de decisiones de hogares, inmobiliarias, aseguradoras y banca hipotecaria. Con este proyecto buscamos disminuir tiempos y sesgos, entregando estimaciones consistentes y explicables para inmuebles en Bogotá, soportadas en datos abiertos verificables y una interfaz que expone la estimación con su intervalo de error e insights de las variables más influyentes.


## 2. Pregunta de negocio y alcance
**Pregunta de negocio.** ¿Cómo desarrollar e implementar un **modelo de predicción** (aprendizaje supervisado) que estime con precisión y rapidez el **valor** de un inmueble en **Bogotá** usando variables físicas, de localización y socioeconómicas, y cómo disponibilizarlo a través de un tablero que encapsule las predicciones, su banda de error y la explicación del modelo?

**Alcance (MVP de esta entrega).**
- Entradas: *área cubierta*, *número de cuartos*, *tipo de inmueble*, *localidad/barrio*, y otras disponibles en el dataset.
- Salida: *precio estimado* y bandas de error (±MAE).
- Métricas objetivo: **RMSE** y **MAE** en validación; reporte de **R²**.
- **Supuestos de la entrega:** enfoque en vivienda residencial; valores en COP; uso de datos abiertos consolidados para Bogotá.
- Fuera de alcance: Integración con APIs externas, actualización en tiempo real y despliegue productivo.

### Cambios respecto a la Entrega 1
- **Ámbito geográfico:** de *Colombia* → **Bogotá**, por disponibilidad y confiabilidad de datasets abiertos a nivel ciudad.
- **Datos:** se sustituyen fuentes generales por un corte consolidado exclusivo de Bogotá; se priorizan variables robustas y disponibles (precio, área, habitaciones, baños, tipo, barrio/UPZ).
- **Alcance del MVP:** se mantiene el prototipo con predicción y métricas (RMSE/MAE), sin APIs públicas ni actualización en tiempo real; se incorporan experimentos trazables en MLflow en EC2.


## 3. Conjuntos de datos a emplear (Bogotá)
**Archivo base:** `inmuebles_bogota.csv` (9,520 registros, 8 columnas).  
**Breve descripción:** datos de anuncios de inmuebles en Bogotá consolidados desde fuentes abiertas; variables principales: `valor` (precio), `área`, `habitaciones`, `baños`, `tipo`, `barrio` y `upz`.  
**Exploración breve (EDA mínima):** a continuación se incluye un resumen con hallazgos rápidos relevantes para el modelado.

### 3.1 Exploración breve (EDA mínima)

- **Tamaño:** 9,520 registros / 8 columnas.

- **Variables clave:** valor (precio), área, habitaciones, baños, tipo, barrio y UPZ.

- **Hallazgos rápidos:** predominan apartamentos sobre casas; la oferta se concentra en zonas del norte; se recomienda tratar atípicos en área/precio antes del entrenamiento.

<table style="width:100%; table-layout:fixed;">
  <tr>
    <td style="vertical-align:top; width:50%; padding-right:12px;">
      <strong>Top barrios por número de registros</strong>
      <table>
        <thead>
          <tr><th></th><th style="text-align:right;">registros</th></tr>
        </thead>
        <tbody>
          <tr><td>Usaquén</td><td style="text-align:right;">1105</td></tr>
          <tr><td>Zona Noroccidental</td><td style="text-align:right;">877</td></tr>
          <tr><td>Bosa</td><td style="text-align:right;">589</td></tr>
          <tr><td>Kennedy</td><td style="text-align:right;">589</td></tr>
          <tr><td>Cedritos</td><td style="text-align:right;">554</td></tr>
          <tr><td>Barrios Unidos</td><td style="text-align:right;">473</td></tr>
          <tr><td>Engativa</td><td style="text-align:right;">462</td></tr>
          <tr><td>Suba</td><td style="text-align:right;">443</td></tr>
          <tr><td>Santa Barbara</td><td style="text-align:right;">438</td></tr>
          <tr><td>Chapinero</td><td style="text-align:right;">332</td></tr>
          <tr><td>Fontibón</td><td style="text-align:right;">270</td></tr>
          <tr><td>Chico Reservado</td><td style="text-align:right;">225</td></tr>
          <tr><td>Teusaquillo</td><td style="text-align:right;">180</td></tr>
          <tr><td>El Batán</td><td style="text-align:right;">133</td></tr>
          <tr><td>Puente Aranda</td><td style="text-align:right;">116</td></tr>
        </tbody>
      </table>
    </td>
    <td style="vertical-align:top; width:50%; padding-left:12px;">
      <strong>Distribución por tipo de inmueble</strong>
      <table>
        <thead>
          <tr><th></th><th style="text-align:right;">registros</th></tr>
        </thead>
        <tbody>
          <tr><td>Apartamento</td><td style="text-align:right;">7327</td></tr>
          <tr><td>Casa</td><td style="text-align:right;">2043</td></tr>
          <tr><td>Oficina/Consultorio</td><td style="text-align:right;">60</td></tr>
          <tr><td>Local</td><td style="text-align:right;">38</td></tr>
          <tr><td>Edificio</td><td style="text-align:right;">22</td></tr>
          <tr><td>Bodega</td><td style="text-align:right;">13</td></tr>
          <tr><td>Finca</td><td style="text-align:right;">11</td></tr>
          <tr><td>Lote</td><td style="text-align:right;">6</td></tr>
        </tbody>
      </table>
    </td>
  </tr>
</table>


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
- **Objetivo:** operacionalizar la respuesta a la pregunta de negocio permitiendo que usuarios no técnicos ingresen los datos del inmueble y reciban un avalúo consistente con contexto de mercado.
- **Entradas:** localidad/barrio (selector alineado con UPZ), tipo de inmueble, área cubierta (m²), número de cuartos y número de baños. Cada campo incluye ayudas visuales para asegurar calidad en la captura.
- **Salidas:** valor estimado en COP, intervalo ±MAE mostrado como píldora destacada, resumen de características evaluadas, visualización de relación área vs. precio en Bogotá y módulo “Factores que más impactan tu avalúo” (espacio reservado para SHAP/feature importance).
- **Estado actual:** mockup navegable (`dashboard/mockup/mockup.html`) que define layout, textos y flujo. Puede abrirse con `open dashboard/mockup/mockup.html` o sirviendo la carpeta con `python3 -m http.server 8000`.
- **Siguiente paso:** conectar el formulario al endpoint `POST /api/v1/avaluo` para poblar el tablero con las predicciones reales y gestionar estados `loading/success/error`.



## 8. Reporte de trabajo en equipo (resumen)
> **Integrantes:** Diego Alejandro Lemus Guzman; Valeria Iglesias Miranda; Sergio Andres Perdomo Murcia; Danilo Suarez Vargas.

- **Datos/EDA:** preparación de cortes Bogotá, diccionario, limpieza básica.
- **Modelado (Valeria Iglesias):** experimentos en MLflow, comparación de modelos y selección (en progreso).
- **Tablero (Danilo Suarez):** diseño de la experiencia, construcción del mockup y definición de la integración con la API.
- **Infra/DevOps:** configuración de entorno (EC2/venv), tracking MLflow.
- **Documentación:** armado de este reporte y evidencias.



## 9. Observaciones y siguientes pasos
- La ubicación (localidad/barrio) y el tipo de inmueble son determinantes del precio; el área presenta efecto no lineal.
- Siguientes pasos: enriquecer con variables geoespaciales (distancia a vías/zonas de interés), robustecer detección de atípicos y evaluar validación cruzada por localidad.
