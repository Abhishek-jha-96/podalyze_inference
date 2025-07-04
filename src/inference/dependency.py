from src.inference.utils import make_ftre, load_models

def predict_watch_time(data):
    all_vals = make_ftre(data)

    models = load_models()
    
    predictions = []
    for model in models:
        pred = model.predict(all_vals)
        predictions.append(pred)
    final_prediction = sum(predictions) / len(predictions)

    return final_prediction