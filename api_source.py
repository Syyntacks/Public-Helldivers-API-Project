from fastapi import FastAPI
from pydantic import BaseModel
from utils.parse_conf.planet_data_parser import PlanetParser
from utils.parse_conf.major_order_parser import parse_major_order_data
from utils.parse_conf.galaxy_stats_parser import parse_galaxy_stats
from utils.parse_conf.data_fetcher import fetch_data_from_url
from conf import settings

# Initiation for FastAPI app
app = FastAPI()

"""
    We define endpoints below for users to access. Subject to change.
"""

# All planet data combined
@app.get("/api/planets") 
def get_all_planets():
    print("Request received for all planet data...")
    planet_handler = PlanetParser()
    return planet_handler.get_all_planets()

# Specific planet data
@app.get("/api/planets/{planet_name}")
def get_single_planet(planet_name: str):
    print("Request received for planet {planet_name}...")
    planet_handler = PlanetParser()
    planet = planet_handler.get_planet_by_name(planet_name)
    return planet if planet else {"error": "Planet was not found"}

# Major order data
@app.get("/api/major_orders")
def get_major_orders():
    print("Request received for major orders...")
    major_order_url = settings.url.get("major_order")
    raw_data = fetch_data_from_url(major_order_url)
    if raw_data:
        parsed_orders = parse_major_order_data(raw_data)
        return parsed_orders
    return {"error": "Failed to fetch major order data"}

# Galaxy stats
@app.get("/api/galaxy_stats")
def get_galaxy_stats():
    print("Request received for galaxy stats...")
    galaxy_stats_url = settings.url.get("planet_stats")
    raw_data = fetch_data_from_url(galaxy_stats_url)
    if raw_data:
        galaxy_stats = parse_galaxy_stats(raw_data)
        return galaxy_stats
    return {"error": "Failed to fetch galaxy stats"}