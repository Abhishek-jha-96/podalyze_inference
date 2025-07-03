from fastapi import APIRouter

from src.inference.schema import VideoData


router = APIRouter(tags=["podalyze"])


@router.post("/analyze")
def analyze(data: VideoData):
    return {"message": "Data received", "validated_data": data.model_dump()}
