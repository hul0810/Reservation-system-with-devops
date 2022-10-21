FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9
WORKDIR /app
COPY ./requirements.txt requirements.txt
COPY . /app
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 8000
