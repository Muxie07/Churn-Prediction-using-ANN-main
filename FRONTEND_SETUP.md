# Churn Prediction Engine - React Frontend

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ with npm
- Python 3.8+ with the Streamlit backend running (optional)

### Installation

```bash
cd frontend
npm install
```

### Development Mode

```bash
npm run dev
```
This starts the Vite dev server at `http://localhost:5173` with hot module reloading.

### Production Build

```bash
npm run build
```

Output will be in the `frontend/dist` directory, ready for deployment.

---

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable UI components
│   │   ├── GaugeChart.jsx          # SVG circular progress gauge
│   │   ├── InputMatrix.jsx         # Parameter input grid (4 categories)
│   │   ├── ModelStatus.jsx         # Live model metrics display
│   │   └── ActionCard.jsx          # AI recommendation card with risk alert
│   ├── App.jsx          # Main application component
│   ├── index.jsx        # React entry point
│   └── index.css        # Global styles + Tailwind
├── index.html           # HTML entry point
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind CSS customization
├── postcss.config.js    # PostCSS configuration
└── package.json         # Dependencies & scripts
```

---

## 🎨 Design System

### Color Palette
- **Background**: `#0f172a` (slate-950)
- **Primary**: `#818cf8` (indigo-400)
- **Secondary**: `#22d3ee` (cyan-400)
- **Tertiary**: `#a78bfa` (violet-400)
- **Risk - Low**: `#10b981` (emerald-400)
- **Risk - Medium**: `#f59e0b` (amber-400)
- **Risk - High**: `#ef4444` (red-500)

### Visual Style
- **Theme**: Glassmorphism with backdrop blur
- **Radius**: 3xl (36px) for primary cards, 2xl (16px) for inputs
- **Borders**: Subtle indigo/cyan with transparency, hover-active states
- **Shadows**: Custom glow effects for depth
- **Typography**: Inter font, gradient text for headers
- **Animations**: Smooth transitions (300ms), pulse pulse indicators, scale-on-hover

---

## 🧩 Components

### GaugeChart
**Purpose**: Visual representation of churn probability (0-100%)

**Props**:
- `value` (number): Churn probability (0-100)

**Features**:
- Dynamic gradient fill: green (0%) → amber (50%) → red (100%)
- Smooth SVG stroke animation
- Center percentage display
- Glow filter for neon effect

**Usage**:
```jsx
<GaugeChart value={churnProb} />
```

### InputMatrix
**Purpose**: Comprehensive parameter input form with 4 categories

**Props**:
- `onInputChange` (function): Callback when inputs change
- `onPredict` (function): Callback when Predict button clicked
- `loading` (boolean): Show loading state

**Categories**:
1. **Demographics**: Age, Gender, City Tier
2. **Account**: Tenure, Preferred Device, Warehouse Distance
3. **Behavioral**: Satisfaction, Order Category, Addresses
4. **Financial**: Order Amount Hike %, Coupon Used, Days Since Last Order, Cashback Amount

**Features**:
- Range sliders with gradient track
- Select dropdowns with custom styling
- Gradient button with Zap icon
- Glassmorphism card design

**Usage**:
```jsx
<InputMatrix 
  onInputChange={setInputs}
  onPredict={handlePredict}
  loading={loading}
/>
```

### ModelStatus
**Purpose**: Display live model performance metrics

**Props**:
- `latency` (number): Response time in milliseconds (default: 24)
- `modelVersion` (string): Model identifier (default: "CatBoost-v4")
- `status` (string): "Online" or "Offline" (default: "Online")

**Features**:
- Animated pulse indicator dot
- Real-time status updates
- Performance confidence bar
- Color-coded status (green/red)

**Usage**:
```jsx
<ModelStatus latency={24} modelVersion="CatBoost-v4" status="Online" />
```

### ActionCard
**Purpose**: AI-powered recommendation card with contextual alerts

**Props**:
- `churnProbability` (number): Churn probability 0-1 (default: 0.45)
- `riskLevel` (string): "low", "medium", or "high" (auto-calculated if not provided)

**Risk Levels**:
- **Low** (< 40%): Green theme, "retention strong" message
- **Medium** (40-70%): Amber theme, "engagement improvement" message
- **High** (> 70%): Red theme, "critical alert" with glow effects

**Features**:
- Dynamic background gradient based on risk
- Conditional "Send Offer" button for high risk
- Probability progress bar with gradient fill
- Action recommendations based on risk level
- Shadow glow effect intensifies at high risk

**Usage**:
```jsx
<ActionCard churnProbability={0.42} riskLevel="low" />
```

---

## 🔗 API Integration

### Expected Backend Endpoint

The React app expects a backend API at `http://localhost:8000/api/predict`

**Request**:
```json
POST /api/predict
{
  "age": 35,
  "gender": "Male",
  "city_tier": "Tier 1",
  "tenure": 72,
  "login_device": "Mobile",
  "warehouse_distance": 50,
  "category": "Electronics",
  "satisfaction": 3,
  "addresses": 3,
  "order_hike_pct": 15,
  "coupon_used": "No",
  "days_since_order": 30,
  "cashback": 500
}
```

**Response**:
```json
{
  "churn_probability": 0.42,
  "risk_level": "low",
  "features_impact": [
    { "name": "Satisfaction Score", "value": 28 },
    { "name": "Days Since Last Order", "value": 22 },
    { "name": "Cashback Amount", "value": 15 }
  ]
}
```

### Vite Proxy Configuration
The `vite.config.js` automatically proxies `/api/` requests to `http://localhost:8000` during development.

To connect with Streamlit backend:
1. Ensure Streamlit app is running: `streamlit run churn_app_develop.py`
2. Or wrap with FastAPI for proper CORS:

```python
# fastapi_bridge.py example
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/predict")
async def predict(data: dict):
    # Call Streamlit backend or model directly
    # Return prediction results
    pass
```

---

## 🛠 Customization

### Modifying Colors
Edit `tailwind.config.js`:
```javascript
extend: {
  colors: {
    indigo: { 400: '#818cf8' },
    cyan: { 400: '#22d3ee' },
    // ... add custom colors
  }
}
```

### Adding New Input Parameters
Edit `frontend/src/components/InputMatrix.jsx`:
```javascript
const categories = {
  YourCategory: [
    { label: 'Your Field', type: 'range', min: 0, max: 100, default: 50 },
    // ... add more fields
  ]
}
```

### Styling Changes
- Global styles: `src/index.css`
- Component styles: Inline Tailwind classes in JSX
- Theme tokens: `tailwind.config.js`

---

## 📦 Dependencies

- **React 18**: UI framework
- **Vite 5**: Fast build tool
- **Tailwind CSS 3**: Utility-first styling
- **Lucide React**: Icon library with 300+ icons
- **Recharts 2**: Charts & visualizations
- **Axios**: HTTP client for API calls
- **PostCSS**: CSS transformation
- **Autoprefixer**: Browser prefix auto-insertion

---

## 🚢 Deployment

### Netlify
```bash
npm run build
# Deploy the dist/ folder
```

### Vercel
```bash
npm run build
# Connect your repo to Vercel dashboard
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

### Environment Variables
Create `.env.local`:
```env
VITE_API_URL=http://localhost:8000
VITE_ENV=development
```

---

## 🐛 Troubleshooting

**Q: Port 5173 already in use?**  
A: Change in `vite.config.js`: `port: 5174`

**Q: API calls failing with CORS error?**  
A: Ensure backend has CORS headers or use Vite proxy (configured in `vite.config.js`)

**Q: Styling looks broken?**  
A: Clear node_modules and reinstall:
```bash
rm -rf node_modules
npm install
npm run dev
```

**Q: Changes not reflecting?**  
A: Vite has hot module reloading. If stuck, restart dev server with Ctrl+C and `npm run dev`

---

## 📊 Performance Analytics

The ModelStatus component simulates:
- **Latency**: 24ms average (configurable)
- **Model Confidence**: 94% (mock value)
- **Status**: Live online indicator with pulse animation

For real metrics, connect to your monitoring backend (Prometheus, DataDog, etc.)

---

## ✨ Future Enhancements

- [ ] Real-time model updates via WebSockets
- [ ] Customer history timeline
- [ ] Batch prediction with CSV upload
- [ ] SHAP waterfall plot integration
- [ ] Multi-model comparison view
- [ ] Mobile app (React Native)
- [ ] Dark/Light theme toggle
- [ ] Accessibility audit (WCAG 2.1 AA)

---

## 📄 License

This project is part of the Churn Prediction Engine. See main README.md for license details.

---

**Last Updated**: December 2024  
**Maintained By**: AI Development Team  
**React Version**: 18.2+ | Vite: 5.0+ | Node: 16+
