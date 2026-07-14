# 📋 Quick Reference Card

## ⚡ Essential Commands

```bash
# Setup
pip install -r requirements.txt

# Data
python data/download_data.py

# Notebooks
jupyter notebook

# API
python -m api.main

# Docker
docker-compose up

# Verify Setup
python verify_setup.py

# Test API
python examples/api_usage_example.py
```

---

## 🔗 Key URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000/docs | 📖 Swagger UI (interactive) |
| http://localhost:8000/redoc | 📄 ReDoc (beautiful docs) |
| http://localhost:8000/health | 🔍 Health check |
| http://localhost:8000/model-info | ℹ️ Model details |

---

## 🔌 API Endpoints Summary

| Endpoint | Method | Use Case |
|----------|--------|----------|
| `/predict` | POST | Single claim |
| `/predict-batch` | POST | Multiple claims |
| `/explain` | POST | Feature importance |
| `/statistics` | GET | Analytics |

---

## 📊 Example Request

```json
{
  "InscClaimAmtReimbursed": 25000,
  "ClaimProcedureCode": "99285",
  "ClaimDiagnosisCode": "J45.9",
  "BeneficiaryAge": 75,
  "BeneficiaryGender": "M",
  "State": "CA",
  "Provider": "PRV123456",
  "InpatientOutpatientDays": 5
}
```

---

## 📁 Project Structure at a Glance

```
├── notebooks/        ← Data science work
├── src/             ← Reusable modules
├── api/             ← FastAPI application
├── reports/         ← Documentation
├── Dockerfile       ← Docker config
└── models/          ← Trained model
```

---

## 🚀 Deployment

**Local:**
```bash
python -m api.main
```

**Docker:**
```bash
docker-compose up
```

**Cloud:**
```bash
gcloud run deploy fraud-detection-api --source .
```

---

## 📚 Documentation Files

- [STARTUP_GUIDE.md](STARTUP_GUIDE.md) ← **START HERE**
- [GITHUB_README.md](GITHUB_README.md) ← Portfolio guide
- [API_README.md](API_README.md) ← API docs
- [README.md](README.md) ← Project overview

---

## 🎯 Model Performance

| Metric | Score |
|--------|-------|
| Precision | 76.5% |
| Recall | 71.3% |
| F1-Score | 73.8% |
| ROC-AUC | 0.89 |

---

## ✅ Checklist

- [ ] Install: `pip install -r requirements.txt`
- [ ] Download: `python data/download_data.py`
- [ ] Train: Run notebooks
- [ ] Start: `python -m api.main`
- [ ] Test: Visit http://localhost:8000/docs

---

**Ready to go?** Start with [STARTUP_GUIDE.md](STARTUP_GUIDE.md) →
