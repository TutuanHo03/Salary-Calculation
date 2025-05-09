from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.salary import router as salary_router

import uvicorn

app = FastAPI(
    title="Salary Calculator API",
    description="API for calculating gross to net salary",
    version="1.0.0"
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
app.include_router(salary_router)

# This allows you to run directly with python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
