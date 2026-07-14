"""
Healthcare Fraud Detection API - Main Application
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
import logging
import joblib
from pathlib import Path
import traceback

from .config import API_TITLE, API_VERSION, API_DESCRIPTION, CORS_ORIGINS, MODEL_PATH
from .routes import router, set_model

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Load model on API startup"""
    logger.info("🚀 Starting Healthcare Fraud Detection API...")
    
    try:
        # Check if model file exists
        if not MODEL_PATH.exists():
            logger.warning(f"⚠️  Model file not found at {MODEL_PATH}")
            logger.info("   To use the API, train a model first:")
            logger.info("   1. Run notebooks/03_modeling.ipynb")
            logger.info("   2. Model will be saved to models/fraud_detector_v1.pkl")
            set_model(None)
        else:
            # Load model
            logger.info(f"📦 Loading model from {MODEL_PATH}...")
            model = joblib.load(MODEL_PATH)
            set_model(model)
            logger.info("✓ Model loaded successfully!")
            
            # Log model info
            if hasattr(model, 'n_estimators'):
                logger.info(f"   Algorithm: Random Forest ({model.n_estimators} trees)")
            if hasattr(model, 'n_features_in_'):
                logger.info(f"   Features: {model.n_features_in_}")
    
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        logger.error(traceback.format_exc())
        set_model(None)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on API shutdown"""
    logger.info("🛑 Shutting down Healthcare Fraud Detection API...")


@app.get("/", tags=["Root"])
async def root():
    """
    Welcome message and API overview
    """
    return {
        "message": "Welcome to Healthcare Fraud Detection API",
        "version": API_VERSION,
        "documentation": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "health": "/health",
            "model_info": "/model-info",
            "predict": "/predict",
            "predict_batch": "/predict-batch",
            "statistics": "/statistics",
            "explain": "/explain",
        },
        "quick_start": "Send a POST request to /predict with claim data",
    }


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "status_code": 500,
        },
    )


def get_openapi_schema():
    """Customize OpenAPI schema"""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=API_TITLE,
        version=API_VERSION,
        description=API_DESCRIPTION,
        routes=app.routes,
    )
    
    # Add custom info
    openapi_schema["info"]["contact"] = {
        "name": "Data Science Team",
        "email": "data-science@company.com",
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = get_openapi_schema


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting API server...")
    logger.info("📖 API docs available at: http://localhost:8000/docs")
    
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
