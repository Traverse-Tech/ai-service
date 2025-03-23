FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 50051

CMD ["python", "grpc_server.py"]