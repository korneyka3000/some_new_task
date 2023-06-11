FROM python:3.10

WORKDIR APP

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD python -m uvicorn run:server --reload --host 0.0.0.0 --port 8000