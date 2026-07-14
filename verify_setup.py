#!/usr/bin/env python
"""
Healthcare Fraud Detection API - Quick Start & Verification

This script helps you get started with the project:
1. Checks environment setup
2. Verifies dependencies
3. Tests API connectivity
4. Provides next steps

Run this after: python -m api.main
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Tuple


def print_header(title: str, width: int = 70):
    """Print a formatted header"""
    print("\n" + "="*width)
    print(f"  {title.center(width-4)}")
    print("="*width)


def print_section(title: str):
    """Print a formatted section"""
    print(f"\n✓ {title}")
    print("-" * 70)


def check_python_version() -> bool:
    """Check Python version"""
    version = sys.version_info
    min_version = (3, 10)
    
    if version >= min_version:
        print(f"✅ Python {version.major}.{version.minor} (required: 3.10+)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} (required: 3.10+)")
        return False


def check_dependencies() -> bool:
    """Check if required packages are installed"""
    required_packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pandas': 'Pandas',
        'sklearn': 'scikit-learn',
        'pydantic': 'Pydantic',
        'numpy': 'NumPy',
    }
    
    all_installed = True
    for package, name in required_packages.items():
        try:
            __import__(package)
            print(f"✅ {name}")
        except ImportError:
            print(f"❌ {name} (pip install {package})")
            all_installed = False
    
    return all_installed


def check_project_structure() -> bool:
    """Check if project folders exist"""
    required_folders = [
        'api',
        'src',
        'notebooks',
        'reports',
        'data',
        'models',
        'examples',
    ]
    
    all_exist = True
    for folder in required_folders:
        path = Path(folder)
        if path.exists() and path.is_dir():
            print(f"✅ {folder}/")
        else:
            print(f"❌ {folder}/ (missing)")
            all_exist = False
    
    return all_exist


def check_model_exists() -> bool:
    """Check if trained model exists"""
    model_path = Path('models/fraud_detector_v1.pkl')
    
    if model_path.exists():
        size_mb = model_path.stat().st_size / (1024**2)
        print(f"✅ Model found ({size_mb:.1f} MB)")
        return True
    else:
        print(f"⚠️  Model not found - run notebooks/03_modeling.ipynb to train")
        return False


def test_api_connection() -> bool:
    """Test if API is running"""
    try:
        import requests
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.status_code == 200:
            print(f"✅ API responding at http://localhost:8000")
            return True
        else:
            print(f"❌ API returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"⚠️  API not running (start with: python -m api.main)")
        return False
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def print_next_steps():
    """Print recommended next steps"""
    print_header("📋 NEXT STEPS")
    
    steps = [
        ("Install Dependencies", "pip install -r requirements.txt"),
        ("Download Dataset", "python data/download_data.py"),
        ("Run Notebooks", "jupyter notebook"),
        ("  1. EDA", "notebooks/01_eda.ipynb"),
        ("  2. Features", "notebooks/02_feature_engineering.ipynb"),
        ("  3. Modeling", "notebooks/03_modeling.ipynb"),
        ("Start API", "python -m api.main"),
        ("Access Docs", "http://localhost:8000/docs"),
        ("Test API", "python examples/api_usage_example.py"),
        ("Deploy (Docker)", "docker-compose up"),
    ]
    
    for i, (desc, cmd) in enumerate(steps, 1):
        print(f"\n{i}. {desc}")
        print(f"   $ {cmd}")


def print_api_endpoints():
    """Print available API endpoints"""
    print_header("🔌 API ENDPOINTS")
    
    endpoints = [
        ("GET /health", "Check API status"),
        ("GET /model-info", "Get model details"),
        ("POST /predict", "Single claim prediction"),
        ("POST /predict-batch", "Batch predictions"),
        ("POST /explain", "Feature importance"),
        ("GET /statistics", "Analytics"),
    ]
    
    for endpoint, desc in endpoints:
        print(f"\n{endpoint}")
        print(f"  └─ {desc}")


def print_useful_links():
    """Print useful documentation links"""
    print_header("📚 DOCUMENTATION")
    
    links = [
        ("README.md", "Project overview"),
        ("API_README.md", "Complete API guide"),
        ("GITHUB_README.md", "GitHub portfolio presentation"),
        ("reports/fraud_detection_report.md", "Executive summary"),
        ("reports/model_card.md", "Technical model docs"),
        ("data/README.md", "Dataset information"),
    ]
    
    for file, desc in links:
        print(f"\n• {file}")
        print(f"  └─ {desc}")


def main():
    """Run all checks"""
    print_header("🏥 HEALTHCARE FRAUD DETECTION - SETUP VERIFICATION")
    
    # Run checks
    print_section("1️⃣  ENVIRONMENT")
    py_ok = check_python_version()
    
    print_section("2️⃣  DEPENDENCIES")
    deps_ok = check_dependencies()
    
    print_section("3️⃣  PROJECT STRUCTURE")
    struct_ok = check_project_structure()
    
    print_section("4️⃣  TRAINED MODEL")
    model_ok = check_model_exists()
    
    print_section("5️⃣  API CONNECTIVITY")
    api_ok = test_api_connection()
    
    # Summary
    print_header("✅ VERIFICATION SUMMARY")
    
    checks = [
        ("Python Version", py_ok),
        ("Dependencies", deps_ok),
        ("Project Structure", struct_ok),
        ("Trained Model", model_ok),
        ("API Running", api_ok),
    ]
    
    for check_name, passed in checks:
        status = "✅ PASS" if passed else "⚠️  CHECK"
        print(f"{status}  {check_name}")
    
    # Next steps
    if not deps_ok:
        print("\n⚠️  Install dependencies first:")
        print("   pip install -r requirements.txt")
        return
    
    if not model_ok:
        print("\n⚠️  Train model first:")
        print("   jupyter notebook notebooks/03_modeling.ipynb")
        return
    
    if not api_ok:
        print("\n✓ Start API to test:")
        print("   python -m api.main")
    else:
        print("\n🎉 Everything is ready! Your API is running.")
    
    # Show useful info
    print_api_endpoints()
    print_next_steps()
    print_useful_links()
    
    print_header("🚀 QUICK TEST")
    print("\nTest the API with:")
    print("  python examples/api_usage_example.py")
    
    print("\n📖 View API documentation at:")
    print("  http://localhost:8000/docs")
    
    print("\n" + "="*70)
    print("For more help, see GITHUB_README.md")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
