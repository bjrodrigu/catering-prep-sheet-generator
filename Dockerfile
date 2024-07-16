# Frontend build stage
FROM node:16 as frontend-builder
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# Backend build stage
FROM python:3.9-slim
WORKDIR /app

# Install backend dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY backend/ ./

# Copy built frontend files to backend's static folder
COPY --from=frontend-builder /app/build ./static

# Expose the backend port
EXPOSE 2003

# Start the backend server
CMD ["python", "app.py"]
