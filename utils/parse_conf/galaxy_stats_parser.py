import json
import time
from utils.parse_conf import datetime_converter

# Stats parser
def parse_galaxy_stats(data):
    #parsed_container = {}

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            print("Error: Received a string that could not be decoded as JSON.")
            return None


    if not isinstance(data, dict):
        print(f"Error: Expected data to be a dictionary, but got {type(data)}")
        return None
    
    datapoint_names = {
        "missionsWon": "Missions Won",
        "missionsLost": "Missions Lost",
        "missionTime": "Total Mission Time (ms)",
        "bugKills": "Terminid Kills",
        "automatonKills": "Automaton Kills",
        "illuminateKills": "Illuminate Kills",
        "bulletsFired": "Total Bullets Fired",
        "bulletsHit": "Total Bullets Hit",
        "timePlayed": "Total Time Played (ms)",
        "deaths": "Total Deaths",
        "revives": "Revives",
        "friendlies": "Friendly Kills",
        "missionSuccessRate": "Mission Success Rate",
        "accurracy": "Accuracy"
    }

    custom_stat_keys = [
        "bugKills", "automatonKills", "illuminateKills", "deaths", "bulletsFired", "bulletsHit"
        ]
    
    remove_stat_keys = [
        "accuracy"
    ]

    try:
        
        overall_stats_dict = data.get("galaxy_stats")

        if not overall_stats_dict:
            return ["No overall stats available."]
        
        formatted_strings = []

        for key, value in overall_stats_dict.items():
            if key in custom_stat_keys or remove_stat_keys:
                continue

            display_name = datapoint_names.get(key, key)

            if key in ["missionSuccessRate", "accuracy"]:
                formatted_strings.append(f"{datapoint_names}: {value}%")
            else:
                formatted_strings.append(f"{datapoint_names}: {value:,}")

        formatted_strings.append("    --------------------")

        missions_won = overall_stats_dict.get("missionsWon", 0)
        missions_lost = overall_stats_dict.get("missionsLost", 0)
        missions_total = missions_won + missions_lost
        missions_won_percent = (missions_won / missions_total) * 100
        formatted_strings.append(f"Missions Won: {missions_won:,}/{missions_total:,} ({missions_won_percent:.3f}%)")

        user_timezone = "America/Toronto"
        mission_time = overall_stats_dict.get("missionTime")
        total_mission_time = datetime_converter.format_duration_from_seconds(mission_time)
        formatted_strings.append(f"Total Mission Time: {total_mission_time}")


        deaths = overall_stats_dict.get("deaths", 0)
        bug_kills = overall_stats_dict.get("bugKills", 0)
        bot_kills = overall_stats_dict.get("automatonKills", 0)
        squid_kills = overall_stats_dict.get("illuminateKills", 0)
        bullets_fired = overall_stats_dict.get("bulletsFired", 0)
        bullets_hit = overall_stats_dict.get("bulletsHit", 0)
        total_kills = bug_kills + bot_kills + squid_kills

        formatted_strings.append(f"\n    {datapoint_names.get("bugKills")}: {bug_kills:,}")
        formatted_strings.append(f"{datapoint_names.get("automatonKills")}: {bot_kills:,}")
        formatted_strings.append(f"{datapoint_names.get("illuminateKills")}: {squid_kills:,}")
        formatted_strings.append(f"Total Kills: {total_kills:,}")
        formatted_strings.append(f"{datapoint_names.get("deaths")}: {deaths:,}")

        if bullets_fired > 0:
            accuracy_percent = (bullets_fired / bullets_hit) * 100 # Stats in API are incorrectly named
            formatted_strings.append(f"Helldivers Accuracy: {accuracy_percent:.3f}%")

        if deaths > 0:
            kd_ratio = total_kills / deaths
            formatted_strings.append(f"Average kills per life: {kd_ratio:.3f}")

        if total_kills > 0:
            bug_percent = (bug_kills / total_kills) * 100
            automaton_percent = (bot_kills / total_kills) * 100
            squid_percent = (squid_kills / total_kills) * 100

            formatted_strings.append("---- Faction Kill Breakdown ----")
            formatted_strings.append(f"    Terminids: {bug_percent:.3f}%")
            formatted_strings.append(f"    Automatons: {automaton_percent:.3f}%")
            formatted_strings.append(f"    Illuminate: {squid_percent:.3f}%")

        

        return formatted_strings

    except Exception as e:
        print(f"An error occurred while parsing galaxy stats: {e}")
        return None