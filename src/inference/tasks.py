from src.config.celery import app
from src.inference.dependency import fetch_video_data, predict_watch_time
from src.inference.helpers.task_helpers import update_video_data
from src.inference.schema import ProjectData, VideoData


@app.task
def podcast_data_inference(data: dict):
    project = ProjectData.model_validate(data)

    video_data = fetch_video_data(str(project.url))

    video_data["host_popu_percentage"] = project.host_popularity
    video_data["guest_popu_percentage"] = project.guest_popularity
    video_data["nums_of_ads"] = project.number_of_ads

    validated = VideoData.model_validate(video_data)

    watch_time = predict_watch_time(validated.model_dump())
    video_data["avg_watch_time"] = watch_time
    print(video_data)
    update_video_data(video_data, project.task_id, project.user_id)
