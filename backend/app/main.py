from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.database import init_db, get_db
from app.models import seed_categories
from app.routers import expenses, categories, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup: Initialize database
    init_db()
    
    # Seed categories
    db = next(get_db())
    seed_categories(db)
    db.close()
    
    yield
    
    # Shutdown: cleanup if needed
    pass


# Create FastAPI application
app = FastAPI(
    title="Smart Expense Tracker API",
    description="API for tracking expenses with OCR receipt processing",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving receipt images
if os.path.exists(settings.upload_dir):
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

# Include routers
app.include_router(expenses.router)
app.include_router(categories.router)
app.include_router(analytics.router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Smart Expense Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }