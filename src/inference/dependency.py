import numpy as np
from src.inference.helpers.NLP_helper import analyze_transcript
from src.inference.utils import make_ftre, load_models
from src.inference.helpers.youtube_helper import YoutubeAPIManager


def fetch_video_data(url):
    youtube_api_manager = YoutubeAPIManager(url)
    result = youtube_api_manager.main()
    if len(result["transcript"]) > 1800:
        analyse_data = result["transcript"][-1800:]
    else:
        analyse_data = result["transcript"]

    nlp_data = analyze_transcript(analyse_data)
    genre = nlp_data["genre"]
    sentiment = nlp_data["sentiment"]
    result["genre"] = genre
    result["sentiment"] = sentiment
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
