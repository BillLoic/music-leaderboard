import pytubefix
import niconico

from utils import _inner_call
from datetime import datetime, UTC

nico_conn = niconico.NicoNico().video

@_inner_call
def get_youtube_views(id):
    try:
        video = pytubefix.YouTube.from_id(id)
        return video.views
    except Exception as e:
        print(f"Error fetching YouTube views: {e}")
        return 0
    
@_inner_call
def get_niconico_views(video_id):
    try:
        video = nico_conn.get_video(video_id)
        return video.count.view
    except Exception as e:
        print(f"Error fetching Niconico views: {e}")
        return 0
    
@_inner_call
def get_youtube_release_date(id):
    try:
        video = pytubefix.YouTube.from_id(id)
        return video.publish_date.astimezone(UTC)
    except Exception as e:
        print(f"Error fetching YouTube release date: {e}")
        return datetime.now(UTC)
   
@_inner_call 
def get_niconico_release_date(video_id):
    try:
        video = nico_conn.get_video(video_id)
        return datetime.fromisoformat(video.registered_at).astimezone(UTC)
    except Exception as e:
        print(f"Error fetching Niconico release date: {e}")
        return datetime.now(UTC)
    
@_inner_call
def get_youtube_duration(id):
    try:
        video = pytubefix.YouTube.from_id(id)
        return video.length
    except Exception as e:
        print(f"Error fetching YouTube duration: {e}")
        return 0