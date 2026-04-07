import numpy as np
import streamlit as st
import pickle
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from catboost import CatBoostClassifier

try:
    import shap
    import matplotlib.pyplot as plt
    SHAP_AVAILABLE = True
except ModuleNotFoundError:
    shap = None
    plt = None
    SHAP_AVAILABLE = False


def encode_cat_features(df):
    df_enc = df.copy()
    for col in df_enc.columns:
        if pd.api.types.is_numeric_dtype(df_enc[col]):
            continue
        # preserve missing values, encode categories to ints (compat with pandas without na_sentinel argument)
        codes, uniques = pd.factorize(df_enc[col].astype(str))
        df_enc[col] = codes
    return df_enc

st.set_page_config(
    page_title='E-commerce Churn Predictor',
    page_icon='📈',
    layout='wide',
    initial_sidebar_state='expanded',
)

st.markdown(
    '''
    <link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css' integrity='sha512-AKA7Xl1G4ya3HHwvMBSzc5LLNhjzmYvJZ5mA4jxuhs3qIlaQYhh+q9ZbXbp8jdF+Yt3lE4r49NdZuo5xg/WKtg==' crossorigin='anonymous' referrerpolicy='no-referrer' />
    <style>
    .stApp { background: #0b1223; color: #e3eafc; }
    .streamlit-expanderHeader, .stSidebar {
        color: #c3d0ff !important;
    }
    .stButton>button { background-color: #30418e; color: #ffffff; border-radius: 10px; }
    .stButton>button:hover { background-color: #4559ab; }
    .css-18e3th9, .stTextInput>div>input, .stNumberInput>div>input { background: #101a32 !important; color: #e4ebff !important; }
    .stMetric { background-color: #131c36 !important; color: #ecf0ff !important; }
    .stSidebar { background: linear-gradient(180deg, #101a32 0%, #13214a 100%); }
    </style>
    ''',
    unsafe_allow_html=True,
)

model = CatBoostClassifier()
model.load_model('best_model.cbm')
with open('scaler.pkl', 'rb') as fp:
    scaler = pickle.load(fp)

try:
    raw_df = pd.read_csv('data_ecommerce_customer_churn.csv')
except FileNotFoundError:
    raw_df = pd.DataFrame()

feature_names = [
    'Tenure', 'WarehouseToHome', 'NumberOfDeviceRegistered', 'PreferedOrderCat',
    'SatisfactionScore', 'MaritalStatus', 'NumberOfAddress', 'Complain',
    'DaySinceLastOrder', 'CashbackAmount'
]
scale_vars = ['Tenure', 'WarehouseToHome', 'NumberOfDeviceRegistered', 'SatisfactionScore', 'NumberOfAddress']

st.sidebar.markdown('## <i class="fas fa-user-cog"></i> Input Profile', unsafe_allow_html=True)
persona = st.sidebar.selectbox('Persona template', ['Balanced', 'At-risk', 'High-value', 'Recent-New'])

# New requested fields
age = st.sidebar.slider('Age', 18, 80, 30)
gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
city_tier = st.sidebar.selectbox('City Tier', ['Tier 1', 'Tier 2', 'Tier 3'])

login_device = st.sidebar.selectbox('Preferred Login Device', ['Desktop', 'Mobile', 'Tablet'])
order_amount_hike = st.sidebar.slider('Order Amount Hike (%)', 0, 100, 10)
coupon_used = st.sidebar.selectbox('Coupon Used', ['Yes', 'No'])

# Keep an analytic summary dataset (not all are model inputs)
user_profile_meta = {
    'Age': age,
    'Gender': gender,
    'CityTier': city_tier,
    'PreferredLoginDevice': login_device,
    'OrderAmountHikePct': order_amount_hike,
    'CouponUsed': 1 if coupon_used == 'Yes' else 0,
}

category_map = {
    'Electronics': 1,
    'Fashion': 2,
    'Grocery': 3,
    'Laptop & Accessory': 4
}

input_data = {
    'Tenure': st.sidebar.slider('Tenure (months)', 0, 240, 72),
    'WarehouseToHome': st.sidebar.slider('Warehouse to Home (%)', 0, 100, 50),
    'NumberOfDeviceRegistered': st.sidebar.slider('Devices Registered', 1, 50, 10),
    'PreferedOrderCat': category_map[st.sidebar.selectbox('Preferred Category', list(category_map.keys()))],
    'SatisfactionScore': st.sidebar.slider('Satisfaction Score', 1, 5, 3),
    'MaritalStatus': st.sidebar.selectbox('Marital Status', [0, 1], format_func=lambda x: 'Single' if x==0 else 'Married'),
    'NumberOfAddress': st.sidebar.slider('Address Count', 1, 10, 1),
    'Complain': st.sidebar.selectbox('Complaint Status', [0,1], format_func=lambda x: 'No' if x==0 else 'Yes'),
    'DaySinceLastOrder': st.sidebar.slider('Days Since Last Order', 0, 365, 30),
    'CashbackAmount': st.sidebar.slider('Cashback Amount', 0, 50000, 600, step=50),
}

if persona == 'At-risk':
    input_data.update({'Tenure': 15, 'SatisfactionScore': 1, 'DaySinceLastOrder': 170, 'Complain': 1, 'WarehouseToHome': 20})
elif persona == 'High-value':
    input_data.update({'Tenure': 190, 'SatisfactionScore': 5, 'NumberOfDeviceRegistered': 15, 'CashbackAmount': 2700, 'WarehouseToHome': 88})
elif persona == 'Recent-New':
    input_data.update({'Tenure': 3, 'DaySinceLastOrder': 6, 'NumberOfDeviceRegistered': 1, 'CashbackAmount': 100})

input_df = pd.DataFrame([input_data])
input_scaled = input_df.copy()
input_scaled[scale_vars] = scaler.transform(input_scaled[scale_vars])

# scale only numerical fields
input_scaled = input_df.copy()
input_scaled[scale_vars] = scaler.transform(input_scaled[scale_vars])

# Main content
st.markdown('<h1 style="color:#f9fbff"><i class="fas fa-chart-line"></i> E-commerce Customer Churn Predictor</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="color:#b3c2f5">Deep Indigo mode with interactive analytics, risk scoring and conditional insights.</h4>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

churn_rate = raw_df['Churn'].mean()*100 if not raw_df.empty and 'Churn' in raw_df.columns else 0
c1.metric('<i class="fas fa-exclamation-triangle"></i> Churn Rate', f'{churn_rate:.2f}%', delta='-1.5%')

sat_avg = raw_df['SatisfactionScore'].mean() if not raw_df.empty and 'SatisfactionScore' in raw_df.columns else 0
c2.metric('<i class="fas fa-smile"></i> Avg Satisfaction', f'{sat_avg:.2f}/5', delta='+0.8%')

gap = raw_df['DaySinceLastOrder'].mean() if not raw_df.empty and 'DaySinceLastOrder' in raw_df.columns else 0
c3.metric('<i class="fas fa-clock"></i> Avg Recency (days)', f'{gap:.0f}', delta='-2.1%')

with st.expander('<i class="fas fa-chart-bar"></i> Dataset Overview', expanded=True):
    if raw_df.empty:
        st.warning('dataset not loaded. Place data_ecommerce_customer_churn.csv in app directory.')
    else:
        r1, r2 = st.columns(2)
        r1.plotly_chart(px.histogram(raw_df, x='Churn', title='Churn Distribution', color='Churn', color_discrete_sequence=['#2f5dd4', '#e85f5f']), use_container_width=True)
        r2.plotly_chart(px.box(raw_df, x='Churn', y='SatisfactionScore', title='Satisfaction vs churn', color='Churn'), use_container_width=True)

        r3, r4 = st.columns(2)
        r3.plotly_chart(px.scatter(raw_df, x='DaySinceLastOrder', y='CashbackAmount', color='Churn', title='Recency vs Cashback'), use_container_width=True)
        if 'PreferedOrderCat' in raw_df.columns:
            df_cat = raw_df['PreferedOrderCat'].value_counts().reset_index(name='count').rename(columns={'PreferedOrderCat':'category'})
            r4.plotly_chart(px.bar(df_cat, x='category', y='count', title='Preferred order categories', color='category'), use_container_width=True)

def predict_churn(data):
    """Placeholder prediction function."""
    prob = float(model.predict_proba(data)[0][1])
    pred = int(model.predict(data)[0])
    return prob, pred

# Prediction
st.markdown('---')
if st.button('▶️ Predict churn risk'):
    with st.spinner('Predicting churn ...'):
        prob, pred = predict_churn(input_scaled)

    churn_pct = prob * 100
    if prob < 0.33:
        risk_level = 'Low Risk'
        risk_color = '#0ecb81'
    elif prob < 0.66:
        risk_level = 'Medium Risk'
        risk_color = '#f9a825'
    else:
        risk_level = 'High Risk'
        risk_color = '#ff4d4d'

    st.markdown(f'<h2 style="color:{risk_color};">{risk_level}</h2>', unsafe_allow_html=True)

    gauge = go.Figure(go.Indicator(
        mode='gauge+number',
        value=churn_pct,
        number={'suffix': '%'},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': risk_color},
            'steps': [
                {'range': [0, 33], 'color': '#1ae0bc'},
                {'range': [33, 66], 'color': '#f9a825'},
                {'range': [66, 100], 'color': '#ff4d4d'}
            ],
        },
        title={'text': 'Churn Probability', 'font': {'size': 16}}
    ))
    gauge.update_layout(height=320, margin={'t': 50, 'b': 0, 'l': 0, 'r': 0})
    st.plotly_chart(gauge, use_container_width=True)

    st.write(f'<i class="fas fa-fire" style="color:#ff6961"></i> Churn probability: **{prob:.2%}**', unsafe_allow_html=True)
    st.write(f'<i class="fas fa-shield-alt" style="color:#4fd348"></i> Retention probability: **{100-prob*100:.2f}%**', unsafe_allow_html=True)

    st.markdown('<h5><i class="fas fa-table"></i> Input values used</h5>', unsafe_allow_html=True)
    st.write(input_df.T.rename(columns={0: 'value'}))

    # Feature contribution (mock SHAP values)
    mock_contrib = pd.Series({
        'SatisfactionScore': abs(input_data['SatisfactionScore'] - 3) * 0.12 + 0.05,
        'DaySinceLastOrder': input_data['DaySinceLastOrder'] / 365 * 0.2,
        'CashbackAmount': input_data['CashbackAmount'] / 50000 * 0.15,
        'Tenure': (240 - input_data['Tenure']) / 240 * 0.1,
        'NumberOfDeviceRegistered': input_data['NumberOfDeviceRegistered'] / 50 * 0.08,
    }).sort_values(ascending=False)

    top3 = mock_contrib.head(3).reset_index().rename(columns={'index': 'feature', 0: 'importance'})
    fig_contrib = px.bar(top3, x='importance', y='feature', orientation='h', color='importance', color_continuous_scale='Blues', title='Top 3 Feature Contribution (Mock SHAP)')
    fig_contrib.update_layout(yaxis={'categoryorder':'total ascending'}, height=320)
    st.plotly_chart(fig_contrib, use_container_width=True)

    # SHAP Explanation for this prediction
    st.markdown('<h5><i class="fas fa-brain"></i> SHAP Explanation for this prediction</h5>', unsafe_allow_html=True)
    if SHAP_AVAILABLE:
        try:
            explainer = shap.TreeExplainer(model)
            input_shap = encode_cat_features(input_scaled)
            shap_values_single = explainer.shap_values(input_shap)
            
            # Create proper Explanation object for waterfall
            if isinstance(shap_values_single, list) and len(shap_values_single) > 1:
                shap_vals = shap_values_single[1][0]
                exp_val = explainer.expected_value[1] if isinstance(explainer.expected_value, list) else explainer.expected_value
            else:
                shap_vals = shap_values_single[0]
                exp_val = explainer.expected_value if not isinstance(explainer.expected_value, list) else explainer.expected_value[0]
            
            # Create Explanation object
            explanation = shap.Explanation(values=shap_vals, base_values=exp_val, data=input_shap.iloc[0].values, feature_names=feature_names)
            fig = plt.figure()
            shap.waterfall_plot(explanation, max_display=10)
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        except Exception as e:
            st.info(f"SHAP waterfall unavailable: {str(e)[:80]}. Check the mock feature contribution above.")
    else:
        st.info('SHAP is not installed. Review the mock feature contribution chart above.')

    st.download_button('Download result as CSV', data=pd.concat([input_df, pd.DataFrame({'ChurnProbability':[prob], 'Prediction':[pred]})], axis=1).to_csv(index=False).encode('utf-8'), file_name='churn_prediction_output.csv', mime='text/csv')

with st.expander('<i class="fas fa-search"></i> SHAP Feature Importance', expanded=True):
    if not SHAP_AVAILABLE:
        st.warning('SHAP is not installed in this environment. Install with `pip install shap` to see SHAP feature importance charts.')
    elif raw_df.empty or 'Churn' not in raw_df.columns:
        st.warning('Dataset missing, cannot compute SHAP importance.')
    else:
        st.info('Computing SHAP feature importance using TreeExplainer...')
        # Prepare sample data for SHAP
        sample_df = raw_df[feature_names].copy()
        # Encode non-numeric categories robustly
        sample_df = encode_cat_features(sample_df)
        # Scale numerical vars
        sample_scaled = sample_df.copy()
        sample_scaled[scale_vars] = scaler.transform(sample_scaled[scale_vars])

        # SHAP explainer
        explainer = shap.TreeExplainer(model)
        sample_for_shap = sample_scaled.sample(min(100, len(sample_scaled)), random_state=42)
        shap_values = explainer.shap_values(sample_for_shap)

        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': abs(shap_values[1]).mean(axis=0) if isinstance(shap_values, list) and len(shap_values) > 1 else abs(shap_values).mean(axis=0)
        }).sort_values('importance', ascending=False)

        fig_shap = px.bar(feature_importance, x='importance', y='feature', orientation='h', title='SHAP Feature Importance')
        st.plotly_chart(fig_shap, use_container_width=True)

st.sidebar.markdown('---')
st.sidebar.markdown('<p style="color:#9bb2e0">Senior Full-Stack Data Engineer mode: pro dashboard controls and visual cues.</p>', unsafe_allow_html=True)
