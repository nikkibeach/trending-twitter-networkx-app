FROM python:3.10.6-slim

EXPOSE 8501

WORKDIR /app

COPY . /app

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", ""--server.port=80", "--server.address=0.0.0.0"]
