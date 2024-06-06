FROM python:3.12
COPY . /app
RUN pip install --no-cache-dir -r ./app/requirements.txt
WORKDIR /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]