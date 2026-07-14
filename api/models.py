"""
Pydantic models for API request/response validation
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from enum import Enum


class FraudRiskLevel(str, Enum):
    """Risk levels for fraud predictions"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ClaimInput(BaseModel):
    """Single healthcare claim for fraud prediction"""
    
    # Claim Information
    InscClaimAmtReimbursed: float = Field(..., gt=0, description="Claim amount in dollars")
    ClaimProcedureCode: str = Field(..., description="Medical procedure code")
    ClaimDiagnosisCode: str = Field(..., description="Primary diagnosis code")
    
    # Beneficiary Information
    BeneficiaryAge: int = Field(..., ge=0, le=120, description="Beneficiary age in years")
    BeneficiaryGender: str = Field(..., description="Gender (M or F)")
    State: str = Field(..., min_length=2, max_length=2, description="State code (e.g., 'CA')")
    
    # Provider Information
    Provider: str = Field(..., description="Provider ID")
    InpatientOutpatientDays: int = Field(default=0, ge=0, description="Days as inpatient/outpatient")
    
    # Engineered Features (optional - will be computed if not provided)
    claim_amount_zscore: Optional[float] = Field(None, description="Z-score of claim amount")
    provider_fraud_rate: Optional[float] = Field(None, description="Provider's historical fraud rate")
    state_fraud_prevalence: Optional[float] = Field(None, description="State-level fraud prevalence")
    age_group: Optional[str] = Field(None, description="Age group (young/middle/senior/elderly)")
    gender: Optional[int] = Field(None, description="Gender encoded (1=M, 0=F)")
    provider_procedure_diversity: Optional[int] = Field(None, description="Procedure diversity")
    provider_diagnosis_diversity: Optional[int] = Field(None, description="Diagnosis diversity")
    days_since_discharge: Optional[int] = Field(None, description="Days since discharge")
    inpatient_outpatient_ratio: Optional[float] = Field(None, description="Claim type ratio")
    
    @validator('BeneficiaryGender')
    def validate_gender(cls, v):
        if v.upper() not in ['M', 'F']:
            raise ValueError("Gender must be 'M' or 'F'")
        return v.upper()
    
    @validator('State')
    def validate_state(cls, v):
        if not v.isupper():
            raise ValueError("State code must be uppercase (e.g., 'CA')")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "InscClaimAmtReimbursed": 12500.50,
                "ClaimProcedureCode": "99285",
                "ClaimDiagnosisCode": "J45.9",
                "BeneficiaryAge": 72,
                "BeneficiaryGender": "M",
                "State": "CA",
                "Provider": "PRV123456",
                "InpatientOutpatientDays": 5,
            }
        }


class BatchPredictionInput(BaseModel):
    """Batch of claims for fraud prediction"""
    
    claims: List[ClaimInput] = Field(..., max_items=1000, description="List of claims (max 1000)")
    include_explanation: bool = Field(
        default=False,
        description="Include feature contribution explanation (slower)"
    )
    threshold: float = Field(
        default=0.45,
        ge=0.0,
        le=1.0,
        description="Decision threshold for binary prediction"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "claims": [
                    {
                        "InscClaimAmtReimbursed": 12500.50,
                        "ClaimProcedureCode": "99285",
                        "ClaimDiagnosisCode": "J45.9",
                        "BeneficiaryAge": 72,
                        "BeneficiaryGender": "M",
                        "State": "CA",
                        "Provider": "PRV123456",
                        "InpatientOutpatientDays": 5,
                    }
                ],
                "threshold": 0.45,
            }
        }


class PredictionOutput(BaseModel):
    """Single fraud prediction result"""
    
    claim_id: Optional[str] = Field(None, description="Unique claim identifier")
    fraud_probability: float = Field(..., ge=0, le=1, description="Probability of fraud (0-1)")
    fraud_prediction: int = Field(..., description="Binary prediction (0=legitimate, 1=fraud)")
    risk_level: FraudRiskLevel = Field(..., description="Risk categorization")
    confidence: float = Field(..., ge=0, le=1, description="Model confidence in prediction")
    recommendation: str = Field(..., description="Recommended action")
    
    class Config:
        schema_extra = {
            "example": {
                "claim_id": "CLM-20260621-001",
                "fraud_probability": 0.78,
                "fraud_prediction": 1,
                "risk_level": "high",
                "confidence": 0.92,
                "recommendation": "Flag for manual review by compliance officer",
            }
        }


class BatchPredictionOutput(BaseModel):
    """Batch prediction results"""
    
    total_claims: int = Field(..., description="Total claims processed")
    predictions: List[PredictionOutput] = Field(..., description="Individual predictions")
    fraud_rate: float = Field(..., description="Percentage of claims flagged as fraud")
    high_risk_count: int = Field(..., description="Number of high/critical risk claims")
    processing_time_seconds: float = Field(..., description="Time to process all claims")
    
    class Config:
        schema_extra = {
            "example": {
                "total_claims": 100,
                "predictions": [],
                "fraud_rate": 0.12,
                "high_risk_count": 8,
                "processing_time_seconds": 2.34,
            }
        }


class ModelInfo(BaseModel):
    """Model metadata and performance information"""
    
    model_name: str = Field(..., description="Model name")
    model_version: str = Field(..., description="Model version")
    algorithm: str = Field(..., description="Algorithm used (Random Forest)")
    training_date: str = Field(..., description="Model training date")
    
    # Performance metrics
    accuracy: float = Field(..., description="Accuracy on test set")
    precision: float = Field(..., description="Precision on test set")
    recall: float = Field(..., description="Recall on test set")
    f1_score: float = Field(..., description="F1-score on test set")
    roc_auc: float = Field(..., description="ROC-AUC on test set")
    
    # Model details
    number_of_trees: int = Field(..., description="Number of trees in forest")
    max_depth: int = Field(..., description="Max depth of trees")
    number_of_features: int = Field(..., description="Number of input features")
    
    # Dataset info
    training_set_size: int = Field(..., description="Size of training set")
    fraud_prevalence: float = Field(..., description="Fraud rate in training data")
    class Config:
        schema_extra = {
            "example": {
                "model_name": "Random Forest Fraud Detector",
                "model_version": "1.0.0",
                "algorithm": "Random Forest",
                "training_date": "2026-06-21",
                "accuracy": 0.832,
                "precision": 0.765,
                "recall": 0.713,
                "f1_score": 0.738,
                "roc_auc": 0.89,
                "number_of_trees": 200,
                "max_depth": 15,
                "number_of_features": 50,
                "training_set_size": 32000,
                "fraud_prevalence": 0.05,
            }
        }


class HealthCheck(BaseModel):
    """Health check response"""
    
    status: str = Field(..., description="API status (healthy/unhealthy)")
    version: str = Field(..., description="API version")
    model_loaded: bool = Field(..., description="Is the fraud detection model loaded?")
    timestamp: str = Field(..., description="Current server time (ISO 8601)")
    uptime_seconds: float = Field(..., description="Seconds since API started")


class ErrorResponse(BaseModel):
    """Error response"""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    status_code: int = Field(..., description="HTTP status code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
