# syntax=docker/dockerfile:1
FROM python:3.11.0-slim-buster
WORKDIR /source
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80
COPY /prpdf $WORKDIR
RUN apt-get update && apt-get install tesseract-ocr poppler-utils tesseract-ocr-deu -y
RUN pip3 install -r $WORKDIR/requirements.txt
CMD ["flask", "run"]
