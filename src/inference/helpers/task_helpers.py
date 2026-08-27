from __future__ import annotations

from typing import Any

import httpx

from src.inference.settings import BASE_API_SERVER_URL, INFERENCE_SERVICE_SECRET


def _to_python(value: Any) -> Any:
    """Convert numpy / non-JSON scalars to plain Python types."""
    if hasattr(value, "item"):
        return value.item()
    return value


def build_task_update_payload(video_data: dict) -> dict:
    """
    Map inference output → backend UpdateTaskDto:
    { sentiment?, watchTime?, metaData?, status? }
    """
    meta_data = {
        "podcast_name": video_data.get("podcast_name"),
        "episode_title": video_data.get("episode_title"),
        "episode_length": _to_python(video_data.get("episode_length")),
        "pub_day": video_data.get("pub_day"),
        "pub_day_time": video_data.get("pub_day_time"),
        "genre": video_data.get("genre"),
        "host_popu_percentage": _to_python(video_data.get("host_popu_percentage")),
        "guest_popu_percentage": _to_python(video_data.get("guest_popu_percentage")),
        "nums_of_ads": _to_python(video_data.get("nums_of_ads")),
    }

    return {
        "status": "active",
        "sentiment": video_data.get("episode_sentiment"),
        "watchTime": float(_to_python(video_data["avg_watch_time"])),
        "metaData": meta_data,
    }


def update_video_data(video_data: dict, task_id: str, user_id: str) -> None:
    if not BASE_API_SERVER_URL:
        raise ValueError("BASE_API_SERVER_URL is not configured")
    if not INFERENCE_SERVICE_SECRET:
        raise ValueError("INFERENCE_SERVICE_SECRET is not configured")

    payload = build_task_update_payload(video_data)
    update_url = f"{BASE_API_SERVER_URL.rstrip('/')}/task/{task_id}/inference-result"

    try:
        with httpx.Client(timeout=30.0) as client:
            response = client.patch(
                update_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Inference-Service-Key": INFERENCE_SERVICE_SECRET,
                    "X-User-Id": user_id,
                },
            )
            response.raise_for_status()
    except Exception as e:
        print(f"failed to update the backend for task: {task_id}")
        print(e)
        raise
