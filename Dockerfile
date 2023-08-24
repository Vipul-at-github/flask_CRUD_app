FROM python:latest

WORKDIR /CRUD_App/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]