FROM python:3.9-slim

WORKDIR /scraper-panamericana

COPY setup.py .
COPY src/ src/

RUN mkdir -p static/xlsx static/db

RUN pip install --upgrade pip \
    && pip install -e . \
    && rm -rf /root/.cache/pip

ENV PYTHONPATH="${PYTHONPATH}:/scraper-panamericana/src"

ENTRYPOINT ["python", "-m", "edu_pad.main"]