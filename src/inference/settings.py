from os import environ


MODEL_DIR = "src/data/"
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


FERNET_KEY = environ.get("FERNET_KEY")
BASE_API_SERVER_URL = environ.get("BASE_API_SERVER_URL")