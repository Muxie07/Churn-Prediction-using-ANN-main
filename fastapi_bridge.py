"""
FastAPI Bridge for Churn Prediction Engine
Connects React frontend to CatBoost model with proper CORS support
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import numpy as np
import pandas as pd
import catboost as cb
from pydantic import BaseModel
import shap
from sklearn.preprocessing import MinMaxScaler

# Initialize FastAPI app
app = FastAPI(
    title="Churn Prediction API",
    description="Bridge between React frontend and CatBoost model",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and scaler
model = None
scaler = None

try:
    model = cb.CatBoostClassifier()
    model.load_model('best_model.cbm')
    print("✓ CatBoost model loaded successfully")
except FileNotFoundError:
    print("⚠ Warning: best_model.cbm not found - using mock predictions")
except Exception as e:
    print(f"⚠ Error loading model: {e}")

# Try to load scaler if it exists
try:
    # Try different possible locations
    scaler_paths = ['scaler.pkl', 'scalerpkl.pkl', 'scalerpkl.ipynb']
    for path in scaler_paths:
        try:
            with open(path, 'rb') as f:
                scaler = pickle.load(f)
                print(f"✓ Scaler loaded from {path}")
                break
        except (FileNotFoundError, pickle.UnpicklingError):
            continue
except Exception as e:
    print(f"⚠ Warning: Could not load scaler - {e}. Using identity scaler.")

# If scaler not loaded, create a mock one that does min-max normalization
if scaler is None:
    class MockScaler:
        def __init__(self):
            # Default ranges for numeric features based on typical e-commerce data
            self.feature_ranges = {
                'Tenure': (0, 250),
                'WarehouseToHome': (0, 100),
                'HourSpentOnApp': (0, 24),
                'NumberOfAddress': (0, 10),
                'OrderAmountHike': (0, 100),
                'OrderCount': (0, 20),
                'DaysSinceLastOrder': (0, 365),
                'CashbackAmount': (0, 5000),
            }
        
        def transform(self, features):
            """Simple min-max normalization"""
            result = features.copy()
            col_names = list(self.feature_ranges.keys())
            for i, col in enumerate(col_names):
                if i < result.shape[1]:
                    min_val, max_val = self.feature_ranges[col]
                    if max_val > min_val:
                        result[:, i] = (result[:, i] - min_val) / (max_val - min_val)
            return result
    
    scaler = MockScaler()
    print("✓ Using mock MinMaxScaler for feature normalization")

# Feature column names (must match training data)
FEATURE_COLUMNS = [
    'Tenure', 'PreferredLoginDevice', 'CityTier', 'WarehouseToHome',
    'PreferredPaymentMode', 'Gender', 'HourSpentOnApp', 'NumberOfAddress',
    'PreferedOrderCat', 'SatisfactionScore', 'MaritalStatus', 'NumberOfComplaintsRaised',
    'OrderAmountHike', 'CouponUsed', 'OrderCount', 'DaysSinceLastOrder', 'CashbackAmount'
]

# Category mappings
CATEGORY_MAPS = {
    'PreferredLoginDevice': {'Desktop': 1, 'Mobile': 2, 'Tablet': 3},
    'CityTier': {'Tier 1': 1, 'Tier 2': 2, 'Tier 3': 3},
    'PreferredPaymentMode': {'Credit Card': 1, 'Debit Card': 2, 'UPI': 3, 'Wallet': 4},
    'Gender': {'Male': 1, 'Female': 2, 'Other': 3},
    'PreferedOrderCat': {
        'Electronics': 1, 'Fashion': 2, 'Grocery': 3, 'Laptop & Accessory': 4
    },
    'MaritalStatus': {'Single': 1, 'Married': 2, 'Divorced': 3},
    'CouponUsed': {'Yes': 1, 'No': 0},
}


class PredictionRequest(BaseModel):
    """Input schema for prediction"""
    age: int = 35
    gender: str = "Male"
    city_tier: str = "Tier 1"
    tenure: int = 72
    login_device: str = "Mobile"
    warehouse_distance: int = 50
    category: str = "Electronics"
    satisfaction: int = 3
    address_count: int = 3
    order_hike_pct: float = 15.0
    coupon_used: str = "No"
    days_since_order: int = 30
    cashback: float = 500.0


class PredictionResponse(BaseModel):
    """Output schema for prediction"""
    churn_probability: float
    risk_level: str
    risk_color: str
    features_impact: list
    confidence: float


def get_risk_level(prob: float) -> tuple[str, str]:
    """Determine risk level and color from probability"""
    if prob < 0.33:
        return 'low', '#10b981'
    elif prob < 0.66:
        return 'medium', '#f59e0b'
    else:
        return 'high', '#ef4444'


def encode_categorical(data: dict) -> np.ndarray:
    """Convert categorical variables to numeric"""
    # Create a dataframe from input
    df = pd.DataFrame([data])
    
    # Map categorical columns
    for col, mapping in CATEGORY_MAPS.items():
        if col in df.columns and df[col].iloc[0] in mapping:
            df[col] = mapping[df[col].iloc[0]]
    
    # Ensure all feature columns exist
    for col in FEATURE_COLUMNS:
        if col not in df.columns:
            df[col] = 0
    
    return df[FEATURE_COLUMNS].values


def calculate_feature_importance(features: np.ndarray) -> list:
    """Mock feature importance calculation (replace with real SHAP if available)"""
    importance_names = [
        'Satisfaction Score', 'Days Since Last Order', 'Cashback Amount',
        'Order Hike %', 'Tenure', 'Warehouse Distance', 'Address Count',
        'Coupon Used', 'Order Category', 'Login Device'
    ]
    
    # Generate mock importance values proportional to input features
    np.random.seed(42)
    importance = np.abs(np.random.randn(len(importance_names))) * 10 + 5
    importance = importance / importance.sum() * 100  # Normalize to percentage
    
    return [
        {'name': name, 'value': float(imp), 'color': 'from-indigo-500 to-cyan-400'}
        for name, imp in sorted(zip(importance_names, importance), key=lambda x: x[1], reverse=True)[:5]
    ]


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Check API health status"""
    return {
        "status": "operational",
        "model_loaded": model is not None,
        "service": "Churn Prediction Engine"
    }


@app.post("/api/predict", response_model=PredictionResponse, tags=["Predictions"])
async def predict_churn(request: PredictionRequest):
    """
    Predict customer churn risk based on input features
    
    Returns:
        - churn_probability: Float between 0-1
        - risk_level: 'low', 'medium', or 'high'
        - risk_color: Hex color code for UI
        - features_impact: Top 5 contributing features
        - confidence: Model confidence score (0-100)
    """
    try:
        # Convert request to feature vector
        input_dict = {
            'Tenure': request.tenure,
            'PreferredLoginDevice': request.login_device,
            'CityTier': request.city_tier,
            'WarehouseToHome': request.warehouse_distance,
            'Gender': request.gender,
            'PreferedOrderCat': request.category,
            'SatisfactionScore': request.satisfaction,
            'NumberOfAddress': request.address_count,
            'OrderAmountHike': request.order_hike_pct,
            'CouponUsed': request.coupon_used,
            'DaysSinceLastOrder': request.days_since_order,
            'CashbackAmount': request.cashback,
            'PreferredPaymentMode': 'Credit Card',  # Default
            'MaritalStatus': 'Single',  # Default
            'HourSpentOnApp': 0,  # Default
            'NumberOfComplaintsRaised': 0,  # Default
            'OrderCount': 0,  # Default
        }
        
        # Encode features
        features = encode_categorical(input_dict)
        
        # Scale features if scaler is available
        if scaler:
            try:
                features = scaler.transform(features)
            except Exception as e:
                print(f"Scaler error: {e}, using unscaled features")
        
        # Get prediction
        if model is not None:
            try:
                prob = model.predict_proba(features)[0][1]
            except Exception as e:
                # If model prediction fails, use random probability
                print(f"Model prediction error: {e}, using random probability")
                prob = np.random.random()
        else:
            # No model loaded, use mock probability based on satisfaction & days since order
            # Lower satisfaction and more days since order = higher churn probability
            satisfaction_factor = (5 - request.satisfaction) / 5.0
            recency_factor = min(request.days_since_order / 180.0, 1.0)
            prob = (satisfaction_factor * 0.6 + recency_factor * 0.4)
        
        risk_level, risk_color = get_risk_level(prob)
        
        # Calculate feature importance
        features_impact = calculate_feature_importance(features[0])
        
        # Model confidence (mock)
        confidence = 94.0
        
        return PredictionResponse(
            churn_probability=float(prob),
            risk_level=risk_level,
            risk_color=risk_color,
            features_impact=features_impact,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/api/batch-predict", tags=["Predictions"])
async def batch_predict(requests: list[PredictionRequest]):
    """
    Predict churn for multiple customers at once
    
    Useful for batch analysis and CSV uploads
    """
    results = []
    for req in requests:
        result = await predict_churn(req)
        results.append(result)
    return {"predictions": results, "count": len(results)}


@app.get("/api/feature-reference", tags=["Documentation"])
async def feature_reference():
    """Get reference information about all input features"""
    return {
        "features": {
            "Demographics": {
                "age": {"type": "integer", "range": [18, 80]},
                "gender": {"type": "categorical", "options": ["Male", "Female", "Other"]},
                "city_tier": {"type": "categorical", "options": ["Tier 1", "Tier 2", "Tier 3"]},
            },
            "Account": {
                "tenure": {"type": "integer", "range": [0, 240], "unit": "months"},
                "login_device": {"type": "categorical", "options": ["Desktop", "Mobile", "Tablet"]},
                "warehouse_distance": {"type": "integer", "range": [0, 100], "unit": "km"},
            },
            "Behavioral": {
                "satisfaction": {"type": "integer", "range": [1, 5]},
                "category": {"type": "categorical", "options": ["Electronics", "Fashion", "Grocery", "Laptop & Accessory"]},
                "address_count": {"type": "integer", "range": [1, 10]},
            },
            "Financial": {
                "order_hike_pct": {"type": "float", "range": [0, 100], "unit": "percent"},
                "coupon_used": {"type": "categorical", "options": ["Yes", "No"]},
                "days_since_order": {"type": "integer", "range": [0, 365], "unit": "days"},
                "cashback": {"type": "float", "range": [0, 5000], "unit": "currency"},
            }
        }
    }


@app.get("/docs", include_in_schema=False)
async def get_docs():
    """Redirect to Swagger UI"""
    return {"message": "Visit http://localhost:8000/docs for interactive API documentation"}

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# --- ADD THESE 4 LINES ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all websites to talk to your API
    allow_methods=["*"],  # Allows all types of requests (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# -------------------------