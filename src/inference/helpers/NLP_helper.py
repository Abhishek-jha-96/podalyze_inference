from huggingface_hub import InferenceClient
from src.config.configs import settings
from src.inference.settings import GENRES, LABLE_MAP

sentiment_client = InferenceClient("cardiffnlp/twitter-roberta-base-sentiment", token=settings.HF_TOKEN)
genre_client = InferenceClient("facebook/bart-large-mnli", token=settings.HF_TOKEN)

def analyze_transcript(text):
    sentiment = sentiment_client.text_classification(text)
    genre = genre_client.zero_shot_classification(text, candidate_labels=GENRES)
    sentiment = sorted(
        [
            {
                "label": LABLE_MAP.get(item["label"], item["label"]),
                "score": item["score"]
            }
            for item in sentiment
        ],
        key=lambda x: x["score"],
        reverse=True
    )
    top_sentiment = sentiment[0]
    label = top_sentiment.get("label")

    return {
        "sentiment": label,
        "genre": genre[0].label if genre else "Unknown"
    }

