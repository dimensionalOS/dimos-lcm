"""
Modular LCM to Foxglove WebSocket Bridge

This package provides a modular implementation of the LCM to Foxglove bridge,
split into logical components for better maintainability and organization.
"""

from .bridge import LcmFoxgloveBridge
from .models import TopicInfo, LcmMessage

__all__ = ['LcmFoxgloveBridge', 'TopicInfo', 'LcmMessage']