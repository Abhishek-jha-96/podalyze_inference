from typing import Literal
from pydantic import BaseModel, Field


class VideoData(BaseModel):
    podcast_name: str = Field(..., min_length=1)
    episode_title: str = Field(..., min_length=1)
    episode_length: float = Field(..., ge=0)

    genre: Literal[
        "Health",
        "True Crime",
        "News",
        "Comedy",
        "Business",
        "Lifestyle",
        "Technology",
        "Music",
        "Sports",
        "Education",
    ]

    host_popu_percentage: float = Field(..., ge=0)

    pub_day: Literal[
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]

    pub_day_time: Literal["Morning", "Afternoon", "Evening", "Night"]

    guest_popu_percentage: float = Field(..., ge=0)
    nums_of_ads: int = Field(..., ge=0)

    episode_sentiment: Literal["Positive", "Neutral", "Negative"]
