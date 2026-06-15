# Builds the dummy app
1. FROM python:3.11-slim
2. WORKDIR /app
3. COPY requirements.txt .
4. RUN pip install --no-cache-dir -r requirements.txt
5. COPY app.py .
6. EXPOSE 5000
7. CMD ["python", "app.py"]