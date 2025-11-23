# Manual de instalación — API y Tablero AvaluaTuHome

![Banner AvaluaTuHome](banner.png)

## 1. Qué incluye este repositorio
- Código de la API (`api/`), código del tablero (`dashboard/`), artefactos del modelo (`models/model.pkl`, `columnas_modelo.pkl`) y Dockerfiles (`Dockerfile.api`, `Dockerfile.dashboard`).
- Manuales y documentación se encuentran en `Entregas/Entrega_3/`.
- Repositorio GitHub: `https://github.com/sergioandres0180/project-dsa.git` (clónalo o descárgalo antes de empezar).

## 2. Guía rápida de pasos
1. Clona el repositorio `project-dsa`.
2. Verifica los requisitos (Docker, AWS CLI, acceso a AWS, modelo en `models/`).
3. Verifica que las imágenes ya existan en ECR (API y tablero).
4. Crea clúster y servicios en ECS Fargate utilizando esas imágenes.
5. Valida URLs de API y tablero.
6. Opcional: prueba API y tablero en local.
7. Opcional: si actualizas el código, reconstruye y publica nuevas imágenes.

## 3. Requisitos previos
Herramientas básicas para construir, empaquetar y desplegar la API y el tablero.
- Cuenta/acceso a AWS con permisos básicos (ECR/ECS).
- Docker Desktop instalado y funcionando (`docker run hello-world`).
- AWS CLI instalado y autenticado (`aws sts get-caller-identity` debe responder).
- Archivos del modelo: `models/model.pkl` y `models/columnas_modelo.pkl`.

## 4. Repositorios de contenedores
Las imágenes de la API y del tablero se almacenan en ECR para que ECS pueda descargarlas al desplegar. En nuestro caso ya existen repositorios en ECR (región `us-east-1`); si trabajas en otra cuenta, deberás crear repositorios equivalentes.
  - API: `...dkr.ecr.us-east-1.amazonaws.com/avaluos-api`
  - Tablero: `...dkr.ecr.us-east-1.amazonaws.com/avaluos-tablero`

Login a ECR:
```bash
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <tu_cuenta>.dkr.ecr.us-east-1.amazonaws.com
```

## 5. (Opcional) Reconstruir y publicar imágenes
Solo necesario si modificas el código de la API o del tablero. Docker empaqueta código + dependencias; buildx para `linux/amd64` asegura compatibilidad con Fargate.
API:
```bash
docker buildx build --platform linux/amd64 \
  -t <tu_cuenta>.dkr.ecr.us-east-1.amazonaws.com/avaluos-api:latest \
  -f Dockerfile.api --push .
```
Tablero:
```bash
docker buildx build --platform linux/amd64 \
  -t <tu_cuenta>.dkr.ecr.us-east-1.amazonaws.com/avaluos-tablero:latest \
  -f Dockerfile.dashboard --push .
```

## 6. Despliegue en ECS (Fargate)
ECS Fargate orquesta los contenedores sin gestionar servidores; crea servicios para API y tablero.
1. Crea un clúster Fargate (ej. `avaluos-cluster`).
2. Define la tarea de la **API**:
   - Imagen: `avaluos-api:latest`
   - Puerto contenedor: 8000/TCP
   - Recursos sugeridos: 0.5 vCPU, 1–2 GB RAM
   - Security Group: regla inbound TCP 8000 desde 0.0.0.0/0 (o restringido según políticas).
3. Define la tarea del **Tablero**:
   - Imagen: `avaluos-tablero:latest`
   - Puerto contenedor: 8501/TCP
   - Variable de entorno: `MODEL_ENDPOINT=http://<HOST_API>:8000/api/v1/avaluo`
   - Recursos sugeridos: 0.5 vCPU, 1–2 GB RAM
   - Security Group: regla inbound TCP 8501 desde 0.0.0.0/0 (o restringido).
4. Crea un servicio para cada tarea (1 tarea) en subredes públicas. Opcional: agrega un ALB para una URL fija.

## 7. Validación rápida (producción)
- API: `http://3.90.237.192:8000/health` y `/docs`.
- Tablero: `http://54.160.253.251:8501/` y ejecuta un avalúo para confirmar respuesta.

## 8. Ejecución local (opcional, sin AWS)
Permite probar la API y el tablero en tu computador sin usar AWS. A continuación se describen los pasos desde cero.

### 8.1 Instalación de Python y entorno virtual

**macOS / Linux**
1. Verifica que tengas Python 3 instalado:
   ```bash
   python3 --version
   ```
   Si no lo tienes, instala la versión 3.10+ desde https://www.python.org/downloads/.
2. Crea un entorno virtual (aisla las librerías del proyecto):
   ```bash
   cd project-dsa
   python3 -m venv .venv
   source .venv/bin/activate
   ```

**Windows**
1. Verifica Python:
   ```powershell
   python --version
   ```
   Si no lo tienes, instala Python 3.10+ desde https://www.python.org/downloads/windows/.
2. Crea y activa el entorno virtual:
   ```powershell
   cd project-dsa
   python -m venv .venv
   .venv\Scripts\activate
   ```

### 8.2 Levantar la API en local
1. Instala dependencias de la API:
   ```bash
   pip install -r api/requirements.txt
   ```
2. Ejecuta la API:
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port 8000
   ```
3. Abre `http://localhost:8000/docs` en el navegador y prueba el endpoint `POST /api/v1/avaluo`.

### 8.3 Levantar el tablero en local
1. En otra terminal, activa el mismo entorno virtual (`source .venv/bin/activate` en macOS/Linux, `.venv\Scripts\activate` en Windows).
2. Define la URL de la API local:
   ```bash
   export MODEL_ENDPOINT="http://localhost:8000/api/v1/avaluo"   # macOS/Linux
   ```
   ```powershell
   setx MODEL_ENDPOINT "http://localhost:8000/api/v1/avaluo"     # Windows (PowerShell)
   ```
3. Instala dependencias del tablero:
   ```bash
   pip install -r dashboard/requirements.txt
   ```
4. Ejecuta el tablero:
   ```bash
   streamlit run dashboard/app.py
   ```
5. Abre `http://localhost:8501` en tu navegador y realiza un avalúo de prueba.

## 9. Mantenimiento y cambios de IP
Al redeployar pueden cambiar las IPs; un ALB evita actualizar el endpoint manualmente.
- Si redeployas la API con IP nueva, actualiza `MODEL_ENDPOINT` en la task del tablero y fuerza “new deployment”.
- Para evitar cambios de IP, usa un Load Balancer (ALB) y apunta `MODEL_ENDPOINT` al DNS del ALB.
- Mantén los SG abiertos en puertos 8000 (API) y 8501 (tablero) según la política de acceso.
