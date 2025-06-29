import datetime

from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.config.configs import settings

from src.inference.utils import (
    estimate_ads,
    extract_guest_name,
    extract_video_id,
    normalize_popularity,
    parse_duration,
)


youtube = build("youtube", "v3", developerKey=settings.API_KEY)


def get_video_data(video_id):
    res = (
        youtube.videos()
        .list(part="snippet,contentDetails,statistics", id=video_id)
        .execute()
    )

    if not res["items"]:
        raise ValueError("Video not found")

    return res["items"][0]


def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([entry["text"] for entry in transcript])
    except TranscriptsDisabled:
        return ""


def get_sentiment_score(text):
    if not text.strip():
        return "Neutral"
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    if score["compound"] >= 0.2:
        return "Positive"
    elif score["compound"] <= -0.2:
        return "Negative"
    else:
        return "Neutral"


def get_genre(tags_or_desc):
    genres = [
        "comedy",
        "tech",
        "business",
        "health",
        "news",
        "education",
        "sports",
        "music",
    ]
    lower_text = " ".join(tags_or_desc).lower()
    for genre in genres:
        if genre in lower_text:
            return genre.capitalize()
    return "Unknown"


def get_podcast_info(youtube_url):
    video_id = extract_video_id(youtube_url)
    video_data = get_video_data(video_id)

    snippet = video_data["snippet"]
    stats = video_data["statistics"]
    content = video_data["contentDetails"]

    podcast_name = snippet["channelTitle"]
    episode_title = snippet["title"]
    episode_length = parse_duration(content["duration"])
    genre = get_genre(snippet.get("tags", []) + [snippet.get("description", "")])

    host_popularity = normalize_popularity(int(stats.get("viewCount", 0)))
    published_at = snippet["publishedAt"]
    pub_datetime = datetime.datetime.fromisoformat(published_at.replace("Z", "+00:00"))

    publication_day = pub_datetime.strftime("%A")
    publication_time = pub_datetime.strftime("%H:%M")

    guest_name = extract_guest_name(episode_title + snippet.get("description", ""))
    guest_popularity = normalize_popularity(
        500_000 if guest_name else 0
    )  # Replace with actual logic if needed

    number_of_ads = estimate_ads(episode_length)

    transcript = get_transcript(video_id)
    episode_sentiment = get_sentiment_score(transcript)

    return [
        podcast_name,
        episode_title,
        episode_length,
        genre,
        host_popularity,
        publication_day,
        publication_time,
        guest_popularity,
        number_of_ads,
        episode_sentiment,
    ]


# === Run Example ===
if __name__ == "__main__":
    podcast_url = input("Enter a YouTube podcast URL: ").strip()
    data = get_podcast_info(podcast_url)

    headers = [
        "Podcast_Name",
        "Episode_Title",
        "Episode_Length_minutes",
        "Genre",
        "Host_Popularity_percentage",
        "Publication_Day",
        "Publication_Time",
        "Guest_Popularity_percentage",
        "Number_of_Ads",
        "Episode_Sentiment",
    ]

    print("\nExtracted Podcast Info:")
    for h, d in zip(headers, data):
        print(f"{h}: {d}")
