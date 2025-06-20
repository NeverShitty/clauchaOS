"""
Cloude Memory System V3 - Enhanced with OpenAI Assistants

A comprehensive memory system with 11 specialized Cloude instances,
ADHD-aware cognitive support, and automated insights generation.
"""

__version__ = "3.0.0"
__author__ = "YourCompany"

from .cloude_vector_memory_v3_enhanced import CloudeVectorMemoryV3Enhanced
from .cloude_automated_insights_generator import MemoryInsightsGenerator
from .cloude_memory_monitoring_dashboard import MemoryMonitoringSystem

__all__ = [
    "CloudeVectorMemoryV3Enhanced",
    "MemoryInsightsGenerator", 
    "MemoryMonitoringSystem"
]
EOF < /dev/null