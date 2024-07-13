FROM opensora:latest

# Install Flask
RUN pip install Flask

# Copy the Flask API server script
COPY api_server.py .

# Set the environment variable for save directory
ENV SAVE_DIR="/home/ubuntu/data"

# Expose the port the API server will run on
EXPOSE 5000

# Run the API server
CMD ["python", "api_server.py"]
