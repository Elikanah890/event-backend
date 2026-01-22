from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Ensure current directory is in PYTHONPATH for reload subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Routers
from app.routers import (
    auth,
    event,
    guest,
    invitations,
    rsvp,
    scan,
    analytics,
    attendance
)

# Create FastAPI app
app = FastAPI(
    title="Professional Event Management System",
    description="Backend API for managing events, invitations, RSVPs, QR scans, attendance, and analytics",
    version="1.0.0"
)

# CORS settings for frontend integration
origins = [
    "http://localhost:8080",  # React dev server
    "https://yourproductiondomain.com"  # Production frontend domain
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include all routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(event.router, prefix="/events", tags=["events"])
app.include_router(guest.router, prefix="/guests", tags=["guests"])
app.include_router(invitations.router, prefix="/invitations", tags=["invitations"])
app.include_router(rsvp.router, prefix="/rsvp", tags=["rsvp"])
app.include_router(scan.router, prefix="/scan", tags=["scan"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(attendance.router, prefix="/attendance", tags=["attendance"])

# Root endpoint
@app.get("/", tags=["root"])
def root():
    return {"message": "Welcome to Professional Event Management System API!"}
