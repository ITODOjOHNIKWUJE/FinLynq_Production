# FinLynq Working Code (Minimal)

This package contains a minimal working backend (FastAPI) and a simple Expo React Native app that demonstrates register/login and wallet balance.

## Backend
- Option 1 (Docker): docker compose up --build
- Option 2 (local):
  cd backend
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  uvicorn app.main:app --reload --port 8000

## Mobile
- Install Expo CLI: npm install -g expo-cli
- cd mobile_app
- npm install
- expo start

Note: For Android emulator use API_URL = http://10.0.2.2:8000 in App.js. For web or iOS simulator use http://localhost:8000
