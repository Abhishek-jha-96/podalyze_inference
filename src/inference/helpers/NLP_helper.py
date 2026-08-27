from huggingface_hub import InferenceClient

from src.config.configs import settings
from src.inference.settings import GENRES, LABLE_MAP

sentiment_client = InferenceClient(
    "cardiffnlp/twitter-roberta-base-sentiment",
    token=settings.HF_TOKEN,
)
genre_client = InferenceClient(
    "facebook/bart-large-mnli",
    token=settings.HF_TOKEN,
)


def _label(item) -> str:
    return item.label if hasattr(item, "label") else item["label"]


def _score(item) -> float:
    return item.score if hasattr(item, "score") else item["score"]


def analyze_transcript(text: str) -> dict:
    sentiment_raw = sentiment_client.text_classification(text)
    genre_raw = genre_client.zero_shot_classification(text, candidate_labels=GENRES)

    sentiment = sorted(
        [
            {
                "label": LABLE_MAP.get(_label(item), _label(item)),
                "score": _score(item),
            }
            for item in sentiment_raw
        ],
        key=lambda x: x["score"],
        reverse=True,
    )
    top_sentiment = sentiment[0]["label"] if sentiment else "Neutral"
    top_genre = _label(genre_raw[0]) if genre_raw else "Unknown"

    return {
        "sentiment": top_sentiment,
        "genre": top_genre,
    }
