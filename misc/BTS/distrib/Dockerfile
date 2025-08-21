FROM python:3.13-slim

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home appuser

WORKDIR /home/appuser

COPY main.py .

RUN chown -R appuser:appuser /home/appuser
RUN chmod +x main.py
USER appuser

EXPOSE 5000

CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:'python main.py'"]