.PHONY: start-backend start-frontend start

start-backend:
	cd backend/ && python server.py &

start-frontend:
	cd frontend/ && npm start &

start: start-backend start-frontend

