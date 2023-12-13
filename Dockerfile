# Use an official Python image as the base image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory 
COPY requirements.txt .

# Install any dependencies
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the content of the local src directory to the working directory
COPY . .

# Declare the port number the container should expose
EXPOSE 80 

# Run the application
CMD ["python", "app.py"]