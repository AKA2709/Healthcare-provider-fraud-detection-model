# 🚀 Healthcare Fraud Detection - Startup Guide

**Get your fraud detection system up and running in 5 minutes!**

---

## ⚡ 5-Minute Quick Start

### Step 1: Install Dependencies (2 min)

```bash
# Install core ML dependencies
pip install -r requirements.txt

# Install API dependencies  
pip install -r requirements-api.txt
```

Or combined:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn fastapi uvicorn pydantic requests
```

### Step 2: Download Dataset (1 min)

**Option A - Automated (if Kaggle API installed):**
```bash
python data/download_data.py
```

**Option B - Manual:**
1. Visit: https://www.kaggle.com/datasets/rohitrox/healthcare-provider-fraud-detection-analysis
2. Click "Download"
3. Extract CSV files to: `data/raw/`

### Step 3: Train Model (Optional - use existing or train new)

```bash
jupyter notebook notebooks/03_modeling.ipynb
# Run all cells to train and save model to models/fraud_detector_v1.pkl
```

### Step 4: Start API (1 min)

```bash
python -m api.main
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
📖 API docs available at: http://localhost:8000/docs
```

### Step 5: Test It! (1 min)

**In another terminal:**
```bash
python examples/api_usage_example.py
```

**Or open in browser:**
- 📖 Swagger Docs: http://localhost:8000/docs
- 📄 ReDoc: http://localhost:8000/redoc

---

## 📋 Detailed Workflow

### Phase 1: Data Science (30 mins)

#### 1.1 Exploratory Data Analysis
```bash
jupyter notebook notebooks/01_eda.ipynb
```
- Examine fraud distribution
- Test hypotheses about fraud patterns
- Identify key features

#### 1.2 Feature Engineering
```bash
jupyter notebook notebooks/02_feature_engineering.ipynb
```
- Create claim amount features
- Build provider-level aggregations
- Generate state-level features

#### 1.3 Model Training & Evaluation
```bash
jupyter notebook notebooks/03_modeling.ipynb
```
- Train Random Forest with balanced class weights
- Evaluate with precision/recall/F1
- Tune decision threshold
- Save trained model

### Phase 2: API Deployment (5 mins)

#### 2.1 Start Development API
```bash
python -m api.main
```

#### 2.2 Test API Health
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

#### 2.3 Make Single Prediction
```bash
curl -X POST http://localhost:8000/predict \
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
  }'
```

### Phase 3: Production Deployment (10 mins)

#### 3.1 Deploy with Docker

```bash
docker-compose up
```

This will:
- ✅ Build Docker image
- ✅ Start API on port 8000
- ✅ Mount volumes for models & data
- ✅ Enable health checks

#### 3.2 Deploy to Cloud

**Google Cloud Run:**
```bash
gcloud run deploy fraud-detection-api --source .
```

**AWS Lambda:**
```bash
pip install mangum
# Configure SAM or Serverless Framework
```

**Azure App Service:**
```bash
az webapp up --name fraud-api --runtime "PYTHON|3.10"
```

---

## 🔍 Verification & Diagnostics

### Check Setup

```bash
python verify_setup.py
```

This will check:
- ✅ Python version (3.10+)
- ✅ Required packages installed
- ✅ Project structure
- ✅ Model file exists
- ✅ API connectivity

### Common Issues & Solutions

#### ❌ "Model not found"
```
Error: Model file not found at models/fraud_detector_v1.pkl
```
**Solution:** Run `notebooks/03_modeling.ipynb` to train model

#### ❌ "Cannot connect to API"
```
Error: Connection refused
```
**Solution:** Make sure API is running: `python -m api.main`

#### ❌ "Missing dependencies"
```
ModuleNotFoundError: No module named 'fastapi'
```
**Solution:** Install requirements: `pip install -r requirements.txt`

#### ❌ "Port 8000 already in use"
```
Error: OSError: [Errno 48] Address already in use
```
**Solution:** Use different port: `uvicorn api.main:app --port 8001`

---

## 🧪 Testing & Examples

### Run Example Tests

```bash
# Full API example with all endpoints
python examples/api_usage_example.py
```

This demonstrates:
1. Health check
2. Model information
3. Single prediction
4. Batch predictions
5. Explanation/features
6. Threshold analysis

### Manual Testing

#### Test Health Endpoint
```bash
curl http://localhost:8000/health
```

#### Test Model Info
```bash
curl http://localhost:8000/model-info
```

#### Test Single Prediction
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d @examples/sample_claim.json
```

#### Test Batch Prediction
```bash
curl -X POST http://localhost:8000/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "claims": [
      {...},
      {...}
    ]
  }'
```

---

## 📊 Using the API

### Python Client

```python
import requests

# Single prediction
response = requests.post(
    "http://localhost:8000/predict",
    json={
        "InscClaimAmtReimbursed": 25000,
        "ClaimProcedureCode": "99285",
        "ClaimDiagnosisCode": "J45.9",
        "BeneficiaryAge": 75,
        "BeneficiaryGender": "M",
        "State": "CA",
        "Provider": "PRV123456",
        "InpatientOutpatientDays": 5,
    },
    params={"threshold": 0.45}
)

prediction = response.json()
print(f"Fraud Probability: {prediction['fraud_probability']:.2%}")
print(f"Risk Level: {prediction['risk_level']}")
```

### Provided Client Class

```python
from examples.api_usage_example import FraudDetectionClient

client = FraudDetectionClient("http://localhost:8000")

# Health check
health = client.health_check()

# Model info
info = client.get_model_info()

# Single prediction
pred = client.predict_single(claim)

# Batch predictions
results = client.predict_batch([claim1, claim2, claim3])

# Explanation
explanation = client.explain_prediction(claim)
```

---

## 📚 Documentation

| Resource | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview |
| [API_README.md](API_README.md) | Complete API documentation |
| [GITHUB_README.md](GITHUB_README.md) | GitHub portfolio guide |
| [reports/fraud_detection_report.md](reports/fraud_detection_report.md) | Executive summary |
| [reports/model_card.md](reports/model_card.md) | Technical model docs |
| [data/README.md](data/README.md) | Dataset guide |

---

## 🎯 Next Steps

### For Data Scientists
- [ ] Modify features in `src/feature_engineering.py`
- [ ] Tune model hyperparameters in `notebooks/03_modeling.ipynb`
- [ ] Add SHAP explanations for better interpretability
- [ ] Implement fairness auditing by state

### For Software Engineers
- [ ] Add database for predictions
- [ ] Implement authentication (API key/JWT)
- [ ] Add request rate limiting
- [ ] Create CI/CD pipeline (GitHub Actions)
- [ ] Add comprehensive unit tests

### For Product Managers
- [ ] Build frontend dashboard
- [ ] Create monitoring/alerting
- [ ] Implement A/B testing for model versions
- [ ] Setup automated retraining pipeline

---

## 💡 Pro Tips

### Tip 1: Use Interactive Swagger UI
Don't build curl commands manually - use the Swagger UI at:
```
http://localhost:8000/docs
```
Click "Try it out" to test endpoints directly!

### Tip 2: Adjust Decision Threshold
Different business needs = different thresholds:
```python
# High recall (catch more fraud):
requests.post("http://localhost:8000/predict", 
              params={"threshold": 0.30})

# Balanced (default):
requests.post("http://localhost:8000/predict",
              params={"threshold": 0.45})

# High precision (minimize false alarms):
requests.post("http://localhost:8000/predict",
              params={"threshold": 0.60})
```

### Tip 3: Batch Processing for Speed
Instead of 1000 individual requests, use batch endpoint:
```python
# Slower: 1000 individual requests
for claim in claims:
    requests.post("/predict", json=claim)

# Faster: One batch request
requests.post("/predict-batch", json={"claims": claims})
```

### Tip 4: Monitor in Production
Keep API logs to track:
- Prediction times
- Model performance drift
- Error rates
- High-risk claim trends

---

## 🐳 Docker Deployment

### Build & Run Locally

```bash
# Build image
docker build -t fraud-detection-api:1.0 .

# Run container
docker run -p 8000:8000 \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/data:/app/data \
  fraud-detection-api:1.0
```

### With Docker Compose (Recommended)

```bash
# Start
docker-compose up

# Stop
docker-compose down

# View logs
docker-compose logs -f
```

### Push to Docker Hub

```bash
docker tag fraud-detection-api:1.0 YOUR_USERNAME/fraud-detection-api:1.0
docker push YOUR_USERNAME/fraud-detection-api:1.0
```

---

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [scikit-learn Guide](https://scikit-learn.org/stable/)
- [Pydantic Validation](https://docs.pydantic.dev/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

---

## 🆘 Getting Help

### Check Existing Issues
```bash
# Search documentation
grep -r "your-error" docs/
```

### Enable Debug Logging
```bash
# Start API with debug output
LOGLEVEL=DEBUG python -m api.main
```

### View API Logs
```bash
tail -f logs/api.log
```

### Contact Support
- 📧 Email: data-science@company.com
- 💬 GitHub Issues: Create an issue
- 📚 See full docs: [API_README.md](API_README.md)

---

## 🎉 Success Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Dataset downloaded (`python data/download_data.py`)
- [ ] Model trained (`notebooks/03_modeling.ipynb`)
- [ ] API running (`python -m api.main`)
- [ ] Swagger UI accessible (`http://localhost:8000/docs`)
- [ ] Single prediction tested
- [ ] Batch prediction tested
- [ ] Docker image builds (`docker build -t fraud-api .`)

**🎉 You're ready to go!**

---

**Happy fraud detecting! 🏥**

For questions, see [GITHUB_README.md](GITHUB_README.md) or the full documentation.

**Last Updated:** June 2026
