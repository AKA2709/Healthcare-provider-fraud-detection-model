# Healthcare Fraud Detection API

**Production-Ready REST API** for detecting fraudulent healthcare provider claims using machine learning.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🚀 Quick Start

### Option 1: Run Locally

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-api.txt

# Train model first (or load existing)
# jupyter notebook notebooks/03_modeling.ipynb

# Start API
python -m api.main
```

API will be available at: **http://localhost:8000**

### Option 2: Run with Docker

```bash
# Build and start with Docker Compose
docker-compose up

# Or build manually
docker build -t fraud-detection-api .
docker run -p 8000:8000 fraud-detection-api
```

---

## 📖 API Documentation

Once running, access interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI JSON:** http://localhost:8000/openapi.json

---

## 🔌 API Endpoints

### System Health

#### `GET /health`
Check API and model availability

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "model_loaded": true,
  "timestamp": "2026-06-21T10:30:45.123456",
  "uptime_seconds": 3600.5
}
```

#### `GET /model-info`
Get detailed model information and performance metrics

**Response:**
```json
{
  "model_name": "Random Forest Fraud Detector",
  "model_version": "1.0.0",
  "algorithm": "Random Forest Classification",
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
  "fraud_prevalence": 0.05
}
```

---

### Predictions

#### `POST /predict`
Predict fraud probability for a **single claim**

**Request:**
```json
{
  "InscClaimAmtReimbursed": 25000.0,
  "ClaimProcedureCode": "99285",
  "ClaimDiagnosisCode": "J45.9",
  "BeneficiaryAge": 75,
  "BeneficiaryGender": "M",
  "State": "CA",
  "Provider": "PRV123456",
  "InpatientOutpatientDays": 5
}
```

**Query Parameters:**
- `threshold` (float, 0-1): Decision threshold for fraud classification (default: 0.45)

**Response:**
```json
{
  "fraud_probability": 0.78,
  "fraud_prediction": 1,
  "risk_level": "high",
  "confidence": 0.92,
  "recommendation": "Flag for manual review by compliance officer"
}
```

**Risk Levels:**
- `low` (0-0.4): Approve claim
- `medium` (0.4-0.6): Add to review queue
- `high` (0.6-0.8): Escalate to compliance
- `critical` (0.8-1.0): Urgent investigation

---

#### `POST /predict-batch`
Predict fraud probability for **multiple claims** (up to 1000)

**Request:**
```json
{
  "claims": [
    {
      "InscClaimAmtReimbursed": 25000.0,
      "ClaimProcedureCode": "99285",
      "ClaimDiagnosisCode": "J45.9",
      "BeneficiaryAge": 75,
      "BeneficiaryGender": "M",
      "State": "CA",
      "Provider": "PRV123456",
      "InpatientOutpatientDays": 5
    },
    {
      "InscClaimAmtReimbursed": 5000.0,
      "ClaimProcedureCode": "99213",
      "ClaimDiagnosisCode": "Z00.00",
      "BeneficiaryAge": 45,
      "BeneficiaryGender": "F",
      "State": "NY",
      "Provider": "PRV789012",
      "InpatientOutpatientDays": 0
    }
  ],
  "threshold": 0.45,
  "include_explanation": false
}
```

**Response:**
```json
{
  "total_claims": 2,
  "predictions": [
    {
      "claim_id": "CLM-1",
      "fraud_probability": 0.78,
      "fraud_prediction": 1,
      "risk_level": "high",
      "confidence": 0.92,
      "recommendation": "Flag for manual review by compliance officer"
    },
    {
      "claim_id": "CLM-2",
      "fraud_probability": 0.12,
      "fraud_prediction": 0,
      "risk_level": "low",
      "confidence": 0.88,
      "recommendation": "Approve claim. Monitor for patterns."
    }
  ],
  "fraud_rate": 0.5,
  "high_risk_count": 1,
  "processing_time_seconds": 0.234
}
```

---

### Explainability

#### `POST /explain`
Get feature importance explanation for a prediction

**Request:** (same as `/predict`)

**Response:**
```json
{
  "claim": { ... },
  "top_contributing_features": [
    {"feature": "claim_amount_zscore", "importance": 0.248},
    {"feature": "provider_fraud_rate", "importance": 0.182},
    {"feature": "days_since_discharge", "importance": 0.141}
  ],
  "note": "For production, use SHAP values for instance-level explanations"
}
```

---

### Analytics

#### `GET /statistics`
Get API usage statistics and prediction analytics

**Query Parameters:**
- `limit` (int, 1-1000): Number of recent predictions to analyze (default: 100)

**Response:**
```json
{
  "total_predictions": 1523,
  "average_fraud_probability": 0.23,
  "fraud_cases_flagged": 187,
  "average_processing_time_ms": 45.2,
  "model_performance": {
    "precision": 0.765,
    "recall": 0.713,
    "f1_score": 0.738
  }
}
```

---

## 💻 Usage Examples

### Python Client

```python
import requests

# API configuration
API_URL = "http://localhost:8000"

# Single prediction
claim = {
    "InscClaimAmtReimbursed": 25000.0,
    "ClaimProcedureCode": "99285",
    "ClaimDiagnosisCode": "J45.9",
    "BeneficiaryAge": 75,
    "BeneficiaryGender": "M",
    "State": "CA",
    "Provider": "PRV123456",
    "InpatientOutpatientDays": 5,
}

response = requests.post(
    f"{API_URL}/predict",
    json=claim,
    params={"threshold": 0.45}
)
prediction = response.json()

print(f"Fraud Probability: {prediction['fraud_probability']:.2%}")
print(f"Risk Level: {prediction['risk_level'].upper()}")
print(f"Recommendation: {prediction['recommendation']}")
```

### Using the Provided Client

```python
from examples.api_usage_example import FraudDetectionClient

client = FraudDetectionClient()

# Check health
health = client.health_check()

# Get model info
model_info = client.get_model_info()

# Single prediction
prediction = client.predict_single(claim, threshold=0.45)

# Batch predictions
results = client.predict_batch([claim1, claim2, claim3])

# Get explanation
explanation = client.explain_prediction(claim)
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "InscClaimAmtReimbursed": 25000,
    "ClaimProcedureCode": "99285",
    "ClaimDiagnosisCode": "J45.9",
    "BeneficiaryAge": 75,
    "BeneficiaryGender": "M",
    "State": "CA",
    "Provider": "PRV123456",
    "InpatientOutpatientDays": 5
  }' \
  --url-query "threshold=0.45"
```

---

## 🔑 Key Features

✅ **Real-time Predictions** - Get fraud probability in <50ms  
✅ **Batch Processing** - Analyze up to 1000 claims at once  
✅ **Explainability** - Feature importance for each prediction  
✅ **Threshold Tuning** - Adjust precision/recall trade-off  
✅ **Auto Documentation** - Interactive Swagger UI  
✅ **Error Handling** - Comprehensive error messages  
✅ **Health Checks** - Monitor API and model availability  
✅ **Docker Ready** - Deploy anywhere with Docker  

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Latency (single)** | <50ms |
| **Throughput** | 10,000+ claims/min |
| **Precision** | 76.5% |
| **Recall** | 71.3% |
| **AUC-ROC** | 0.89 |

---

## 🔒 Security & Ethics

### Best Practices
- ✅ Input validation (Pydantic schemas)
- ✅ CORS middleware for web integration
- ✅ Rate limiting (recommended for production)
- ✅ Request/response logging
- ✅ Error masking (no sensitive data in errors)

### Fairness Considerations
- Model may show geographic bias (higher fraud rates in certain states)
- Recommend monitoring precision/recall by state
- Implement human review for all flags

### Production Recommendations
1. **Authentication** - Add API key or JWT authentication
2. **Rate Limiting** - Implement request throttling
3. **Monitoring** - Track model performance drift
4. **Logging** - Store predictions for audit trail
5. **Database** - Add persistence for predictions
6. **Caching** - Cache model predictions when possible

---

## 🔄 Deployment

### Local Development
```bash
python -m api.main
```

### Production (Gunicorn + Uvicorn)
```bash
pip install gunicorn
gunicorn api.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

### Cloud Deployment

**AWS (Lambda + API Gateway)**
```bash
pip install mangum
# Use Mangum adapter for Lambda
```

**Google Cloud (Cloud Run)**
```bash
gcloud run deploy fraud-detection-api \
  --source . \
  --platform managed \
  --region us-central1
```

**Azure (App Service)**
```bash
az webapp up \
  --name fraud-detection-api \
  --resource-group myResourceGroup \
  --sku B1 \
  --runtime "PYTHON|3.10"
```

---

## 📝 Configuration

Environment variables (optional):

```bash
LOG_LEVEL=INFO              # Logging level
API_TITLE="Fraud Detection" # API title
```

Modify in `api/config.py`:
- `DEFAULT_FRAUD_THRESHOLD` - Default decision threshold
- `MAX_BATCH_SIZE` - Max claims per batch request
- `CORS_ORIGINS` - Allowed origins for CORS

---

## 🧪 Testing

```bash
# Run example usage
python examples/api_usage_example.py

# Run tests (if available)
pytest tests/
```

---

## 🐛 Troubleshooting

**Issue: Model not loading**
```
❌ Model file not found at models/fraud_detector_v1.pkl
Solution: Train model first using notebooks/03_modeling.ipynb
```

**Issue: Cannot connect to API**
```
Error: Connection refused
Solution: Make sure API is running with: python -m api.main
```

**Issue: Prediction errors**
```
400 Bad Request: Missing required fields
Solution: Check request format matches schema in /docs
```

---

## 📚 Related Documentation

- [Main README](../README.md) - Project overview
- [Model Card](../reports/model_card.md) - Technical details
- [Feature Engineering](../notebooks/02_feature_engineering.ipynb) - Features used
- [Data Guide](../data/README.md) - Dataset information

---

## 📞 Support & Contact

For issues or questions:
- 📖 Check API docs: `/docs`
- 📧 Email: data-science@company.com
- 🐛 Report bugs on GitHub

---

**License:** MIT  
**Version:** 1.0.0  
**Last Updated:** June 2026

