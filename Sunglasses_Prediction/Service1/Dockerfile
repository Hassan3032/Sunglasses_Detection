FROM python:3.11.4

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /Service1

WORKDIR /Service1

EXPOSE 5001

CMD ["python", "app1.py"]

