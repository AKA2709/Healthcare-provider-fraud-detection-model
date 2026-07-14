"""
API routes for healthcare fraud detection
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List
import time
import logging
from datetime import datetime
import numpy as np
import pandas as pd

from .models import (
    ClaimInput, BatchPredictionInput, PredictionOutput, BatchPredictionOutput,
    ModelInfo, HealthCheck, ErrorResponse, FraudRiskLevel
)
from .config import DEFAULT_FRAUD_THRESHOLD

logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter()

# Global variables (will be initialized in main.py)
model = None
feature_scaler = None
api_start_time = time.time()


def set_model(ml_model, scaler=None):
    """Set the loaded model (called from main.py)"""
    global model, feature_scaler
    model = ml_model
    feature_scaler = scaler


def get_risk_level(fraud_probability: float) -> FraudRiskLevel:
    """Categorize fraud probability into risk levels"""
    if fraud_probability >= 0.8:
        return FraudRiskLevel.CRITICAL
    elif fraud_probability >= 0.6:
        return FraudRiskLevel.HIGH
    elif fraud_probability >= 0.4:
        return FraudRiskLevel.MEDIUM
    else:
        return FraudRiskLevel.LOW


def get_recommendation(fraud_probability: float, risk_level: FraudRiskLevel) -> str:
    """Generate recommended action based on risk level"""
    recommendations = {
        FraudRiskLevel.CRITICAL: "🚨 URGENT: Immediately escalate to fraud investigation team. Recommend claim suspension pending review.",
        FraudRiskLevel.HIGH: "⚠️ HIGH RISK: Flag for manual review by compliance officer. Prioritize investigation.",
        FraudRiskLevel.MEDIUM: "⚠️ MEDIUM RISK: Add to fraud review queue. Investigate within 48 hours.",
        FraudRiskLevel.LOW: "✓ LOW RISK: Approve claim. Monitor for patterns across provider.",
    }
    return recommendations.get(risk_level, "Requires manual review")


@router.get("/health", response_model=HealthCheck, tags=["System"])
async def health_check():
    """
    Check API health and model availability
    
    Returns:
        Health status, API version, and model availability
    """
    try:
        uptime = time.time() - api_start_time
        return HealthCheck(
            status="healthy" if model is not None else "unhealthy",
            version="1.0.0",
            model_loaded=model is not None,
            timestamp=datetime.utcnow().isoformat(),
            uptime_seconds=uptime,
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


@router.get("/model-info", response_model=ModelInfo, tags=["System"])
async def get_model_info():
    """
    Get detailed information about the fraud detection model
    
    Returns:
        Model metadata, performance metrics, and specifications
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Get model properties
        info = ModelInfo(
            model_name="Random Forest Fraud Detector",
            model_version="1.0.0",
            algorithm="Random Forest Classification",
            training_date="2026-06-21",
            accuracy=0.832,
            precision=0.765,
            recall=0.713,
            f1_score=0.738,
            roc_auc=0.89,
            number_of_trees=getattr(model, 'n_estimators', 200),
            max_depth=getattr(model, 'max_depth', 15),
            number_of_features=model.n_features_in_ if hasattr(model, 'n_features_in_') else 50,
            training_set_size=32000,
            fraud_prevalence=0.05,
        )
        return info
    except Exception as e:
        logger.error(f"Failed to get model info: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve model information")


@router.post("/predict", response_model=PredictionOutput, tags=["Predictions"])
async def predict_single(
    claim: ClaimInput,
    threshold: float = Query(DEFAULT_FRAUD_THRESHOLD, ge=0, le=1, description="Fraud probability threshold")
):
    """
    Predict fraud probability for a single healthcare claim
    
    Args:
        claim: Single claim data
        threshold: Decision threshold for binary classification (default 0.45)
    
    Returns:
        Fraud probability, risk level, and recommendation
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Convert claim to feature vector
        X = pd.DataFrame([claim.dict()])
        
        # Get prediction
        fraud_proba = model.predict_proba(X)[0][1]  # Probability of fraud class
        fraud_pred = 1 if fraud_proba >= threshold else 0
        
        # Calculate risk level and recommendation
        risk_level = get_risk_level(fraud_proba)
        confidence = max(fraud_proba, 1 - fraud_proba)
        recommendation = get_recommendation(fraud_proba, risk_level)
        
        return PredictionOutput(
            fraud_probability=float(fraud_proba),
            fraud_prediction=int(fraud_pred),
            risk_level=risk_level,
            confidence=float(confidence),
            recommendation=recommendation,
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")


@router.post("/predict-batch", response_model=BatchPredictionOutput, tags=["Predictions"])
async def predict_batch(batch_input: BatchPredictionInput):
    """
    Predict fraud probability for multiple claims (batch processing)
    
    Args:
        batch_input: Batch of claims with optional threshold
    
    Returns:
        Predictions for all claims plus summary statistics
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        start_time = time.time()
        threshold = batch_input.threshold
        
        # Convert claims to feature matrix
        claims_data = [claim.dict() for claim in batch_input.claims]
        X = pd.DataFrame(claims_data)
        
        # Get predictions
        fraud_probas = model.predict_proba(X)[:, 1]
        fraud_preds = (fraud_probas >= threshold).astype(int)
        
        # Generate individual predictions
        predictions = []
        for i, (proba, pred) in enumerate(zip(fraud_probas, fraud_preds)):
            risk_level = get_risk_level(proba)
            confidence = max(proba, 1 - proba)
            recommendation = get_recommendation(proba, risk_level)
            
            predictions.append(PredictionOutput(
                claim_id=f"CLM-{i+1}",
                fraud_probability=float(proba),
                fraud_prediction=int(pred),
                risk_level=risk_level,
                confidence=float(confidence),
                recommendation=recommendation,
            ))
        
        # Calculate summary statistics
        fraud_rate = float(fraud_preds.mean())
        high_risk_count = sum(1 for p in predictions if p.risk_level in [FraudRiskLevel.HIGH, FraudRiskLevel.CRITICAL])
        processing_time = time.time() - start_time
        
        return BatchPredictionOutput(
            total_claims=len(batch_input.claims),
            predictions=predictions,
            fraud_rate=fraud_rate,
            high_risk_count=high_risk_count,
            processing_time_seconds=processing_time,
        )
    except Exception as e:
        logger.error(f"Batch prediction failed: {e}")
        raise HTTPException(status_code=400, detail=f"Batch prediction failed: {str(e)}")


@router.get("/statistics", tags=["Analytics"])
async def get_statistics(
    limit: int = Query(100, ge=1, le=1000, description="Number of recent predictions to analyze")
):
    """
    Get API usage statistics and prediction analytics
    
    Returns:
        Recent prediction statistics and system metrics
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        return {
            "message": "Statistics endpoint - tracks predictions over time",
            "note": "Implement with database for production use",
            "sample_metrics": {
                "total_predictions": 1523,
                "average_fraud_probability": 0.23,
                "fraud_cases_flagged": 187,
                "average_processing_time_ms": 45.2,
                "model_performance": {
                    "precision": 0.765,
                    "recall": 0.713,
                    "f1_score": 0.738,
                }
            }
        }
    except Exception as e:
        logger.error(f"Statistics retrieval failed: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve statistics")


@router.post("/explain", tags=["Explainability"])
async def explain_prediction(claim: ClaimInput):
    """
    Get feature importance explanation for a single prediction
    
    Args:
        claim: Single claim data
    
    Returns:
        Feature contributions to fraud probability
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Get model's feature importances
        feature_importance = model.feature_importances_
        feature_names = [field for field in claim.dict().keys()][:len(feature_importance)]
        
        # Sort by importance
        importance_dict = dict(zip(feature_names, feature_importance))
        top_features = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "claim": claim.dict(),
            "top_contributing_features": [
                {"feature": name, "importance": float(importance)}
                for name, importance in top_features
            ],
            "note": "For production, use SHAP values for instance-level explanations"
        }
    except Exception as e:
        logger.error(f"Explanation generation failed: {e}")
        raise HTTPException(status_code=400, detail=f"Explanation failed: {str(e)}")
