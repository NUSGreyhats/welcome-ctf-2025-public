FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt /app
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY templates/index.html /app/templates/
COPY app.py /app/

COPY flag.txt /flag.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]
