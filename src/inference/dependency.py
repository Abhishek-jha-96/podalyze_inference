import numpy as np
from src.inference.utils import make_ftre, load_models


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
