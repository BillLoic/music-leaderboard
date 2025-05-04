from logging import * 

basicConfig(
    format="[%(asctime)s %(levelname)s %(filename)s:%(lineno)s] %(message)s"
)

logger = getLogger("music_leaderboard")
logger.addHandler(
    FileHandler("log.txt", encoding="utf8")
)
logger.setLevel(DEBUG)
