# Usa la imagen oficial de Python 3.11
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone los puertos para FastAPI (8000) y Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Comando para iniciar ambas aplicaciones en paralelo
CMD uvicorn --reload src.app:api_router --host 0.0.0.0 --port 8000 & streamlit run main.py --server.port 8501 --server.address 0.0.0.0