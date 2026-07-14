"""
Model evaluation and visualization module.
Metrics, plots, and analysis for fraud detection models.
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    confusion_matrix, classification_report, roc_curve, auc,
    precision_recall_curve, f1_score, precision_score, recall_score
)


def evaluate_model(y_true, y_pred, y_pred_proba=None):
    """
    Comprehensive model evaluation with all relevant metrics.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels (binary)
        y_pred_proba: Predicted probabilities (for ROC-AUC)
    
    Returns:
        Dictionary with metrics
    """
    metrics = {
        'accuracy': (y_pred == y_true).mean(),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1': f1_score(y_true, y_pred),
    }
    
    if y_pred_proba is not None:
        metrics['roc_auc'] = auc(
            *roc_curve(y_true, y_pred_proba)[:2]
        )
    
    return metrics


def print_classification_report(y_true, y_pred):
    """Print detailed classification report."""
    print("\n" + "="*60)
    print("CLASSIFICATION REPORT")
    print("="*60)
    print(classification_report(y_true, y_pred, target_names=['Legitimate', 'Fraud']))


def plot_confusion_matrix(y_true, y_pred, figsize=(8, 6), save_path=None):
    """
    Plot confusion matrix.
    
    Args:
        y_true: True labels
        y_pred: Predicted labels
        figsize: Figure size
        save_path: Path to save figure (optional)
    """
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=True,
                xticklabels=['Legitimate', 'Fraud'],
                yticklabels=['Legitimate', 'Fraud'])
    plt.title('Confusion Matrix', fontsize=14, fontweight='bold')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    return cm


def plot_roc_curve(y_true, y_pred_proba, figsize=(8, 6), save_path=None):
    """
    Plot ROC curve.
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        figsize: Figure size
        save_path: Path to save figure (optional)
    """
    fpr, tpr, _ = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=figsize)
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Classifier')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC Curve - Fraud Detection', fontsize=14, fontweight='bold')
    plt.legend(loc='lower right')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    return roc_auc


def plot_precision_recall_curve(y_true, y_pred_proba, figsize=(8, 6), save_path=None):
    """
    Plot Precision-Recall curve (important for imbalanced data).
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        figsize: Figure size
        save_path: Path to save figure (optional)
    """
    precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
    avg_precision = np.mean(precision)
    
    plt.figure(figsize=figsize)
    plt.plot(recall, precision, color='green', lw=2, label=f'AP = {avg_precision:.2f}')
    plt.fill_between(recall, precision, alpha=0.2, color='green')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('Precision-Recall Curve (handles class imbalance)', fontsize=14, fontweight='bold')
    plt.legend(loc='best')
    plt.grid(alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    return avg_precision


def analyze_threshold_tradeoff(y_true, y_pred_proba, thresholds=None):
    """
    Analyze precision/recall trade-offs at different decision thresholds.
    
    Args:
        y_true: True labels
        y_pred_proba: Predicted probabilities
        thresholds: List of thresholds to test (default: 0.3, 0.4, 0.5, 0.6, 0.7)
    
    Returns:
        DataFrame with metrics at each threshold
    """
    if thresholds is None:
        thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]
    
    results = []
    for threshold in thresholds:
        y_pred = (y_pred_proba >= threshold).astype(int)
        results.append({
            'threshold': threshold,
            'precision': precision_score(y_true, y_pred),
            'recall': recall_score(y_true, y_pred),
            'f1': f1_score(y_true, y_pred),
            'fraud_detected': y_pred.sum(),
        })
    
    import pandas as pd
    df_results = pd.DataFrame(results)
    print("\n" + "="*80)
    print("THRESHOLD ANALYSIS - Precision/Recall Trade-off")
    print("="*80)
    print(df_results.to_string(index=False))
    
    return df_results
