import random
import numpy as np
from datetime import datetime
from src.inference.utils import make_ftre, load_models


def fetch_video_data(url):
    yt = YouTube(url)

    publish_date = yt.publish_date or datetime.now()
    pub_day = publish_date.strftime("%A")
    hour = publish_date.hour

    if hour < 12:
        pub_day_time = "Morning"
    elif hour < 17:
        pub_day_time = "Afternoon"
    elif hour < 21:
        pub_day_time = "Evening"
    else:
        pub_day_time = "Night"

    episode_sentiment = random.choice(["Positive", "Neutral", "Negative"])
    genre = random.choice([
        "Health", "True Crime", "News", "Comedy", "Business",
        "Lifestyle", "Technology", "Music", "Sports", "Education"
    ])

    return fetch_video_data(
        podcast_name=yt.author,
        episode_title=yt.title,
        episode_length=yt.length / 60,  # minutes
        genre=genre,
        host_popu_percentage=random.uniform(50, 100),  # Placeholder
        pub_day=pub_day,
        pub_day_time=pub_day_time,
        guest_popu_percentage=random.uniform(0, 50),  # Placeholder
        nums_of_ads=random.randint(0, 5),  # Placeholder
        episode_sentiment=episode_sentiment,
    )



def predict_watch_time(data):
    all_vals = make_ftre(data)

    models = load_models()

    predictions = []
    for model in models:
        pred = model.predict(all_vals)[0]
        print("the time prediciton:", pred)
        predictions.append(pred)

    average_prediction = np.mean(predictions)

    return average_prediction
