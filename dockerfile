# Stage 1: Build React frontend
FROM node:14-alpine as frontend-build
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

# Ensure App.js and other necessary files are included in build
RUN cp -r src/. build/

# Stage 2: Set up Python backend
FROM python:3.9-slim
WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install -r requirements.txt

# Copy backend code
COPY backend/ backend/

# Copy built React files into Flask static directory
COPY --from=frontend-build /app/frontend/build /app/backend/static

# Set working directory for backend
WORKDIR /app/backend

# Expose port 5000 (or the port your Flask app runs on)
EXPOSE 5000

# Command to run the Flask app with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
