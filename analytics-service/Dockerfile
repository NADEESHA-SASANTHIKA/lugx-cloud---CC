FROM python:3.9
WORKDIR /app
COPY app.py .
COPY export_clickhouse_to_pg.py .
RUN pip install flask flask_cors clickhouse-driver psycopg2-binary
CMD ["python", "app.py"]
