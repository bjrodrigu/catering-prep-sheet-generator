# Stage 1: Build the React frontend
FROM node:14 AS frontend-builder

WORKDIR /app/frontend

# Copy the frontend files and install dependencies
COPY frontend/package*.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build

# Stage 2: Build the Flask backend
FROM python:3.9 AS backend-builder

WORKDIR /app/backend

# Copy the backend files and install dependencies
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY backend/ ./

# Copy the built frontend from Stage 1 to the backend's static files directory
COPY --from=frontend-builder /app/frontend/build /app/backend/static

# Stage 3: Final image to run the application
FROM python:3.9

WORKDIR /app

# Copy the backend files
COPY --from=backend-builder /app/backend /app

# Expose the necessary ports
EXPOSE 2003

# Command to run Gunicorn with the Flask application
CMD ["gunicorn", "-b", "0.0.0.0:2003", "app:app"]
