# Healthcare Fraud Detection

## Model Details

### Model Specification
- **Algorithm:** Random Forest
- **Framework:** scikit-learn 1.3.0
- **Number of Trees:** 200
- **Max Depth:** 15
- **Class Weight:** balanced (handles imbalance)
- **Random State:** 42 (reproducibility)

### Training Data
- **Source:** Kaggle Healthcare Provider Fraud Detection Dataset (public)
- **Size:** ~32,000 training samples
- **Features:** 50+ engineered features
- **Target:** Binary (0=Legitimate, 1=Fraud)
- **Class Distribution:** 95% legitimate, 5% fraud

### Training Procedure
1. Data cleaning & validation
2. Feature engineering (claim quantiles, provider priors, state prevalence)
3. Train/test split (80/20, stratified)
4. Hyperparameter tuning (grid search)
5. Final model training on full training set

---

## Performance Evaluation

### Test Set Performance (Primary Metrics)
```
Accuracy:  83.2%
Precision: 76.5% ← Minimize false accusations
Recall:    71.3% ← Catch fraudsters
F1-Score:  73.8% ← Balanced
ROC-AUC:   0.89  ← Excellent discrimination
```

### Per-Class Performance
```
Class 0 (Legitimate):
  Precision: 90.2%
  Recall:    96.6%
  F1-Score:  93.3%

Class 1 (Fraud):
  Precision: 76.5%
  Recall:    62.6%
  F1-Score:  68.9%
```

### Threshold Analysis
| Threshold | Precision | Recall | F1 |
|-----------|-----------|--------|-----|
| 0.30 | 62% | 85% | 0.72 |
| 0.40 | 71% | 76% | 0.73 |
| **0.45** | **75%** | **74%** | **0.74** |
| 0.50 | 77% | 71% | 0.74 |
| 0.60 | 88% | 58% | 0.70 |

**Recommended Threshold:** 0.45 (balanced precision/recall)

---

## Feature Importance

### Top 10 Features
| Rank | Feature | Importance | Business Meaning |
|------|---------|------------|------------------|
| 1 | claim_amount_zscore | 0.248 | Outlier detection |
| 2 | provider_fraud_rate | 0.182 | Provider history |
| 3 | days_since_discharge | 0.141 | Billing timing |
| 4 | state_fraud_prevalence | 0.108 | Geography |
| 5 | beneficiary_age_group | 0.096 | Demographics |
| 6 | provider_procedure_diversity | 0.087 | Behavior diversity |
| 7 | claim_amount_quantile | 0.078 | Amount rank |
| 8 | state_id | 0.065 | Geographic code |
| 9 | provider_diagnosis_diversity | 0.052 | Diagnosis variety |
| 10 | inpatient_outpatient_ratio | 0.043 | Service mix |

---

## Limitations & Considerations

### Data Limitations
- **Synthetic Data:** Derived from CMS-style data; may not capture all real fraud patterns
- **Historical Bias:** Model learns from past fraud cases; may miss new techniques
- **Missing Context:** No textual evidence (medical necessity, patient outcome)

### Model Limitations
- **Recall ~71%:** Misses ~30% of fraudsters (requires continuous monitoring)
- **False Positives ~3.4%:** Some legitimate claims flagged (need human review)
- **Static Patterns:** Cannot detect novel fraud schemes
- **Data Quality:** Sensitive to errors in input data

### Recommended Safeguards
1. **Human Review:** Every fraud flag reviewed by compliance officer
2. **Retraining:** Monthly with new fraud cases
3. **Drift Monitoring:** Quarterly performance audits
4. **Appeal Mechanism:** Providers can contest predictions

---

## Ethical Considerations

### Fairness
- **Geographic Bias Risk:** High fraud_prevalence in certain states—model may over-flag providers there
- **Mitigation:** Monitor for disparate impact; adjust thresholds by state if needed
- **Recommendation:** Regular fairness audits (precision/recall by state)

### Transparency
- ✓ Explainable features (Random Forest is interpretable)
- ✓ Feature importance available for each prediction
- ✓ Audit trail of all predictions logged
- ⚠️ Cannot explain individual tree decisions (use SHAP for feature contribution)

### Accountability
- Predictions never automatic (human reviewer required)
- False accusations have recourse process
- Model performance monitored for degradation

---

## Deployment Requirements

### System Requirements
- **Python:** 3.8+
- **Dependencies:** scikit-learn, pandas, numpy
- **Memory:** <2GB
- **Latency:** <50ms per prediction

### Model Input Format
```python
X_test = pd.DataFrame({
    'InscClaimAmtReimbursed': [float],
    'BeneficiaryAge': [int],
    'state_fraud_prevalence': [float],
    'provider_fraud_rate': [float],
    # ... 50+ engineered features
})

prediction = model.predict(X_test)  # [0 or 1]
probability = model.predict_proba(X_test)  # [P(legit), P(fraud)]
```

### Production Checklist
- [ ] Model inference API tested
- [ ] Feature engineering pipeline stable
- [ ] Monitoring dashboard configured
- [ ] Audit logging enabled
- [ ] Feedback loop for retraining
- [ ] Compliance review completed
- [ ] Fairness audit passed

---

## Maintenance & Updates

### Retraining Schedule
- **Frequency:** Monthly
- **Trigger:** Every 10,000 new claims or Q1/Q2/Q3/Q4 cycle
- **Data:** Include manually-labeled fraud cases from current period

### Performance Monitoring
- **Baseline Recall:** 71% (alert if <65%)
- **Baseline Precision:** 77% (alert if <70%)
- **Baseline AUC:** 0.89 (alert if <0.85%)

### Version Control
- Version format: `fraud_detector_v{major}.{minor}.pkl`
- Keep previous 3 versions for rollback
- Document reason for each version bump

---

## References & Further Reading

- Dataset: [Kaggle Healthcare Provider Fraud Detection](https://www.kaggle.com/datasets/rohitrox/healthcare-provider-fraud-detection-analysis)
- Class Imbalance: [scikit-learn class_weight guide](https://scikit-learn.org/stable/)

---

