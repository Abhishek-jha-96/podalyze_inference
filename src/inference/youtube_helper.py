from datetime import datetime
from urllib.parse import urlparse, parse_qs
from src.config.configs import settings
from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build

class YoutubeAPIManager:
    def __init__(self, url: str):
        self.url = url
        self.video_id = self.extract_video_id()
        self.youtube = build("youtube", "v3", developerKey=settings.DEVELOPER_KEY)

        self.title = None
        self.author = None
        self.length = None
        self.publication_data = None

        self.fetch_video_metadata()
    
    def extract_video_id(self,) -> str:
        query = urlparse(self.url)
        if query.hostname == "youtu.be":
            return query.path[1:]
        elif "youtube" in query.hostname:
            return parse_qs(query.query).get("v", [""])[0]
        return ""
    
    def fetch_video_metadata(self, ):
        response = self.youtube.videos().list(
            part="snippet,contentDetails",
            id=self.video_id
        ).execute()

        item = response["items"][0]
        snippet = item["snippet"]
        content_details = item["contentDetails"]

        # duration_seconds = isodate.parse_duration(content_details["duration"]).total_seconds()
        duration_seconds = content_details["duration"]

        self.title = snippet["title"]
        self.author = snippet["channelTitle"]
        self.publication_data = snippet["publishedAt"]
        self.length = duration_seconds
    
    def list_captions(self,):
        results = self.youtube.captions().list(
            part="snippet",
            videoId=self.video_id
        ).execute()

        return results["items"]
    
    def fetch_transcript(self, lang: str = "en"):
        transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
        transcript = transcript_list.find_transcript([lang])
        return transcript.fetch()    

    def main(self,):
        publish_date = self.publication_data
        pub_day = publish_date.strftime("%A")
        hour = publish_date.hour

        if hour < 12:
            pub_day_time = "Morning"
        elif hour < 17:
            pub_day_time = "Afternoon"
        elif hour < 21:
            pub_day_time = "Evening"
        else:
            pub_day_time = "Night"

        transcript = self.fetch_transcript()
        captions = self.list_captions()

        return {
            "podcast_name": self.author,
            "episode_title": self.title,
            "episode_length": round(self.length / 60, 2),  # in minutes
            # "genre": genre,
            # "host_popu_percentage": round(random.uniform(50, 100), 2),
            "pub_day": pub_day,
            "pub_day_time": pub_day_time,
            # "guest_popu_percentage": round(random.uniform(0, 50), 2),
            # "nums_of_ads": random.randint(0, 5),
            # "episode_sentiment": episode_sentiment,
            "captions": captions,
            "transcript": transcript
        }