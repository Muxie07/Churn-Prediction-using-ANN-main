# Churn Prediction Engine - Full Integration Guide

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React Frontend                           │
│                  (localhost:5173)                           │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • GaugeChart: Churn probability visualization      │    │
│  │ • InputMatrix: Parameter input grid                 │    │
│  │ • ModelStatus: Live metrics display                 │    │
│  │ • ActionCard: Risk recommendations                  │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                   │
│               HTTP Requests (Axios)                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ POST /api/predict
                         │ {age, gender, city_tier, ...}
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Bridge                             │
│              (localhost:8000) - CORS Enabled                │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ • Request validation & encoding                    │    │
│  │ • Feature transformation & scaling                 │    │
│  │ • Model inference (CatBoost)                       │    │
│  │ • SHAP interpretability (optional)                 │    │
│  │ • Response formatting & risk scoring               │    │
│  └─────────────────────────────────────────────────────┘    │
│                          ▼                                   │
│        JSON Response {churn_prob, risk_level, ...}          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────┐
        │   CatBoost Model                 │
        │  (best_model.cbm)                │
        │  Input: [17 features]            │
        │  Output: [0-1] probability       │
        └──────────────────────────────────┘
```

---

## 📋 Prerequisites

### Global Dependencies
- **Node.js**: 16.x or higher (includes npm)
- **Python**: 3.8 or higher
- **Git**: For version control

### Check Installation
```bash
node --version  # Should be v16+
npm --version   # Should be 7+
python --version  # Should be 3.8+
```

---

## 🚀 Setup Instructions

### Step 1: Backend Setup (FastAPI)

#### 1a. Install Python Dependencies

```bash
pip install fastapi uvicorn catboost scikit-learn pandas numpy shap
```

Or use the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

#### 1b. Verify Model Files

Ensure these files exist in the root directory:
- `best_model.cbm` - Trained CatBoost model
- `scalerpkl.ipynb` - MinMaxScaler object

#### 1c. Start FastAPI Server

```bash
python fastapi_bridge.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

Verify it's running:
```bash
curl http://localhost:8000/health
# Response: {"status":"operational","model_loaded":true,"service":"Churn Prediction Engine"}
```

### Step 2: Frontend Setup (React)

#### 2a. Navigate to Frontend Directory

```bash
cd frontend
```

#### 2b. Install Dependencies

```bash
npm install
```

This installs all packages defined in `package.json` (React, Vite, Tailwind, Lucide, Recharts, Axios, etc.)

#### 2c. Start Development Server

```bash
npm run dev
```

Expected output:
```
VITE v5.0.8  ready in 123 ms

➜  Local:   http://localhost:5173/
➜  press h to show help
```

#### 2d. Open in Browser

Navigate to `http://localhost:5173` - You should see the dashboard with:
- Gradient header "Churn Prediction Engine"
- Model Status panel
- Gauge chart (0% initially)
- Input matrix with parameter sliders
- Feature impact bar chart
- Action card with risk recommendations

---

## 🔄 API Communication

### Request Flow

1. **User enters parameters** in InputMatrix component
2. **React sends POST request** to `http://localhost:8000/api/predict`
3. **FastAPI server**:
   - Validates input data
   - Encodes categorical variables (Gender → 1/2/3)
   - Scales numeric features using MinMaxScaler
   - Calls CatBoost model for inference
   - Calculates risk level (low/medium/high)
   - Returns structured JSON response
4. **React receives response** and updates UI:
   - GaugeChart animates to new probability
   - ActionCard updates with recommendations
   - ModelStatus shows latency

### Example API Call

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "gender": "Male",
    "city_tier": "Tier 1",
    "tenure": 72,
    "login_device": "Mobile",
    "warehouse_distance": 50,
    "category": "Electronics",
    "satisfaction": 3,
    "address_count": 3,
    "order_hike_pct": 15.0,
    "coupon_used": "No",
    "days_since_order": 30,
    "cashback": 500.0
  }'
```

**Response:**
```json
{
  "churn_probability": 0.42,
  "risk_level": "low",
  "risk_color": "#10b981",
  "features_impact": [
    {"name": "Satisfaction Score", "value": 28, "color": "from-indigo-500 to-cyan-400"},
    {"name": "Days Since Last Order", "value": 22, "color": "from-violet-500 to-indigo-400"},
    {"name": "Cashback Amount", "value": 15, "color": "from-cyan-400 to-blue-500"}
  ],
  "confidence": 94.0
}
```

---

## 🛠 Configuration

### FastAPI Configuration

Edit `fastapi_bridge.py` to:

**Change Server Port:**
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)  # Changed from 8000
```

**Modify CORS Allowed Origins:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://yourdomain.com",  # Add production domain
        "https://app.example.com"
    ],
)
```

**Change Model Path:**
```python
model.load_model('path/to/custom_model.cbm')
with open('path/to/custom_scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)
```

### React Configuration

Edit `frontend/vite.config.js` to update API endpoint:

```javascript
proxy: {
  '/api': {
    target: 'http://localhost:9000',  // Match FastAPI port
    changeOrigin: true,
  }
}
```

Or use environment variable in React components:

```javascript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const response = await axios.post(`${API_URL}/api/predict`, data);
```

---

## 🧪 Testing

### Test API Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Feature reference
curl http://localhost:8000/api/feature-reference

# Interactive docs (Swagger UI)
http://localhost:8000/docs
```

### Test React Component Integration

In `frontend/src/App.jsx`, check browser console for network requests:

1. Open Developer Tools (F12)
2. Go to Network tab
3. Click "Run Prediction" button
4. Should see POST request to `/api/predict`
5. Check response in Preview/Response tab

### Debug Mode

**FastAPI:** Add verbose logging in `fastapi_bridge.py`
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**React:** Add console logs in `App.jsx`
```jsx
const handlePredict = async () => {
  console.log('Input values:', inputs);
  const response = await axios.post('/api/predict', inputs);
  console.log('API Response:', response.data);
  setChurnProb(response.data.churn_probability * 100);
};
```

---

## 📊 Example Workflows

### Workflow 1: Single Customer Prediction

1. User opens React app at `http://localhost:5173`
2. Enters customer parameters in InputMatrix
3. Clicks "Run Prediction" button
4. GaugeChart animates to churn probability
5. ActionCard shows personalized recommendations
6. Feature Impact chart displays top 5 contributing factors

### Workflow 2: Batch Predictions

```bash
# Use FastAPI batch endpoint
POST /api/batch-predict
Content-Type: application/json

[
  {"age": 25, "gender": "Female", ...},
  {"age": 45, "gender": "Male", ...},
  ...
]

# Response: 100 predictions with individual probabilities
```

### Workflow 3: Model Monitoring

Monitor model performance via:
```bash
# Check API health
curl http://localhost:8000/health

# View feature schema
curl http://localhost:8000/api/feature-reference

# Logs in FastAPI terminal show inference details
```

---

## 🚀 Deployment

### Development
```bash
# Terminal 1: FastAPI backend
python fastapi_bridge.py

# Terminal 2: React frontend
cd frontend && npm run dev
```

### Production

#### Backend (FastAPI)

**Using Gunicorn + Uvicorn:**
```bash
pip install gunicorn

gunicorn fastapi_bridge:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

**Using Docker:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "fastapi_bridge:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t churn-api .
docker run -p 8000:8000 churn-api
```

#### Frontend (React)

**Build for Production:**
```bash
cd frontend
npm run build

# Output in frontend/dist/ - ready for static hosting
```

**Deploy to Netlify:**
```bash
npm install -g netlify-cli
netlify deploy --prod --dir=frontend/dist
```

**Deploy to Vercel:**
```bash
npm install -g vercel
vercel --prod
```

**Using Docker:**
```dockerfile
FROM node:18-alpine AS build

WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
RUN npm run build

FROM node:18-alpine

WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist ./dist

EXPOSE 3000
CMD ["serve", "-s", "dist"]
```

---

## 🔐 Security Considerations

### CORS Security
Currently, CORS allows localhost only. For production:

```python
# In fastapi_bridge.py
origins = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    # NO wildcards for production!
]

app.add_middleware(CORSMiddleware, allow_origins=origins)
```

### Input Validation
FastAPI automatically validates against `PredictionRequest` schema. Accepts only valid types and ranges.

### Environment Variables
**Backend:**
```bash
export MODEL_PATH=path/to/model.cbm
export SCALER_PATH=path/to/scaler.pkl
export ALLOWED_ORIGINS=https://yourdomain.com
```

**Frontend:**
```bash
VITE_API_URL=https://api.yourdomain.com
VITE_ENV=production
```

### Rate Limiting
Add to `fastapi_bridge.py`:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address
