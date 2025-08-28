from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .db.mongo import MongoDB
from .routes import user_routes, menu_routes, order_routes

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(menu_routes.router, prefix=settings.API_V1_PREFIX)
app.include_router(order_routes.router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
async def startup_db_client():
    await MongoDB.connect_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await MongoDB.close_db()

@app.get("/")
async def root():
    return {
        "message": "Welcome to Restaurant Management System API",
        "docs_url": "/docs",
        "openapi_url": f"{settings.API_V1_PREFIX}/openapi.json"
    }
