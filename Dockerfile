FROM python:3.12

ENV PORT=8080

RUN adduser note_api
USER note_api

RUN pip install --upgrade pip
ENV PATH="/home/note_api/.local/bin:${PATH}"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./note_api /code/note_api

CMD ["bash", "-c", "uvicorn note_api.main:app --host 0.0.0.0 --port ${PORT}"]