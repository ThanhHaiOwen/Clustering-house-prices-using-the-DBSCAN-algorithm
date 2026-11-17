import numpy as np
import pandas as pd
from sklearn.preprocessing import RobustScaler

def clean_house_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans raw King County housing data:
    - Drops duplicate records based on unique house 'id'
    - Strips whitespace and ensures correct numeric types
    """
    df_clean = df.drop_duplicates(subset=['id']).copy()
    
    # Ensure numeric columns
    numeric_cols = ['price', 'sqft_living', 'grade', 'bedrooms', 'bathrooms', 'lat', 'long', 'zipcode']
    for col in numeric_cols:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
            
    df_clean = df_clean.dropna(subset=['price', 'sqft_living', 'grade'])
    return df_clean

def transform_features(df: pd.DataFrame, features=None, scaler=None):
    """
    Applies Log1p transformation to skewed numerical features (price, sqft_living)
    and normalizes features using RobustScaler (resistant to outliers).
    
    Returns:
        X_scaled: numpy array of scaled features
        scaler: fitted or provided RobustScaler instance
        X_transformed: DataFrame of log-transformed features
    """
    if features is None:
        features = ['price', 'sqft_living', 'grade']
        
    X_raw = df[features].copy()
    X_transformed = X_raw.copy()
    
    # Log transformation for right-skewed variables
    if 'price' in X_transformed.columns:
        X_transformed['price'] = np.log1p(X_raw['price'])
    if 'sqft_living' in X_transformed.columns:
        X_transformed['sqft_living'] = np.log1p(X_raw['sqft_living'])
        
    if scaler is None:
        scaler = RobustScaler()
        X_scaled = scaler.fit_transform(X_transformed)
    else:
        X_scaled = scaler.transform(X_transformed)
        
    return X_scaled, scaler, X_transformed
