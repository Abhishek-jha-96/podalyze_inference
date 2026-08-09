import traceback

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.inference.schema import AnalyzeErrorResponse, AnalyzeResponse, ProjectData
from src.inference.tasks import podcast_data_inference


router = APIRouter(tags=["podalyze"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={500: {"model": AnalyzeErrorResponse}},
    status_code=status.HTTP_200_OK,
)
def analyze(data: ProjectData) -> AnalyzeResponse | JSONResponse:
    try:
        args = data.model_dump(mode="json")
        podcast_data_inference.delay(args)
        return AnalyzeResponse(message="Podcast analysis task submitted.")
    except Exception as e:
        print(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content=AnalyzeErrorResponse(
                error=f"An error occurred while processing the video: {str(e)}"
            ).model_dump(),
        )
