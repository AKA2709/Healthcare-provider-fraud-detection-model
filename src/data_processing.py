"""
Data processing module for healthcare fraud detection.
Handles data loading, cleaning, and train/test split.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load data from CSV or parquet file.
    
    Args:
        filepath: Path to data file (CSV or parquet)
    
    Returns:
        DataFrame with raw data
    """
    filepath = Path(filepath)
    
    if filepath.suffix == '.csv':
        return pd.read_csv(filepath)
    elif filepath.suffix == '.parquet':
        return pd.read_parquet(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath.suffix}")


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean raw data: handle missing values, remove duplicates, validate ranges.
    
    Args:
        df: Raw DataFrame
    
    Returns:
        Cleaned DataFrame
    """
    df = df.copy()
    
    # Remove exact duplicates
    df = df.drop_duplicates()
    
    # Drop rows with all NaN values
    df = df.dropna(how='all')
    
    # Fill missing categorical columns with 'Unknown'
    categorical_cols = df.select_dtypes(include='object').columns
    for col in categorical_cols:
        df[col] = df[col].fillna('Unknown')
    
    # Fill missing numeric columns with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    
    # Remove outliers (claims > 99th percentile)
    claim_cols = [col for col in df.columns if 'claim' in col.lower() and 'amount' in col.lower()]
    for col in claim_cols:
        q99 = df[col].quantile(0.99)
        df = df[df[col] <= q99]
    
    return df


def split_data(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Split data into train and test sets, stratified by target.
    
    Args:
        df: Full dataset
        test_size: Proportion for test set (default 0.2)
        random_state: Seed for reproducibility
    
    Returns:
        Tuple of (train_df, test_df)
    """
    from sklearn.model_selection import train_test_split
    
    # Identify target column
    target_col = 'PotentialFraud' if 'PotentialFraud' in df.columns else df.columns[-1]
    
    train_df, test_df = train_test_split(
        df,
        test_size=test_size,
        random_state=random_state,
        stratify=df[target_col]  # Maintain class balance
    )
    
    print(f"Train set size: {len(train_df)} ({len(train_df)/len(df)*100:.1f}%)")
    print(f"Test set size: {len(test_df)} ({len(test_df)/len(df)*100:.1f}%)")
    print(f"Fraud rate (train): {train_df[target_col].mean()*100:.2f}%")
    print(f"Fraud rate (test): {test_df[target_col].mean()*100:.2f}%")
    
    return train_df, test_df


def get_feature_dtypes_summary(df: pd.DataFrame) -> dict:
    """
    Get summary of feature types and missing values.
    
    Args:
        df: DataFrame to analyze
    
    Returns:
        Dictionary with feature information
    """
    summary = {
        'total_features': len(df.columns),
        'numeric_features': len(df.select_dtypes(include=[np.number]).columns),
        'categorical_features': len(df.select_dtypes(include='object').columns),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
    }
    return summary
