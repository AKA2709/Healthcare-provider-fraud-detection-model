"""
Script to download Healthcare Provider Fraud Detection dataset from Kaggle.

Prerequisites:
1. Install Kaggle API: pip install kaggle
2. Create ~/.kaggle/kaggle.json with your API credentials from Kaggle
   See: https://github.com/Kaggle/kaggle-api

Usage:
    python download_data.py
"""

import os
import subprocess
from pathlib import Path


def download_kaggle_dataset():
    """Download Healthcare fraud dataset from Kaggle."""
    
    dataset_name = "rohitrox/healthcare-provider-fraud-detection-analysis"
    output_dir = Path(__file__).parent / "raw"
    
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading dataset to {output_dir}...")
    print(f"Dataset: {dataset_name}")
    
    try:
        # Download dataset using Kaggle CLI
        subprocess.run([
            "kaggle", "datasets", "download",
            "-d", dataset_name,
            "-p", str(output_dir),
            "--unzip"
        ], check=True)
        
        print("✓ Dataset downloaded successfully!")
        
        # List downloaded files
        files = list(output_dir.glob("*.csv"))
        print(f"\nDownloaded files ({len(files)}):")
        for f in files:
            size_mb = f.stat().st_size / (1024**2)
            print(f"  - {f.name} ({size_mb:.1f} MB)")
        
    except FileNotFoundError:
        print("❌ Error: Kaggle CLI not found.")
        print("Install with: pip install kaggle")
        print("Then configure API credentials from: https://www.kaggle.com/settings/account")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading dataset: {e}")
        print("Check your Kaggle API credentials and internet connection.")


if __name__ == "__main__":
    download_kaggle_dataset()
