import database_manager as dm

dm.add_artist(
    name="DECO*27", 
    website="https://otoiro.co.jp", 
    x_name="DECO27", 
    youtube_channel_name="DECO27", 
    nnd_channel_id=811012
)
dm.add_artist(
    name="Satsuki", 
    website="https://32ki-may.myprofolio.com", 
    x_name="32ki_may", 
    youtube_channel_name="32ki_may", 
    nnd_channel_id=88956260
)
dm.add_singer(
    name="Hatsune Miku", 
    website="https://piapro.jp", 
    x_name="cfm_miku", 
    developer="Crypton Future Media Inc.", 
    developer_website="https://crypton.co.jp"
)
dm.add_singer(
    name="Kasane Teto", 
    website="https://https://kasaneteto.jp/", 
    x_name="twindrill_teto", 
    developer="TwinDrill", 
    developer_website="https://kasaneteto.jp"
)
dm.add_song(
    name="Telepathy", 
    singer_names=["Hatsune Miku"], 
    artist_names=["DECO*27"], 
    yt_id1="c56TpxfO9q0", 
    nnd_id="sm44661043"
)

dm.add_song(
    name="Mesmerizer", 
    singer_names=["Hatsune Miku", "Kasane Teto"], 
    artist_names=["Satsuki"], 
    yt_id1="19y8YTbvri8", 
    yt_id2="ibjWftkJrd4", 
    yt_id3="sVCcqC3M1H4", 
    nnd_id="sm43708803"
)