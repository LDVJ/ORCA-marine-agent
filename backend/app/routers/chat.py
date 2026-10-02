from fastapi import APIRouter

router =  APIRouter(
    tags=["chat"],
    prefix="/chat"
)