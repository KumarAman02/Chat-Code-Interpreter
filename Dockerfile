# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /chat-code-interpreter

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port that the application will run on
EXPOSE 8000

# Run the application with Chainlit
CMD ["chainlit", "run", "app.py", "-h", "0.0.0.0", "-p", "8000"]
