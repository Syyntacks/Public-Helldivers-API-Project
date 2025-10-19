import json
from typing import Dict, Any, Union, List
from utils.parse_conf.data_fetcher import fetch_data_from_url
from conf import settings

PLANETS_URL: str = settings.url.get("planets")
PLANET_DETAILS_URL: str = settings.url.get("planet_stats")
PLANET_STATUS_URL: str = settings.url.get("status")

class PlanetParser():
    """
        Handles all functions regarding all planets
        on the Galactic Map.
        \n3 sources combined.
    """

    def __init__(self):
        self.combined_data: Dict[int, Dict[str, Any]] = {} # Return for better understanding
        self._fetch_and_combine()
    

    def _fetch_and_combine(self):
        # Creates one dictionary from API endpoints
        planets_data = fetch_data_from_url(PLANETS_URL)
        details_data = fetch_data_from_url(PLANET_DETAILS_URL)
        status_data = fetch_data_from_url(PLANET_STATUS_URL)

        if not planets_data or not details_data or not status_data:
            print("\nCould not combine data due to fetching errors.")
            return
        
        # Dictionary Comprehension --> for further reference
        planets_dict = {planet['index']: planet for planet in planets_data}
        details_dict = {detail['planetIndex']: detail for detail in details_data}
        status_planets_dict = {status['statusIndex']: status for status in status_data}

        # Combine data
        for index, planet_detail in planets_dict.items():
            details = details_dict.get(index, {}) # Get planet details
            status = status_planets_dict.get(index, {}) # Get stats of planet

            # Labelling
            self.combined_data[index] = {
                # planets
                'index': index,
                'name': details.get('name', 'Unknown'),
                'sector': details.get('sector', 'Unknown Sector'),
                'type': details.get('type', 'Unknown Type'),
                'biome': details.get('biome', {}).get('name', 'Unknown Biome'),
                'description': planet_detail.get('biome', {}).get('description', 'No Description'),
                'environName': [env.get('name') for env in planet_detail.get('environmentals', [])],
                'environDesc': [env.get('description') for env in planet_detail.get('environmentals', [])],
                'weatherEffects': planet_detail.get('weather_effects'),
                
                # status
                'players': status.get('players', 0),
                'owner': status.get('owner', 'N/A'),

                # planet_stats/planets_stats
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
                "friendlies": "Friendly Kills",
                "missionSuccessRate": "Mission Success Rate",

            }
    
    #### Return all planet stats and create the ability to search by planet name

    def return_all_planets(self):
        return self.combined_data
    
    def search_by_planet_name(self, planet_name: str):
        for planet in self.combined_data.values():
            if planet.get('name', '').lower() == planet_name.lower():
                return planet
        return None