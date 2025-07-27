# map_server.py
from mcp.server.fastmcp import FastMCP
from typing import Dict, List

# Use any geocoding/library you prefer. Here we’ll use geopy for geocoding,
# and a stubbed routing function for demo purposes.
from geopy.geocoders import Nominatim

mcp = FastMCP("Map")

# Geocode an address
@mcp.tool()
def geocode(address: str) -> Dict[str, float]:
    """Return {'latitude': float, 'longitude': float} for the given address."""
    geolocator = Nominatim(user_agent="map_mcp_adapter")
    loc = geolocator.geocode(address)
    if loc is None:
        raise ValueError(f"Could not geocode '{address}'")
    return {"latitude": loc.latitude, "longitude": loc.longitude}

# Get simple step‑by‑step directions (stubbed)
@mcp.tool()
def get_directions(start: str, end: str) -> List[str]:
    """
    Return a list of direction steps from start to end.
    (In production, hook into OSRM / Google Maps / Mapbox directions API.)
    """
    # Here we just fake a couple of steps
    return [
        f"1. Head north from {start}",
        "2. Turn right onto Main St",
        f"3. Continue until you reach {end}",
        "4. You have arrived."
    ]

if __name__ == "__main__":
    # You can also expose via streamable-http by changing transport
    mcp.run(transport="stdio")
