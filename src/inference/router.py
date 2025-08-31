import traceback

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.inference.schema import ProjectData
from src.inference.tasks import podcast_data_inference


router = APIRouter(tags=["podalyze"])


@router.post("/analyze")
def analyze(data: ProjectData):
    try:
        args = data.model_dump()
        podcast_data_inference.delay(args)
        return JSONResponse(status_code=200, content={"message": "Podcast analysis task submitted."})
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={
                "error": f"An error occurred while processing the video: {str(e)}"
            },
        )
