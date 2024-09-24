FROM python:3.8.10

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    ca-certificates


WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
# Copy the rest of the application code
COPY . .

# Ensure OpenCV is installed
RUN pip install opencv-python-headless

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]