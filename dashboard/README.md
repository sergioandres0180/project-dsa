# Dashboard AvaluaTuHome

Este directorio contiene dos artefactos complementarios:

1. `mockup/`: maqueta HTML estática utilizada para acordar textos, colores y jerarquía del tablero.
2. `app.py`: implementación en Streamlit que permite ejecutar el tablero localmente mientras se integra el modelo.

## Requisitos

- Python 3.10+
- Entorno virtual recomendado (`python -m venv .venv && source .venv/bin/activate`)
- Dependencias:
  ```bash
  pip install streamlit pandas numpy
  ```

> Cuando el modelo esté desplegado, la app podrá consumirlo configurando la variable de entorno `MODEL_ENDPOINT` con la URL del endpoint `POST /api/v1/avaluo`.

## Ejecutar la aplicación

Desde la raíz del repositorio:

```bash
cd dashboard
streamlit run app.py
```

Esto abrirá automáticamente `http://localhost:8501` con el tablero interactivo. Si `MODEL_ENDPOINT` no está definido, la app usa datos y lógica mock para evidenciar el flujo completo (captura → estimación → contexto).

## Próximos pasos

1. Conectar el formulario con la API real y mostrar estados `loading/error` según la respuesta.
2. Reemplazar los datos mock de los gráficos por comparables reales (dataset o endpoint dedicado).
3. Mostrar importancias reales (SHAP/feature importance) en el módulo de “Impacto de las variables”.
