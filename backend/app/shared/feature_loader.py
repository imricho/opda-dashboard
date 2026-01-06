import importlib
import pkgutil
from typing import List, Tuple
from fastapi import FastAPI
from app.config import ENABLED_FEATURES

def _enabled_list() -> List[str]:
    return [x.strip() for x in ENABLED_FEATURES.split(",") if x.strip()]

def register_feature_routers(app: FastAPI, base_package: str = "app.features") -> Tuple[List[str], List[str]]:
    """
    Discover app.features.<feature>.router and include only those in ENABLED_FEATURES.
    Secure-by-default: if ENABLED_FEATURES empty => include nothing.
    """
    enabled = _enabled_list()
    enabled_set = set(enabled)

    if not enabled_set:
        return [], ["(none) ENABLED_FEATURES is empty"]
    
    base = importlib.import_module(base_package)

    included: List[str] = []
    skipped: List[str] = []

    for m in pkgutil.iter_modules(base.__path__):
        if not m.ispkg:
            continue

        feature_name = m.name
        if feature_name not in enabled_set:
            skipped.append(feature_name)
            continue

        module_path = f"{base_package}.{feature_name}.router"
        try:
            mod = importlib.import_module(module_path)
        except Exception as e:
            skipped.append(f"{feature_name} (import error: {e})")
            continue

        router = getattr(mod, "router", None)
        if router is None:
            skipped.append(f"{feature_name} (router not found)")
            continue

        app.include_router(router)
        included.append(feature_name)
    
    return included, skipped