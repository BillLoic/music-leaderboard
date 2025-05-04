from sqlalchemy import (
    create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Date, Float, Table, inspect, UniqueConstraint
)
from sqlalchemy.orm import (DeclarativeBase, sessionmaker, relationship)
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime, date, time, UTC, timedelta
import atexit
import pprint
import logger

class Base(DeclarativeBase):
    pass

class wrapped:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.logger.info(
            f"Created instance {self.__class__.__qualname__} \n\targs: {pprint.pformat(args)} \n\tkwargs: {pprint.pformat(kwargs)}"
        )

YOUTUBE_USER_COUNT = 2500000000
NND_USER_COUNT = 140000000

#engine = create_engine("postgresql+psycopg://postgres@localhost:5432/music_leaderboard")
engine = create_engine("sqlite:///music_leaderboard.db") # Use SQLite for simplicity testing

artist_song_association = Table(
    'artist_song_association', Base.metadata,
    Column('artist_id', Integer, ForeignKey('artists.id'), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.id'), primary_key=True)
)

singer_song_association = Table(
    'singer_song_association', Base.metadata,
    Column('singer_id', Integer, ForeignKey('singers.id'), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.id'), primary_key=True)
)

class Song(Base, wrapped):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    title = Column(String, nullable=False)
    release_date = Column(DateTime, nullable=True)
    duration = Column(Float, nullable=True)  # Duration in seconds
    stats = relationship('SongStats', back_populates='song')
    
    daily_stats = relationship('DailyStats', back_populates='song')
    hourly_stats = relationship('HourlyStats', back_populates='song')
    
    artists = relationship('Artist', secondary=artist_song_association, back_populates='songs')
    singers = relationship('Singer', secondary=singer_song_association, back_populates='songs')
    
    yt_id1 = Column(String(11), nullable=False)
    yt_id2 = Column(String(11), nullable=True)
    yt_id3 = Column(String(11), nullable=True)
    
    nnd_id = Column(String(10), nullable=True)
    
    def __repr__(self):
        return f"<Song(id={self.id}, title='{self.title}', release_date='{self.release_date}', duration={self.duration}')>"
    
class Artist(Base, wrapped):
    __tablename__ = 'artists'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    songs = relationship('Song', secondary=artist_song_association, back_populates='artists')
    website = Column(String, nullable=True)
    x_name = Column(String, nullable=True) # Format: https://x.com/<name>
    youtube_channel_name = Column(String, nullable=True) # Format: https://www.youtube.com/@channel_name
    nnd_channel_id = Column(Integer, nullable=True)
    
    def __repr__(self):
        return f"<Artist(id={self.id}, name='{self.name}')>"
    
class Singer(Base, wrapped):
    __tablename__ = 'singers'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    songs = relationship('Song', secondary=singer_song_association, back_populates='singers')
    website = Column(String, nullable=True)
    x_name = Column(String, nullable=True)
    developer = Column(String, nullable=True)
    developer_website = Column(String, nullable=True)
    
    def __repr__(self):
        return f"<Singer(id={self.id}, name='{self.name}')>"
    
class SongStats(Base, wrapped):
    __tablename__ = 'song_stats'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    song = relationship('Song', back_populates='stats')
    
    yt1_views = Column(Integer, nullable=True)
    yt2_views = Column(Integer, nullable=True, default=0)
    yt3_views = Column(Integer, nullable=True, default=0)
    
    nnd_views = Column(Integer, nullable=True, default=0)
    
    record_time = Column(DateTime, nullable=False)
    
    __table_args__ = (
        UniqueConstraint("song_id", record_time), 
    )
    def __repr__(self):
        return f"<SongStats(id={self.id}, song_id={self.song_id}, views={self.views})>"
    
    @property
    def views(self):
        return {
            'yt1': self.yt1_views,
            'yt2': self.yt2_views,
            'yt3': self.yt3_views,
            'nnd': self.nnd_views
        }
        
    @property
    def youtube_views(self):
        return self.yt1_views + self.yt2_views + self.yt3_views
    
    @property
    def total_views(self):
        return self.youtube_views + self.nnd_views
    
    def calc_score(self):
        # Calculate the score based on views and actual user counts
        score = self.youtube_views / YOUTUBE_USER_COUNT + self.nnd_views / NND_USER_COUNT
        return score * 100
    
class HourlyStats(Base, wrapped):
    __tablename__ = 'hourly_stats'
    id = Column(Integer, primary_key=True, autoincrement=True, default=1, nullable=False, unique=True)
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    song = relationship('Song', back_populates='hourly_stats')
    
    yt1_views = Column(Integer, nullable=True)
    yt2_views = Column(Integer, nullable=True, default=0)
    yt3_views = Column(Integer, nullable=True, default=0)
    
    nnd_views = Column(Integer, nullable=True, default=0)
    
    record_time = Column(DateTime, nullable=False, default=datetime.now(UTC))
    
    def __repr__(self):
        return f"<HourlyStats(id={self.id}, song_id={self.song_id}, views={self.views} record_time={self.record_time})>"
    
class DailyStats(Base, wrapped):
    __tablename__ = 'daily_stats'
    id = Column(Integer, primary_key=True, autoincrement=True, default=1, nullable=False, unique=True)
    song_id = Column(Integer, ForeignKey('songs.id'), nullable=False)
    song = relationship('Song', back_populates='daily_stats')
    
    yt1_views = Column(Integer, nullable=True)
    yt2_views = Column(Integer, nullable=True, default=0)
    yt3_views = Column(Integer, nullable=True, default=0)
    
    nnd_views = Column(Integer, nullable=True, default=0)
    
    record_time = Column(Date, nullable=False)
    
    def __repr__(self):
        return f"<DailyStats(id={self.id}, song_id={self.song_id}, views={self.views} record_time={self.record_time})>"
    
if not database_exists(engine.url):
    create_database(engine.url)
    
Base.metadata.create_all(engine)
    
Session = sessionmaker(bind=engine)
session = Session()

atexit.register(session.close_all)