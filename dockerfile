# 1. Usar a imagem base do Python
FROM python:3

# 2. Atualizar e instalar dependências do sistema necessárias para OpenCV e dlib
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopencv-dev \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Configurar o diretório de trabalho
WORKDIR /open_gate-main

# 4. Copiar os arquivos da aplicação para o container
COPY static/ static/
COPY templates/ templates/
COPY main.py .

# 5. Instalar as bibliotecas Python necessárias
RUN pip install --upgrade pip && pip install --no-cache-dir flask opencv-python face_recognition setuptools

# 6. Expor a porta que a aplicação Flask vai utilizar
EXPOSE 8080

# 7. Comando para rodar a aplicação
CMD ["python", "main.py"]
