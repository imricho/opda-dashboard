from app.config import DATA_SOURCE
from app.features.incidents.repo_db import IncidentsDbRepository
from app.features.incidents.repo_mock import IncidentsMockRepository

def get_incidents_repo():
    return IncidentsMockRepository() if DATA_SOURCE == "mock" else IncidentsDbRepository()