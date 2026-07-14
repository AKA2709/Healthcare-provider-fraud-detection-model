"""
Example: How to use the Healthcare Fraud Detection API

Run the API first:
    python -m api.main

Or with Docker:
    docker-compose up

Then test with these examples:
"""

import requests
import json
from typing import Dict, List

# API configuration
API_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}


class FraudDetectionClient:
    """Client for Healthcare Fraud Detection API"""
    
    def __init__(self, base_url: str = API_URL):
        self.base_url = base_url
        self.headers = HEADERS
    
    def health_check(self) -> Dict:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def get_model_info(self) -> Dict:
        """Get model information"""
        response = requests.get(f"{self.base_url}/model-info")
        return response.json()
    
    def predict_single(self, claim: Dict, threshold: float = 0.45) -> Dict:
        """Predict fraud for a single claim"""
        response = requests.post(
            f"{self.base_url}/predict",
            json=claim,
            params={"threshold": threshold},
            headers=self.headers
        )
        return response.json()
    
    def predict_batch(self, claims: List[Dict], threshold: float = 0.45) -> Dict:
        """Predict fraud for multiple claims"""
        payload = {
            "claims": claims,
            "threshold": threshold,
            "include_explanation": False
        }
        response = requests.post(
            f"{self.base_url}/predict-batch",
            json=payload,
            headers=self.headers
        )
        return response.json()
    
    def explain_prediction(self, claim: Dict) -> Dict:
        """Get feature importance explanation"""
        response = requests.post(
            f"{self.base_url}/explain",
            json=claim,
            headers=self.headers
        )
        return response.json()


# Example claims data
EXAMPLE_CLAIM_1 = {
    "InscClaimAmtReimbursed": 25000.0,
    "ClaimProcedureCode": "99285",
    "ClaimDiagnosisCode": "J45.9",
    "BeneficiaryAge": 75,
    "BeneficiaryGender": "M",
    "State": "CA",
    "Provider": "PRV123456",
    "InpatientOutpatientDays": 5,
}

EXAMPLE_CLAIM_2 = {
    "InscClaimAmtReimbursed": 5000.0,
    "ClaimProcedureCode": "99213",
    "ClaimDiagnosisCode": "Z00.00",
    "BeneficiaryAge": 45,
    "BeneficiaryGender": "F",
    "State": "NY",
    "Provider": "PRV789012",
    "InpatientOutpatientDays": 0,
}

EXAMPLE_CLAIM_3 = {
    "InscClaimAmtReimbursed": 50000.0,
    "ClaimProcedureCode": "99285",
    "ClaimDiagnosisCode": "I10",
    "BeneficiaryAge": 82,
    "BeneficiaryGender": "M",
    "State": "FL",
    "Provider": "PRV345678",
    "InpatientOutpatientDays": 14,
}


def example_health_check():
    """Example: Check API health"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Health Check")
    print("="*70)
    
    client = FraudDetectionClient()
    
    try:
        health = client.health_check()
        print(json.dumps(health, indent=2))
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running:")
        print("   python -m api.main")
        return False
    
    return True


def example_model_info():
    """Example: Get model information"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Model Information")
    print("="*70)
    
    client = FraudDetectionClient()
    
    try:
        model_info = client.get_model_info()
        print(json.dumps(model_info, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")


def example_single_prediction():
    """Example: Predict fraud for a single claim"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Single Claim Prediction")
    print("="*70)
    
    client = FraudDetectionClient()
    
    print("\nClaim Data:")
    print(json.dumps(EXAMPLE_CLAIM_1, indent=2))
    
    try:
        prediction = client.predict_single(EXAMPLE_CLAIM_1, threshold=0.45)
        print("\nPrediction Result:")
        print(json.dumps(prediction, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")


def example_batch_predictions():
    """Example: Predict fraud for multiple claims"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Batch Predictions (3 claims)")
    print("="*70)
    
    client = FraudDetectionClient()
    
    claims = [EXAMPLE_CLAIM_1, EXAMPLE_CLAIM_2, EXAMPLE_CLAIM_3]
    
    try:
        results = client.predict_batch(claims, threshold=0.45)
        print(json.dumps(results, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")


def example_explain():
    """Example: Get explanation for prediction"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Prediction Explanation")
    print("="*70)
    
    client = FraudDetectionClient()
    
    try:
        explanation = client.explain_prediction(EXAMPLE_CLAIM_1)
        print(json.dumps(explanation, indent=2))
    except Exception as e:
        print(f"❌ Error: {e}")


def example_different_thresholds():
    """Example: Compare predictions at different thresholds"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Threshold Analysis")
    print("="*70)
    print("Testing high-risk claim at different decision thresholds:\n")
    
    client = FraudDetectionClient()
    thresholds = [0.30, 0.45, 0.60, 0.75]
    
    try:
        for threshold in thresholds:
            pred = client.predict_single(EXAMPLE_CLAIM_1, threshold=threshold)
            print(f"Threshold {threshold:.2f}:")
            print(f"  Fraud Probability: {pred['fraud_probability']:.2%}")
            print(f"  Binary Prediction: {pred['fraud_prediction']} ({'FRAUD' if pred['fraud_prediction'] else 'LEGIT'})")
            print(f"  Risk Level: {pred['risk_level'].upper()}")
            print()
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("\n" + "🏥 Healthcare Fraud Detection API - Usage Examples".center(70))
    print("=" * 70)
    
    # Run examples
    if example_health_check():
        example_model_info()
        example_single_prediction()
        example_batch_predictions()
        example_explain()
        example_different_thresholds()
    
    print("\n" + "="*70)
    print("✓ Examples complete!")
    print("="*70)
    print("\nAPI Documentation available at:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("  - OpenAPI JSON: http://localhost:8000/openapi.json")
