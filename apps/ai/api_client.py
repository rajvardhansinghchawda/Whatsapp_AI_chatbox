import requests
import logging

logger = logging.getLogger(__name__)

BASE_API = "https://4c7d-47-247-173-78.ngrok-free.app"

HEADERS = {
    "ngrok-skip-browser-warning": "true",
    "Accept": "application/json"
}


def search_hospitals(city: str = None, search: str = None) -> list:
    """
    Search hospitals using the public /api/hospitals/search/ endpoint.
    Supports filtering by city name or free-text search.
    Returns a list of hospital dicts.
    """
    params = {}
    if city:
        params["city"] = city
    if search:
        params["search"] = search

    url = f"{BASE_API}/api/hospitals/search/"
    logger.info(f"API REQUEST | GET {url} | params={params}")

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        logger.info(f"API RESPONSE | Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            hospitals = data.get("results", [])
            logger.info(f"API DATA | Found {len(hospitals)} hospitals")
            return hospitals
        else:
            logger.warning(f"API FAILURE | Status: {response.status_code} | Body: {response.text[:200]}")
            return []
    except Exception as e:
        logger.error(f"API ERROR | {type(e).__name__}: {e}")
        return []


def get_hospital_by_id(hospital_id: str) -> dict:
    """
    Get a specific hospital by ID using /api/hospitals/<id>/.
    """
    url = f"{BASE_API}/api/hospitals/{hospital_id}/"
    logger.info(f"API REQUEST | GET {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        logger.error(f"API ERROR | {type(e).__name__}: {e}")
        return {}


def get_bed_availability(hospital_id: str) -> dict:
    """
    Get bed availability for a hospital using /api/beds/availability/<hospital_id>/.
    Returns dict with total_beds, available_beds, occupied_beds, by_type.
    """
    url = f"{BASE_API}/api/beds/availability/{hospital_id}/"
    logger.info(f"API REQUEST | GET {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception as e:
        logger.error(f"API ERROR | {type(e).__name__}: {e}")
        return {}


def get_service_categories() -> list:
    """
    Get all service categories from /api/hospitals/service-categories/.
    """
    url = f"{BASE_API}/api/hospitals/service-categories/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    except Exception as e:
        logger.error(f"API ERROR | {type(e).__name__}: {e}")
        return []


def get_services() -> list:
    """
    Get all services from /api/hospitals/services/.
    """
    url = f"{BASE_API}/api/hospitals/services/"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            return response.json().get("results", [])
        return []
    except Exception as e:
        logger.error(f"API ERROR | {type(e).__name__}: {e}")
        return []
