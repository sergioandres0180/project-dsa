# Tablero de avalúos — Entrega de mockup funcional

Este documento acompaña la entrega de la versión mockup del tablero de avalúos desarrollada para la semana 5 del proyecto. Resume el alcance logrado, las decisiones de diseño y el plan de integración con la API/modelo que el resto del equipo liberará en iteraciones futuras.

## 1. Objetivo de la entrega

Proveer una referencia navegable que evidencia:

- Flujo completo desde captura de datos del inmueble hasta visualización de resultados.
- Lineamientos visuales y de experiencia acordados con el equipo.
- Espacios reservados para integrar inferencias y métricas tan pronto el modelo esté disponible.

## 2. Alcance de esta iteración

- **Screen 1 – Formulario**: recolección de ciudad, tipo de inmueble, área, cuartos y baños con botón primario “Calcular avalúo”.
- **Screen 2 – Resultados**: tarjeta lateral con valor estimado y resumen de inputs, más dos visualizaciones (comparables por ciudad y panorama nacional).
- **Sistema visual**: paleta primaria (#6F2CFF) + secundarios neutros, tipografía Inter, grid de 12 columnas y componentes reutilizables definidos en CSS.

## 3. Proceso seguido

1. **Descubrimiento**: consolidación de requerimientos del curso (modelo supervisado + tablero conectados por API). Identificación de variables de entrada disponibles y métricas clave para el usuario final.
2. **Wireframe de baja fidelidad**: bosquejos en papel para validar jerarquía (formulario → resultado → insights comparativos).
3. **UI de alta fidelidad**: construcción en HTML/CSS (`mockup.html`) con fuentes y colores definitivos para acelerar la transferencia al framework elegido (Streamlit/Dash) sin re-trabajos.

## 4. Decisiones de diseño

- **Identidad visual**: morado #6F2CFF como color de marca y acción, gris #F5F6FB para fondo y neutros #2C2C2C/#6B6B6B para texto. Garantiza contraste AA en botones y mensajes.
- **Componentes**: inputs con bordes suaves, tarjetas elevadas (shadow) para separar paneles, ícono de casa como ancla visual en ambas pantallas.
- **Feedback**: se definirán estados `idle`, `loading`, `success`, `error`. En el mock el CTA desencadena una transición visual; en la versión productiva se mostrará spinner/alertas según respuesta de la API.
- **Visualizaciones**: Platzholders para scatter de área vs. precio y bubble chart por ciudad. Estos gráficos se alimentarán de endpoints de comparables o de agregados calculados en backend.

## 5. Integración prevista con la API

- **Endpoint estimado**: `POST /api/v1/avaluo`

```json
{
  "ciudad": "Bogotá",
  "tipo_inmueble": "Apartamento",
  "area_m2": 60,
  "cuartos": 3,
  "banos": 2
}
```

- **Respuesta esperada**:

```json
{
  "avaluo_cop": 250000000,
  "intervalo_confianza": [230000000, 270000000],
  "comparables_ciudad": [...],
  "comparables_nacional": [...]
}
```

La capa de presentación mapeará el campo `avaluo_cop` al panel principal y usará los bloques `comparables_*` para alimentar los gráficos. El mockup ya contempla el layout requerido para mostrar mensajes de error si el endpoint no responde.

## 6. Artefactos incluidos

- `dashboard/mockup/mockup.html`: maqueta navegable construida con HTML/CSS y fuentes alojadas en Google Fonts.
- `dashboard/mockup/README.md`: este documento de entrega y plan de integración.

## 7. Cómo visualizar la maqueta

Opción rápida (macOS):

```bash
open dashboard/mockup/mockup.html
```


## 8. Próximos hitos

1. Conectar el formulario a la API real y mostrar estados de carga y error.
2. Reemplazar los placeholders de gráficos con componentes dinámicos (Streamlit/Dash) alimentados por los datos de comparables.
3. Incorporar métricas adicionales (SHAP, ranking de barrios) una vez el equipo de modelado exponga esos artefactos en MLflow/DVC.
