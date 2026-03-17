import requests
import logging

logger = logging.getLogger(__name__)

BASE_API = "https://4c7d-47-247-173-78.ngrok-free.app"

def get_hospitals(city: str):
    """
    Fetches real-time hospital data from the backend HMS API for a specific city.
    """
    url = f"{BASE_API}/api/hospitals/?city={city}"
    logger.info(f"API REQUEST | URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        logger.info(f"API RESPONSE | Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            hospitals = data.get("hospitals", [])
            logger.info(f"API DATA | Found {len(hospitals)} hospitals for {city}")
            return data
            
        return None
    except Exception as e:
        logger.error(f"API ERROR | City: {city} | {str(e)}")
        return None
