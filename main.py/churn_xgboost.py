import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score

# 1. Load your dataset
# Make sure data_ecommerce_customer_churn.csv is in the same folder!
dataset = pd.read_csv('data_ecommerce_customer_churn.csv')

# 2. Handle Missing Values
dataset = dataset.fillna(0)

# 3. Separate Features and Target
X = dataset.drop('Churn', axis=1)
y = dataset['Churn']

# 4. Convert ALL text columns to numbers (The "XGBoost way")
# This converts columns like 'PreferedOrderCat' and 'MaritalStatus' into numeric columns automatically
X = pd.get_dummies(X)

# 5. Ensure all data is float (This prevents the 'str' error for good)
X = X.astype(float)

# 6. Split Data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = xgb.XGBClassifier(n_estimators=100, learning_rate=0.1, max_depth=5)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, predictions) * 100:.2f}%")