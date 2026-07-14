"""
Feature engineering module for fraud detection.
Creates domain-informed features that capture fraud signals.
"""

import pandas as pd
import numpy as np
from typing import List, Tuple


def create_features(df: pd.DataFrame, target_col: str = 'PotentialFraud') -> pd.DataFrame:
    """
    Create engineered features from raw data.
    
    Args:
        df: Input DataFrame with raw features
        target_col: Name of target column (for prior fraud rates)
    
    Returns:
        DataFrame with new features added
    """
    df = df.copy()
    
    # 1. Claim Amount Features
    if 'InscClaimAmtReimbursed' in df.columns:
        df['claim_amount_quantile'] = df.groupby('Provider')['InscClaimAmtReimbursed'].transform(
            lambda x: pd.qcut(x, q=10, labels=False, duplicates='drop')
        )
        df['claim_amount_zscore'] = df.groupby('Provider')['InscClaimAmtReimbursed'].transform(
            lambda x: np.abs((x - x.mean()) / x.std())
        )
    
    # 2. Provider-level Aggregations (Fraud Prior)
    if target_col in df.columns:
        provider_fraud_rate = df.groupby('Provider')[target_col].agg(['sum', 'count'])
        provider_fraud_rate.columns = ['fraud_count', 'total_claims']
        provider_fraud_rate['provider_fraud_rate'] = (
            provider_fraud_rate['fraud_count'] / provider_fraud_rate['total_claims']
        )
        df = df.merge(provider_fraud_rate[['provider_fraud_rate']], left_on='Provider', right_index=True)
    
    # 3. State-level Aggregations
    if target_col in df.columns and 'State' in df.columns:
        state_fraud_rate = df.groupby('State')[target_col].mean()
        df['state_fraud_prevalence'] = df['State'].map(state_fraud_rate)
    
    # 4. Age Group (binned)
    if 'BeneficiaryAge' in df.columns:
        df['age_group'] = pd.cut(df['BeneficiaryAge'], bins=[0, 40, 65, 75, 100], 
                                  labels=['young', 'middle', 'senior', 'elderly'])
        df['age_group'] = df['age_group'].astype(str)
    
    # 5. Gender encoding
    if 'BeneficiaryGender' in df.columns:
        df['gender'] = df['BeneficiaryGender'].map({'M': 1, 'F': 0}).fillna(0)
    
    # 6. Claim diversity by provider
    if 'ClaimProcedureCode' in df.columns:
        procedure_diversity = df.groupby('Provider')['ClaimProcedureCode'].nunique()
        df['provider_procedure_diversity'] = df['Provider'].map(procedure_diversity)
    
    # 7. Diagnosis code diversity
    if 'ClaimDiagnosisCode' in df.columns:
        diagnosis_diversity = df.groupby('Provider')['ClaimDiagnosisCode'].nunique()
        df['provider_diagnosis_diversity'] = df['Provider'].map(diagnosis_diversity)
    
    # 8. One-hot encode categorical if few unique values
    categorical_cols = ['age_group', 'BeneficiaryGender', 'State']
    for col in categorical_cols:
        if col in df.columns and df[col].nunique() < 50:
            dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
            df = pd.concat([df, dummies], axis=1)
    
    return df


def get_feature_importance_dict(model, feature_names: List[str]) -> dict:
    """
    Extract feature importance from trained model.
    
    Args:
        model: Trained scikit-learn model
        feature_names: List of feature names
    
    Returns:
        Dictionary of {feature: importance}
    """
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
    elif hasattr(model, 'coef_'):
        importances = np.abs(model.coef_[0])
    else:
        raise ValueError("Model doesn't have feature importance")
    
    importance_dict = dict(zip(feature_names, importances))
    # Sort descending
    importance_dict = {k: v for k, v in sorted(
        importance_dict.items(), key=lambda x: x[1], reverse=True
    )}
    
    return importance_dict


def select_top_features(feature_importance: dict, top_n: int = 15) -> List[str]:
    """
    Select top N features by importance.
    
    Args:
        feature_importance: Feature importance dictionary
        top_n: Number of features to select
    
    Returns:
        List of top feature names
    """
    return list(feature_importance.keys())[:top_n]


def validate_feature_distribution(df: pd.DataFrame, feature_col: str) -> dict:
    """
    Check feature distribution statistics.
    
    Args:
        df: DataFrame
        feature_col: Column to validate
    
    Returns:
        Dictionary with stats
    """
    return {
        'mean': df[feature_col].mean(),
        'median': df[feature_col].median(),
        'std': df[feature_col].std(),
        'min': df[feature_col].min(),
        'max': df[feature_col].max(),
        'skewness': df[feature_col].skew(),
        'kurtosis': df[feature_col].kurtosis(),
    }
