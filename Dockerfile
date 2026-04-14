FROM python:3.12-slim

WORKDIR /app

# Copy requirement files and install dependencies
# We will use a requirements.txt file. Create one with `pip freeze > requirements.txt`
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port uvicorn runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]