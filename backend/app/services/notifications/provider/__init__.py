from __future__ import annotations

import os
from .base import NotificationProvider
from .mock import MockProvider
from .whatsapp_cloud import WhatsAppCloudProvider

def get_provider() -> NotificationProvider:
    mode = os.getenv("NOTIF_PROVIDER", "mock").lower()
    if mode == "whatsapp":
        return WhatsAppCloudProvider()
    return MockProvider()