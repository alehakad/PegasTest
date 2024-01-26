FROM python:3.10.6-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

RUN apt-get update && apt-get -y install libpq-dev gcc
# Install the requirements
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

ENV PYTHONDONTWRITEBYTECODE 1
# Copy the source code
COPY . .

# Run the application
CMD python main_bot.py