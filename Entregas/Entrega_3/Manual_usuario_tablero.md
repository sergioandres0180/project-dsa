# Manual de usuario — Tablero AvaluaTuHome

![Banner AvaluaTuHome](banner.png)

## 1. Descripción general
- AvaluaTuHome es un tablero web para estimar el valor de inmuebles **residenciales en Bogotá**.
- Está pensado para usuarios no técnicos (inmobiliarias, bancos, particulares) que necesitan una referencia rápida de avalúo.
- Usa un modelo de producción para entregar el valor estimado, un rango de confianza y contexto gráfico del mercado.
- URL del tablero: `http://54.160.253.251:8501/`

> Nota: los valores son aproximados y no reemplazan un avalúo legal; se recomienda usarlos como apoyo a la decisión.

## 2. Antes de empezar
- Conexión a Internet estable.
- Navegador actualizado (Chrome, Edge, Firefox o similar).
- Información básica del inmueble en Bogotá:
  - Localidad/barrio.
  - Tipo de inmueble.
  - Área cubierta en m².
  - Número de cuartos y baños.

![Formulario de datos](Imagen_1_panel_info_por_usuario.png)
*Figura 1. Panel donde el usuario ingresa la información del inmueble.*

## 3. Datos que puedes ingresar (solo Bogotá)
- **Localidad/barrio**: selecciona la localidad donde está el inmueble (Bogotá).
- **Tipo de inmueble**: Apartamento, Casa, Studio u Oficina.
- **Área cubierta (m²)**: metros cuadrados del inmueble (número entero o decimal).
- **Cuartos y Baños**: números enteros (incluye baños sociales que sumen valor).

## 4. Pasos de uso
1. Abre el tablero en tu navegador.
2. Completa todos los campos del formulario (localidad, tipo, área, cuartos y baños).
3. Haz clic en **Calcular avalúo estimado**.
4. Revisa los paneles de resultados:
   - **Precio estimado (COP)**.
   - **Intervalo ±MAE**.
   - **Impacto de las variables**.
   - **Contexto de mercado (gráfico área vs. precio)**.

![Ejemplo de resultado](inagen_21_resultado_ejemplo.png)
*Figura 2. Resultado del avalúo con valor estimado, intervalo e impacto de variables.*

## 5. Cómo leer los resultados
- **Valor estimado**: es la mejor estimación del modelo para el inmueble que ingresaste.
- **Intervalo ±MAE**:
  - El límite inferior es un escenario conservador.
  - El límite superior es un escenario optimista.
  - El valor real suele ubicarse dentro de este rango si el inmueble es similar a los datos del modelo.
- **Impacto de variables**:
  - Muestra qué factores pesan más en el avalúo (ej. localidad y área suelen dominar).
  - Útil para identificar qué características mejoran más el valor de un inmueble.
- **Gráfico de comparables**:
  - Cada punto representa un inmueble similar en Bogotá.
  - Permite comparar el precio estimado de tu inmueble frente a inmuebles de área similar.

## 6. Manejo de errores
- Si aparece error al calcular:
  - Verifica conexión a internet y vuelve a intentar.
  - Si persiste, contacta al equipo indicando la hora del fallo.
- Si no carga el tablero:
  - Asegúrate de usar la URL correcta y que el puerto 8501 esté accesible.

## 7. Datos y privacidad
- Enviamos solo características del inmueble: `{localidad, tipo_inmueble, area_m2, cuartos, banos}`.
- No capturamos datos personales.
