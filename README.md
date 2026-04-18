# 🤖 IDRMS-AI — Flood Risk Prediction Service
### Barangay Kauswagan, Cagayan de Oro

This is the **FastAPI AI service** for the IDRMS (Integrated Disaster Risk Management System).  
It predicts flood risk per zone using historical incident data from the Django backend.

---

## 📁 Project Structure
```
idrms-ai/
├── main.py                  ← FastAPI entry point
├── .env                     ← Your environment variables (create this manually!)
├── requirements.txt         ← Python packages needed
│
├── core/
│   ├── __init__.py
│   └── config.py            ← Reads settings from .env
│
├── routers/
│   ├── __init__.py
│   └── flood.py             ← All /ai/flood/* API endpoints
│
├── services/
│   ├── __init__.py
│   ├── django_client.py     ← Connects to Django backend
│   └── flood_ai.py          ← AI flood prediction logic
│
├── schemas/
│   ├── __init__.py
│   └── flood.py             ← Response data shapes
│
└── snippets/
    ├── MapPage_integration.js    ← Guide for web MapPage.jsx
    └── MapScreen_integration.js  ← Guide for mobile MapScreen.js
```

---

## 🔗 How It Connects

```
📱 Mobile App (idrms_MobApp)
        ↓ fetch
🤖 FastAPI AI (this project) — port 8001
        ↓ fetch
🌐 Django Backend (lab8-backend) — ngrok URL
        ↓
🗄️ Database
        
💻 Web App (idrms-lab5)
        ↓ fetch
🤖 FastAPI AI (this project) — port 8001
```

---

## ⚙️ Setup Guide (Do this once!)

### ✅ Requirements
- Python 3.10 or higher installed
- Git installed
- ngrok installed (for exposing to mobile/web)

---

### Step 1 — Clone the repository
```bash
git clone https://github.com/trishaguangco428-creator/idrmc-ai.git
```

### Step 2 — Go into the project folder
```bash
cd idrmc-ai
```

### Step 3 — Create virtual environment
```bash
python -m venv venv
```

### Step 4 — Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line ✅

### Step 5 — Install all packages
```bash
pip install -r requirements.txt
```

### Step 6 — Create your `.env` file
Create a new file called `.env` in the root folder and paste this:
```
DJANGO_API_URL=https://julianna-unblossomed-zahra.ngrok-free.dev
PORT=8001
DEBUG=True
```

> ⚠️ **Important:** Replace the URL with the actual Django ngrok URL if it has changed!  
> ⚠️ **Never push `.env` to GitHub!** It contains secret URLs.

---

## ▶️ Running the Server

### Step 1 — Make sure venv is active
```bash
venv\Scripts\activate
```

### Step 2 — Run FastAPI
```bash
python -m uvicorn main:app --reload --port 8001
```

### Step 3 — You should see this:
```
🚀 IDRMS AI running on port 8001
📡 Django: https://julianna-unblossomed-zahra.ngrok-free.dev
INFO:     Uvicorn running on http://127.0.0.1:8001
INFO:     Application startup complete.
```

### Step 4 — Open Swagger docs in browser
```
http://localhost:8001/docs
```

You will see all available API endpoints! ✅

---

## 🌐 Exposing FastAPI with ngrok

To connect web and mobile apps, you need to expose port 8001 using ngrok.

### Open a NEW terminal (keep FastAPI running!) and run:
```bash
ngrok http 8001
```

### You will get a URL like:
```
https://xxxx-your-url.ngrok-free.app
```

### Use this URL in:
- `idrms-lab5/src/pages/MapPage.jsx` → see `snippets/MapPage_integration.js`
- `idrms_MobApp/src/screens/MapScreen.js` → see `snippets/MapScreen_integration.js`

---

## 📡 API Endpoints

| Method | Endpoint | Description | Used By |
|--------|----------|-------------|---------|
| GET | `/` | Service info | Anyone |
| GET | `/health` | Health check | Anyone |
| GET | `/ai/flood/heatmap` | Flood heatmap for all 6 zones | MapPage.jsx, MapScreen.js |
| GET | `/ai/flood/summary` | Ranked flood risk summary | Dashboard, Reports |
| POST | `/ai/flood/predict` | Predict risk for specific zone | RiskScreen, RiskIntelligencePage |

---

## 🧪 Testing the Endpoints

### Test heatmap:
1. Go to `http://localhost:8001/docs`
2. Click `GET /ai/flood/heatmap`
3. Click **Try it out**
4. Click **Execute**
5. You should see flood risk data for all 6 zones!

### Test predict:
1. Click `POST /ai/flood/predict`
2. Click **Try it out**
3. Paste this in the body:
```json
{
  "zone": "Zone 3",
  "severity": "High",
  "month": 8
}
```
4. Click **Execute**
5. You should see predicted risk level and recommendation!

---

## 🗺️ Connecting to Web App (MapPage.jsx)

Open `idrms-lab5/src/pages/MapPage.jsx` and follow the steps in:
```
snippets/MapPage_integration.js
```

---

## 📱 Connecting to Mobile App (MapScreen.js)

Open `idrms_MobApp/src/screens/MapScreen.js` and follow the steps in:
```
snippets/MapScreen_integration.js
```

---

## 🤝 Collaboration Guide

### Before starting work — always pull first!
```bash
git pull
```

### After finishing work — push your changes!
```bash
git status
git add .
git commit -m "feat: describe what you changed"
git push
```

### Commit message format:
```bash
git commit -m "feat: add new feature"
git commit -m "fix: fix a bug"
git commit -m "refactor: clean up code"
git commit -m "docs: update README"
```

---

## ⚠️ Common Problems & Fixes

### ❌ Problem: `ModuleNotFoundError`
```bash
pip install -r requirements.txt
```

### ❌ Problem: `Cannot reach Django`
- Check if Django backend is running
- Check if ngrok URL in `.env` is correct and still active

### ❌ Problem: `venv not activated`
```bash
venv\Scripts\activate
```

### ❌ Problem: Push rejected
```bash
git pull
git push
```

### ❌ Problem: Port 8001 already in use
```bash
# Windows — find and kill the process
netstat -ano | findstr :8001
taskkill /PID <PID_NUMBER> /F
```

### ❌ Problem: `core` folder missing (OneDrive issue)
```bash
New-Item -ItemType Directory -Path core
New-Item -ItemType File -Path core\__init__.py
New-Item -ItemType File -Path core\config.py
```
Then paste the config code again!

---

## 🌊 How the AI Works

```
1. Fetches all incidents from Django backend
2. Filters only Flood type incidents
3. Calculates score per zone:
   - Base score (from constants)
   - + Severity weight (Low=1, Medium=2, High=3)
   - + Rainy season bonus (June-November)
   - + Dynamic score from incident history
4. Normalizes scores to 0.0-1.0 for heatmap
5. Returns risk level per zone:
   - 🔴 High  = score >= 65
   - 🟡 Medium = score >= 35
   - 🟢 Low   = score < 35
```

---

## 📊 Zone Base Scores

| Zone | Base Score | Primary Hazard |
|------|-----------|----------------|
| Zone 1 | 25 | Fire |
| Zone 2 | 42 | Flood |
| Zone 3 | 78 | Flood |
| Zone 4 | 18 | Storm |
| Zone 5 | 82 | Landslide |
| Zone 6 | 48 | Storm |

---

## 👥 Team

| Name | Role |
|------|------|
| Trisha | FastAPI AI Service |
| Friend | Web & Mobile Integration |

---

## 📝 Notes

- FastAPI runs on port **8001**
- Django runs on port **8000**
- Always create your own `.env` file — never share it!
- Always activate `venv` before running the server
- The `snippets/` folder contains integration guides for web and mobile

---

*IDRMS — Integrated Disaster Risk Management System*  
*Barangay Kauswagan, Cagayan de Oro City*
