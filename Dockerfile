FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && useradd -m appuser && mkdir /data && chown appuser /data
COPY app app
USER appuser
ENV DB_PATH=/data/tasks.db
EXPOSE 8000
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
