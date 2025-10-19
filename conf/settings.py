# From Diveharder API settings.py file
import os
from urllib.parse import unquote

import requests
from dotenv import load_dotenv

if os.path.isfile("./src/cfg/env/.env"):
    load_dotenv("./src/cfg/env/.env")


security = {
    "token": os.environ["SECURITY_TOKEN"],
}

ahgs_api = {
    "request_headers": {
        "Accept-Language": "en-US",
        "User-Agent": "Diveharder API - api.diverharder.com",
    },
    "auth_headers": {
        "Accept-Language": "en-US",
        "User-Agent": "Diveharder API - api.diverharder.com",
        "Authorization": os.environ["SESSION_TOKEN"],
    },
    "time_delay": int(20),
}


base_url = os.environ["BASE_URL"]

war_id_url = base_url + os.environ["WAR_ID"]
war_id_json = requests.get(war_id_url).json()
war_id = war_id_json["id"]

urls = {
    "status": base_url + os.environ["STATUS"],
    "war_info": base_url + os.environ["WAR_INFO"],
    "war_id": war_id_url,
    "galaxy_stats": base_url + os.environ["GALAXY_STATS"],
    "planets": base_url + os.environ["PLANETS"],
    "planet_stats": base_url + os.environ["PLANET_STATS"],
    "major_order": base_url + os.environ["MAJOR_ORDER"],
    "personal_order": base_url + os.environ["PERSONAL_ORDER"],
    "news_feed": base_url + os.environ["NEWS_FEED"],
    "updates": os.environ["STEAM_NEWS"],
    "items": base_url + os.environ["ITEMS"],
    "mission_rewards": base_url + os.environ["MISSION_REWARDS"],
    "store_rotation": base_url + os.environ["STORE_ROTATION"],
    "warbonds": base_url + os.environ["WARBONDS"],
    "warbond_hm": base_url + os.environ["WARBOND_HM"],
    "warbond_sv": base_url + os.environ["WARBOND_SV"],
    "warbond_ce": base_url + os.environ["WARBOND_CE"],
    "warbond_dd": base_url + os.environ["WARBOND_DD"],
    "warbond_pp": base_url + os.environ["WARBOND_PP"],
    "warbond_vc": base_url + os.environ["WARBOND_VC"],
    "warbond_ff": base_url + os.environ["WARBOND_FF"],
    "warbond_ca": base_url + os.environ["WARBOND_CA"],
    "warbond_te": base_url + os.environ["WARBOND_TE"],
    "space_station_1": base_url + os.environ["SPACE_STATIONS"],
    "player_leaderboard": base_url + os.environ["PLAYER_LEADERBOARD"]
}

for i, (key, value) in enumerate(urls.items()):
    urls[key] = unquote(value)
    if "%id" in value:
        urls[key] = urls[key].replace("%id", str(war_id))
