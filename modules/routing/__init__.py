"""
Route Optimization Module.

Provides multi-stop route optimization using OpenRouteService (ORS) API
powered by VROOM for TSP/VRP solving. Integrates with the existing
Mapbox GL JS frontend for route visualization.
"""

from .routes import routing_bp

__all__ = ['routing_bp']
