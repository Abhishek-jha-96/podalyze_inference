from fastapi import APIRouter
from fastapi.responses import JSONResponse
import traceback

from src.inference.dependency import fetch_video_data, predict_watch_time
from src.inference.schema import ProjectData


router = APIRouter(tags=["podalyze"])


@router.post("/analyze")
def analyze(data: ProjectData):
    try:
        video_data = fetch_video_data(data.url)
        # res = predict_watch_time(video_data)
        return JSONResponse(status_code=200, content={"video_data": video_data})
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while processing the video: {str(e)}"
            },
        )
