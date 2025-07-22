import random
import numpy as np
from datetime import datetime
from src.inference.utils import make_ftre, load_models
from src.inference.helpers.youtube_helper import YoutubeAPIManager


def fetch_video_data(url):
    youtube_api_manager = YoutubeAPIManager(url)
    # result = youtube_api_manager.main()
    result = youtube_api_manager.fetch_transcript()
    return result


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
