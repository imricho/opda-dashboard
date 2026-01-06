from app.config import DATA_SOURCE
from app.features.dashboard.repo_db import DashboardDbRepository
from app.features.dashboard.repo_mock import DashboardMockRepository

def get_dashboard_repo():
    return DashboardMockRepository() if DATA_SOURCE == "mock" else DashboardDbRepository()