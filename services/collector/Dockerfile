# We use Alpine because it is TINY (around 5MB) - Great for your RAM!
FROM python:3.9-alpine

# Create a folder for our code
WORKDIR /app

# Copy the requirements file first (this makes building faster)
COPY requirements.txt .

# Install dependencies (none for now, but we create the command)
RUN pip install --no-cache-dir -r requirements.txt

# Copy our script
COPY src/ ./src/

# Run the script
CMD ["python", "src/main.py"]