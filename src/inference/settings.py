from os import environ


MODEL_DIR = "src/models/"
GENRES = ["Health",
        "True Crime",
        "News",
        "Comedy",
        "Business",
        "Lifestyle",
        "Technology",
        "Music",
        "Sports",
        "Education",]

LABLE_MAP = {
        "LABEL_0": "Negative",
        "LABEL_1": "Neutral",
        "LABEL_2": "Positive"
    }


BASE_API_SERVER_URL = environ.get("BASE_API_SERVER_URL")
INFERENCE_SERVICE_SECRET = environ.get("INFERENCE_SERVICE_SECRET")
