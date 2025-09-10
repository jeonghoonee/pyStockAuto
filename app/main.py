"""
FastAPI Application Entry Point

This is the main application file for PyStockAuto.
Equivalent to BizStockApplication.kt in the original Kotlin project.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.hello_controller import router as hello_router
from app.controllers.krinvest import router as krinvest_router
from app.controllers.sa import router as sa_router
from app.config.database import init_db
from app.config.settings import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="PyStockAuto",
    description="Python Stock Auto Trading System",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure according to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting PyStockAuto application...")
    await init_db()
    logger.info("Database initialized successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown"""
    logger.info("Shutting down PyStockAuto application...")

# Include routers
app.include_router(hello_router, prefix="/api", tags=["hello"])
app.include_router(krinvest_router, prefix="/api/krinvest", tags=["krinvest"])
app.include_router(sa_router, prefix="/api/sa", tags=["sa"])

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to PyStockAuto - Python Stock Auto Trading System"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "PyStockAuto"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
