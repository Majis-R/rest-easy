# rest-easy
A demonstration of a secure RESTful API

python -m uvicorn app.main:app --reload
docker compose up -d db

Open https://127.0.0.1:8000/test-ui for a browser-based tester for account and chat endpoints.