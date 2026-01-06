import os

DATA_SOURCE = os.getenv("DATA_SOURCE", "db") # "db" | "mock"
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Allowlist for autoscan, e.g. "dashboard,incidents"
ENABLED_FEATURES = os.getenv("ENABLED_FEATURES", "")