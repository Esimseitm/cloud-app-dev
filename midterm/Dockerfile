FROM python:3.9-slim

WORKDIR /app

COPY ./main.py /app
COPY ./requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8080

# Run the Flask app.
CMD ["python", "main.py"]
