from app.config import DATA_SOURCE
from app.repositories.dashboard_repo_db import DashboardDbRepository
from app.repositories.dashboard_repo_mock import DashboardMockRepository

def get_dashboard_repo():
    if DATA_SOURCE == "mock":
        return DashboardMockRepository()
    retur DashboardDbRepository()