from src.config.celery import app
from src.inference.dependency import fetch_video_data, predict_watch_time
from src.inference.helpers.task_helpers import update_video_data


@app.task
def podcast_data_inference(data: dict):
    url = data.get("url")

    host_popularity = data.get("host_popularity")
    guest_popularity = data.get("guest_popularity")
    number_of_ads = data.get("number_of_ads")

    task_id = data.get("task_id")
    user_id = data.get("user_id")

    video_data = fetch_video_data(url)

    video_data["host_popu_percentage"] = host_popularity
    video_data["guest_popu_percentage"] = guest_popularity
    video_data["nums_of_ads"] = number_of_ads
    
    res = predict_watch_time(video_data)
    video_data["avg_watch_time"] = res
    print(video_data)
    update_video_data(video_data, task_id, user_id)