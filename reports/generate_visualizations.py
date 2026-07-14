"""
Script to generate all visualizations for the fraud detection model.
Run this after training the model (see notebooks/03_modeling.ipynb).

Generated files saved to: ../images/
"""

import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


def generate_all_visualizations():
    """
    Generate all production-ready visualizations.
    
    Assumes model is trained and predictions are available.
    """
    
    import sys
    sys.path.append('..')
    
    print("="*70)
    print("GENERATING VISUALIZATIONS FOR FRAUD DETECTION MODEL")
    print("="*70)
    
    output_dir = Path(__file__).parent.parent / 'images'
    output_dir.mkdir(exist_ok=True)
    
    print(f"\nOutput directory: {output_dir}")
    
    # Note: Actual visualization generation happens in notebooks/03_modeling.ipynb
    # This script is a template for batch visualization generation
    
    visualizations = [
        "✓ confusion_matrix.png - Binary classification confusion matrix",
        "✓ roc_curve.png - ROC curve with AUC score",
        "✓ precision_recall_curve.png - Precision-Recall curve",
        "✓ feature_importance.png - Top 15 feature importances",
        "✓ fraud_distribution.png - Class imbalance visualization",
        "✓ claim_amount_distribution.png - Amount distributions (fraud vs legit)",
        "✓ state_fraud_distribution.png - Geographic fraud patterns",
        "✓ threshold_analysis.png - Precision/Recall trade-offs",
    ]
    
    print("\n" + "="*70)
    print("VISUALIZATIONS TO GENERATE")
    print("="*70)
    for viz in visualizations:
        print(f"  {viz}")
    
    print("\n" + "="*70)
    print("INSTRUCTIONS")
    print("="*70)
    print("""
1. Run notebooks in order:
   - notebooks/01_eda.ipynb          (saves fraud_distribution.png, etc)
   - notebooks/02_feature_engineering.ipynb  (saves feature_correlation.png)
   - notebooks/03_modeling.ipynb     (saves confusion_matrix.png, roc_curve.png, etc)

2. All visualizations automatically saved to images/ folder

3. Use visualizations in:
   - reports/fraud_detection_report.md  (stakeholder report)
   - presentations/fraud_detection_deck.pptx  (business presentation)
   - team reviews / regulatory audits

4. Update .gitignore to ignore PNG/image files (already included)
    """)
    
    print("\n✓ Visualization generation script ready!")
    print("  Run notebooks to generate images.")


def example_visualization_code():
    """
    Template code for generating individual visualizations.
    (Actual code is in src/model_evaluation.py)
    """
    
    code_examples = """
# Example 1: Confusion Matrix
from src.model_evaluation import plot_confusion_matrix
plot_confusion_matrix(y_test, y_pred, save_path='../images/confusion_matrix.png')

# Example 2: ROC Curve
from src.model_evaluation import plot_roc_curve
plot_roc_curve(y_test, y_pred_proba, save_path='../images/roc_curve.png')

# Example 3: Feature Importance
import pandas as pd
import matplotlib.pyplot as plt
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(10, 6))
feature_importance.head(15).plot(x='feature', y='importance', kind='barh')
plt.savefig('../images/feature_importance.png', dpi=300, bbox_inches='tight')

# Example 4: Fraud Distribution (Class Imbalance)
df['PotentialFraud'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.savefig('../images/fraud_distribution.png', dpi=300, bbox_inches='tight')
    """
    
    return code_examples


if __name__ == "__main__":
    generate_all_visualizations()
    print("\n" + example_visualization_code())
