import requests
import json
import logging

def get_request(url: str, headers: dict, params: dict, logger: logging.Logger) -> dict:
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        logger.error('Error connecting to the API.')
        raise
    except requests.exceptions.Timeout:
        logger.error('Request to the API timed out.')
        raise
    except requests.exceptions.HTTPError as e:
        logger.error(f'HTTP error occurred: {e}')
        raise
    except json.JSONDecodeError:
        logger.error('Error decoding the JSON response.')
        raise