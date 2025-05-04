import database
import database_manager
import scraper
from utils import _inner_call
from datetime import datetime, date, time, UTC, timedelta

@_inner_call
def normalize_time(time: datetime):
    """
    Normalizes a given datetime object to the nearest hour in UTC.
    If the minute value of the provided datetime is less than 30, the time is 
    rounded down to the start of the current hour. Otherwise, it is rounded up 
    to the start of the next hour. If the time is close to midnight (23:30 or later), 
    it will roll over to the next day at 00:00.
    Args:
        time (datetime): A timezone-aware datetime object in UTC.
    Returns:
        datetime: A new datetime object rounded to the nearest hour in UTC.
    Raises:
        AssertionError: If the provided datetime object is not in UTC.
    """
    assert time.tzinfo == UTC, "All datetime objects in thins project should be provided as UTC."
    if time.minute < 30:
        return datetime(time.year, time.month, time.day, time.hour, 0, 0, 0, UTC)
    else:
        if time.hour == 23:
            return datetime(time.year, time.month, time.day + 1, 0, 0, 0, 0, UTC)
        else:
            return datetime(time.year, time.month, time.day, time.hour + 1, 0, 0, 0, UTC)
       
@_inner_call 
def scrap_data_of_a_song(song: database.Song):
    now = datetime.now(UTC)
    
    yt1_views = scraper.get_youtube_views(song.yt_id1)
    yt2_views = scraper.get_youtube_views(song.yt_id2)
    yt3_views = scraper.get_youtube_views(song.yt_id3)
    nnd_views = scraper.get_niconico_views(song.nnd_id)
    
    t = normalize_time(now)
    return database.SongStats(
        song=song, 
        yt1_views=yt1_views, 
        yt2_views=yt2_views, 
        yt3_views=yt3_views, 
        nnd_views=nnd_views, 
        record_time=t
    )
    
@_inner_call
def scrap_data_for_all_song():
    songs = database.session.query(database.Song).all()
    for song in songs:
        record = scrap_data_of_a_song(song=song)
        database.session.add(record)
        
    database.session.commit()
    
if __name__ == "__main__":
    scrap_data_for_all_song()