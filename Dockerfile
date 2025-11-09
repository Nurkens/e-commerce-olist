FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY custom_exporter.py .

EXPOSE 8000

USER nobody

CMD ["python", "custom_exporter.py"]