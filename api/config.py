"""
Configuration for Healthcare Fraud Detection API
"""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "fraud_detector_v1.pkl"
FEATURE_NAMES_PATH = PROJECT_ROOT / "models" / "feature_names.txt"
DATA_DIR = PROJECT_ROOT / "data"

# API Settings
API_TITLE = "Healthcare Fraud Detection API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
ML-powered API for detecting fraudulent healthcare provider claims.

## Features
- **Single Prediction**: Predict fraud probability for a single claim
- **Batch Predictions**: Analyze multiple claims at once
- **Model Info**: Get model details and performance metrics
- **Health Check**: Monitor API availability

## Model
- **Algorithm**: Random Forest (200 trees)
- **Performance**: 76.5% precision, 71.3% recall, 0.89 AUC-ROC
- **Handling**: Imbalanced classification (5% fraud rate)

## Authentication
Currently no authentication required (suitable for internal deployment).
For production, add API key/JWT authentication.
"""

# Model Settings
DEFAULT_FRAUD_THRESHOLD = 0.45  # Threshold for binary prediction
MIN_PROBABILITY = 0.0
MAX_PROBABILITY = 1.0

# Request Settings
MAX_BATCH_SIZE = 1000
REQUEST_TIMEOUT_SECONDS = 30

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = PROJECT_ROOT / "logs" / "api.log"

# CORS Settings (for web frontend)
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:3000",
]

# Feature schema (required for predictions)
REQUIRED_FEATURES = [
    "InscClaimAmtReimbursed",
    "BeneficiaryAge",
    "claim_amount_zscore",
    "provider_fraud_rate",
    "state_fraud_prevalence",
    "age_group",
    "gender",
    "provider_procedure_diversity",
    "provider_diagnosis_diversity",
    "days_since_discharge",
    # ... add all 50+ engineered features
]
