from fastapi import APIRouter, Response

from inference.dependency import predict_watch_time
from src.inference.schema import VideoData


router = APIRouter(tags=["podalyze"])


@router.post("/analyze")
def analyze(data: VideoData):
    try:
        res = predict_watch_time(data)
        return Response(
            status_code=200,
            content={"watch_time": res},
            media_type="application/json"
        )
    except Exception as e:
        return Response(
            status_code=500,
            detail=f"An error occurred while processing the video: {str(e)}"
        )
