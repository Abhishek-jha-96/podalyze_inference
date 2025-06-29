import isodate
import re

from urllib.parse import urlparse, parse_qs


def extract_video_id(url: str) -> str:
    query = urlparse(url)
    if query.hostname == "youtu.be":
        return query.path[1:]
    if query.hostname in ("www.youtube.com", "youtube.com"):
        if query.path == "/watch":
            return parse_qs(query.query)["v"][0]
        elif query.path.startswith("/embed/"):
            return query.path.split("/")[2]
    raise ValueError("Invalid YouTube URL")


def parse_duration(iso_duration):
    duration = isodate.parse_duration(iso_duration)
    return int(duration.total_seconds() / 60)


def extract_guest_name(title_or_description):
    # Very naive heuristic (you can use spaCy or transformers for better NER)
    match = re.search(
        r"(?:with|feat\.?|featuring)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
        title_or_description,
    )
    return match.group(1) if match else None


def estimate_ads(duration_min):
    # Naive assumption: 1 ad per 10 minutes if monetized
    return duration_min // 10


def normalize_popularity(metric, max_metric=10_000_000):
    return round((metric / max_metric) * 100, 2)
