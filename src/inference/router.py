from fastapi import APIRouter
from fastapi.responses import JSONResponse  # <- use this instead
import traceback

from src.inference.dependency import predict_watch_time
from src.inference.schema import VideoData


router = APIRouter(tags=["podalyze"])


@router.post("/analyze")
def analyze(data: VideoData):
    try:
        res = predict_watch_time(data)
        return JSONResponse(status_code=200, content={"watch_time": res})
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while processing the video: {str(e)}"
            },
        )
