FROM python:3.9-slim

WORKDIR /app

# Copy the current directory contents into the container.
COPY ./main.py /app
COPY ./requirements.txt /app

# Install the required packages.
RUN pip install -r requirements.txt

# Make port 8080 available to the world outside this container.
EXPOSE 8080

# Run the Flask app.
CMD ["python", "main.py"]
