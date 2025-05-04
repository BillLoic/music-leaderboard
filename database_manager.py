import database
import scraper
from utils import _inner_call

session = database.session

@_inner_call
def add_singer(name, website=None, x_name=None, developer=None, developer_website=None):
    new_singer = database.Singer(
        name=name,
        website=website,
        x_name=x_name,
        developer=developer,
        developer_website=developer_website
    )
    session.add(new_singer)
    session.commit()
    session.close()
    
@_inner_call
def add_song(name, singer_names, artist_names, yt_id1, yt_id2=None, yt_id3=None, nnd_id=None):
    singers = session.query(database.Singer).filter(database.Singer.name.in_(singer_names)).all()
    artists = session.query(database.Artist).filter(database.Artist.name.in_(artist_names)).all()
    new_song = database.Song(
        title=name,
        singers=singers,
        artists=artists,
        yt_id1=yt_id1,
        yt_id2=yt_id2,
        yt_id3=yt_id3,
        nnd_id=nnd_id
    )
    duration = scraper.get_youtube_duration(yt_id1)
    release_date = min(scraper.get_youtube_release_date(yt_id1), scraper.get_youtube_release_date(yt_id2), 
                       scraper.get_youtube_release_date(yt_id3), scraper.get_niconico_release_date(nnd_id))
    # Set the release date to the earliest of the available dates
    new_song.release_date = release_date
    new_song.duration = duration
    
    session.add(new_song)
    session.commit()
    session.close()
    return new_song
    
@_inner_call
def add_artist(name, website=None, x_name=None, youtube_channel_name=None, nnd_channel_id=None):
    new_artist = database.Artist(
        name=name,
        website=website,
        x_name=x_name,
        youtube_channel_name=youtube_channel_name,
        nnd_channel_id=nnd_channel_id
    )
    session.add(new_artist)
    session.commit()
    session.close()
   
@_inner_call 
def add_song_stats(song_id, yt1_views=None, yt2_views=None, yt3_views=None, nnd_views=None):
    
    new_stats = database.SongStats(
        song_id=song_id,
        yt1_views=yt1_views,
        yt2_views=yt2_views,
        yt3_views=yt3_views,
        nnd_views=nnd_views
    )
    session.add(new_stats)
    session.commit()
    session.close()
    
@_inner_call
def get_singer_by_id(singer_id):
    singer = session.query(database.Singer).filter_by(id=singer_id).first()
    session.close()
    return singer

@_inner_call
def get_song_by_id(song_id):
    
    song = session.query(database.Song).filter_by(id=song_id).first()
    session.close()
    return song

@_inner_call
def latest_stats(song_id):
    
    stats = session.query(database.SongStats).filter_by(song_id=song_id).order_by(database.SongStats.id.desc()).first()
    session.close()
    return stats

@_inner_call
def calculate_hourly_views(song_id):
    latest_stat = latest_stats(song_id)
    secondary_stats = session.query(database.SongStats).filter_by(song_id=song_id).order_by(database.SongStats.id.desc()).offset(1).first()
    when = secondary_stats.record_time
    if latest_stats and secondary_stats:
        yt1_hourly = (latest_stat.yt1_views - secondary_stats.yt1_views)
        yt2_hourly = (latest_stat.yt2_views - secondary_stats.yt2_views)
        yt3_hourly = (latest_stat.yt3_views - secondary_stats.yt3_views)
        nnd_hourly = (latest_stat.nnd_views - secondary_stats.nnd_views)
        return database.HourlyStats(
            song_id=song_id,
            yt1_views=yt1_hourly,
            yt2_views=yt2_hourly,
            yt3_views=yt3_hourly,
            nnd_views=nnd_hourly, 
            record_time=when
        )
    return None

@_inner_call
def calculate_daily_views(song_id, date):
    records = session.query(database.SongStats).filter_by(song_id=song_id).filter(database.SongStats.record_time.date == date)\
        .order_by(database.SongStats.record_time.desc()).all()
        
    last_record = records[0] if records else None
    first_record = records[-1] if records else None
    if last_record and first_record:
        yt1_daily = (last_record.yt1_views - first_record.yt1_views)
        yt2_daily = (last_record.yt2_views - first_record.yt2_views)
        yt3_daily = (last_record.yt3_views - first_record.yt3_views)
        nnd_daily = (last_record.nnd_views - first_record.nnd_views)
        return database.DailyStats(
            song_id=song_id,
            yt1_views=yt1_daily,
            yt2_views=yt2_daily,
            yt3_views=yt3_daily,
            nnd_views=nnd_daily, 
            record_time=date
        )
        
    else:
        print("No secondary record available to calculate.")
        
@_inner_call
def register_singer_dialog():
    name = input("Enter singer name: ")
    website = input("Enter singer website (optional): ")
    x_name = input("Enter singer X account name (optional): ")
    developer = input("Enter developer name (optional): ")
    developer_website = input("Enter developer website (optional): ")

    add_singer(name, website, x_name, developer, developer_website)
   
@_inner_call 
def register_song_dialog():
    title = input("Enter song name: ")
    singer_names = input("Enter singer names (comma separated): ").split(",")
    artist_names = input("Enter artist names (comma separated): ").split(",")
    yt1_url = input("Enter YouTube ID 1: ")
    yt2_url = input("Enter YouTube ID 2 (optional): ")
    yt3_url = input("Enter YouTube ID 3 (optional): ")
    nnd_url = input("Enter NND URL (optional): ")

    add_song(title, singer_names, artist_names, yt1_url, yt2_url, yt3_url, nnd_url)
  
@_inner_call  
def register_artist_dialog():
    name = input("Enter artist name: ")
    website = input("Enter artist website (optional): ")
    x_name = input("Enter artist X account (optional): ")
    youtube_channel = input("Enter artist YouTube channel (optional): ")
    nnd_channel_id = input("Enter NND channel ID (optional): ")

    add_artist(name, website, x_name, youtube_channel, nnd_channel_id)