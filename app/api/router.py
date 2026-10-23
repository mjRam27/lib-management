"""Aggregates all endpoint routers under the versioned API prefix."""

from fastapi import APIRouter

from app.api.endpoints import books, health, loans, members

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(books.router)
api_router.include_router(members.router)
api_router.include_router(loans.router)
