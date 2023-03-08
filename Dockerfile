# App: Interpol
FROM python:3.8

COPY interpol /interpol

WORKDIR /interpol

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "main.py"]


# App: Flask
FROM python:3.8

COPY flaskr /flaskr

WORKDIR /flaskr

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main.py", "app.py"]




