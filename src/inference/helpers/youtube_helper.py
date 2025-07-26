import isodate
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from src.config.configs import settings
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeAPIManager:
    def __init__(self, url: str):
        self.url = url
        self.video_id = self.extract_video_id()
        self.youtube = build("youtube", "v3", developerKey=settings.DEVELOPER_KEY)

        self.title = None
        self.author = None
        self.length = None
        self.publication_data = None
        self.duration = None

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

        duration_seconds = content_details["duration"]

        self.title = snippet["title"]
        self.author = snippet["channelTitle"]
        self.publication_data = snippet["publishedAt"]
        self.length = duration_seconds
    
    def get_duration_in_minutes(self, duration_str: str) -> float:
        self.duration = isodate.parse_duration(duration_str)
        return round(self.duration.total_seconds() / 60, 2)

    def fetch_transcript(self,) -> str:
        try:
            handler = YouTubeTranscriptApi()
            transcript_data = handler.fetch(video_id=self.video_id)
            quater_duration = round(self.duration.total_seconds() / 4)
            filtered_data = [
                        snippet for snippet in transcript_data 
                        if snippet.start <= quater_duration
                    ]
            full_text = ' '.join([snippet.text for snippet in filtered_data])
            return full_text
        except Exception as e:
            print(f"Error: {e}")
            return None

    def main(self,):
        publish_date = self.publication_data
        publish_date = datetime.strptime(publish_date, "%Y-%m-%dT%H:%M:%SZ")
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

        episode_length = self.get_duration_in_minutes(self.length)
        transcript = self.fetch_transcript()


        return {
            "podcast_name": self.author,
            "episode_title": self.title,
            "episode_length": episode_length,  # in minutes
            # "host_popu_percentage": round(random.uniform(50, 100), 2),
            "pub_day": pub_day,
            "pub_day_time": pub_day_time,
            # "guest_popu_percentage": round(random.uniform(0, 50), 2),
            # "nums_of_ads": random.randint(0, 5),
            "transcript": transcript
        }