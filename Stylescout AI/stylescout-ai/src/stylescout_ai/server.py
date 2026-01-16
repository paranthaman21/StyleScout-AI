import asyncio
import json
import base64
from typing import Any
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
import httpx
from pathlib import Path

# Initialize MCP Server
server = Server("stylescout-ai")

# Outfit analysis prompts and logic
OUTFIT_ANALYSIS_PROMPT = """Analyze this outfit image and provide a detailed assessment:

1. **Formality Level** (1-10): Rate how formal/casual the outfit is
2. **Style Category**: Classify as (Traditional/Ethnic, Formal/Business, Casual, Sporty, Party/Glamorous, Streetwear)
3. **Color Palette**: List dominant colors and their mood
4. **Occasion Suitability**: What occasions is this outfit perfect for?
5. **Best Photo Environments**: What backgrounds/settings would complement this outfit?
6. **Time of Day**: Best time for photos (Golden hour, midday, evening, etc.)
7. **Venue Types**: Specific venue categories that match this style

Respond in JSON format:
{
  "formality_score": 0-10,
  "style_category": "...",
  "colors": ["color1", "color2"],
  "color_mood": "warm/cool/neutral/vibrant",
  "occasions": ["occasion1", "occasion2"],
  "best_environments": ["environment1", "environment2"],
  "best_time": "...",
  "venue_types": ["type1", "type2"],
  "photography_tips": "..."
}"""

# Location matching rules
VENUE_MATCHING = {
    "Traditional/Ethnic": ["temple", "heritage", "cultural_centre", "garden", "park", "monument"],
    "Formal/Business": ["hotel", "restaurant", "museum", "corporate", "convention_centre", "gallery"],
    "Casual": ["cafe", "park", "bookstore", "shopping", "street", "urban", "market"],
    "Sporty": ["beach", "stadium", "park", "sports_complex", "marina", "waterfront"],
    "Party/Glamorous": ["rooftop", "bar", "lounge", "skyline", "modern_architecture", "luxury_hotel"],
    "Streetwear": ["urban", "street_art", "graffiti", "downtown", "skate_park", "industrial"]
}

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools for StyleScout AI"""
    return [
        types.Tool(
            name="analyze_outfit",
            description="Analyze an outfit image to determine style, formality, colors, and suitable locations",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the outfit image file"
                    },
                    "additional_context": {
                        "type": "string",
                        "description": "Optional: Any additional context about the occasion or preferences"
                    }
                },
                "required": ["image_path"]
            }
        ),
        types.Tool(
            name="find_photo_locations",
            description="Find photo-worthy locations near a pincode/area that match an outfit style",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "Location name, pincode, or address (e.g., 'Chetpet, Tamil Nadu, 606801')"
                    },
                    "outfit_profile": {
                        "type": "object",
                        "description": "Outfit analysis results from analyze_outfit tool"
                    },
                    "radius_km": {
                        "type": "number",
                        "description": "Search radius in kilometers (default: 5)",
                        "default": 5
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of locations to return (default: 8)",
                        "default": 8
                    }
                },
                "required": ["location", "outfit_profile"]
            }
        ),
        types.Tool(
            name="get_location_details",
            description="Get detailed information and map links for a specific location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "Name of the location"
                    },
                    "latitude": {
                        "type": "number",
                        "description": "Latitude coordinate"
                    },
                    "longitude": {
                        "type": "number",
                        "description": "Longitude coordinate"
                    }
                },
                "required": ["location_name", "latitude", "longitude"]
            }
        ),
        types.Tool(
            name="suggest_photo_spots",
            description="Complete workflow: Analyze outfit and suggest photo locations in one go",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the outfit image file"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location name, pincode, or address"
                    },
                    "radius_km": {
                        "type": "number",
                        "description": "Search radius in kilometers (default: 5)",
                        "default": 5
                    }
                },
                "required": ["image_path", "location"]
            }
        )
    ]

async def geocode_location(location: str) -> dict:
    """Convert location/pincode to coordinates using Nominatim (FREE)"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": location,
                    "format": "json",
                    "limit": 1
                },
                headers={"User-Agent": "StyleScoutAI/1.0"}
            )
            data = response.json()
            if data:
                return {
                    "latitude": float(data[0]["lat"]),
                    "longitude": float(data[0]["lon"]),
                    "display_name": data[0]["display_name"]
                }
            return None
        except Exception as e:
            return {"error": str(e)}

async def search_nearby_places(lat: float, lon: float, radius_km: float, venue_types: list) -> list:
    """Search for nearby places using Overpass API (FREE OpenStreetMap data)"""
    
    # Convert venue types to OSM tags
    osm_queries = []
    tag_mapping = {
        "temple": "amenity=place_of_worship",
        "heritage": "historic=monument",
        "park": "leisure=park",
        "garden": "leisure=garden",
        "cafe": "amenity=cafe",
        "restaurant": "amenity=restaurant",
        "hotel": "tourism=hotel",
        "museum": "tourism=museum",
        "beach": "natural=beach",
        "waterfront": "natural=water",
        "monument": "historic=monument",
        "gallery": "tourism=gallery"
    }
    
    # Build Overpass query
    query_parts = []
    for venue in venue_types:
        tag = tag_mapping.get(venue, "tourism=attraction")
        query_parts.append(f'node[{tag}](around:{int(radius_km * 1000)},{lat},{lon});')
        query_parts.append(f'way[{tag}](around:{int(radius_km * 1000)},{lat},{lon});')
    
    overpass_query = f"""
    [out:json];
    (
      {' '.join(query_parts)}
    );
    out center 50;
    """
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(
                "https://overpass-api.de/api/interpreter",
                data={"data": overpass_query},
                headers={"User-Agent": "StyleScoutAI/1.0"}
            )
            data = response.json()
            
            places = []
            for element in data.get("elements", []):
                lat_coord = element.get("lat") or element.get("center", {}).get("lat")
                lon_coord = element.get("lon") or element.get("center", {}).get("lon")
                
                if lat_coord and lon_coord:
                    name = element.get("tags", {}).get("name", "Unnamed Location")
                    place_type = element.get("tags", {}).get("amenity") or \
                                element.get("tags", {}).get("tourism") or \
                                element.get("tags", {}).get("leisure") or "attraction"
                    
                    places.append({
                        "name": name,
                        "type": place_type,
                        "latitude": lat_coord,
                        "longitude": lon_coord,
                        "tags": element.get("tags", {})
                    })
            
            return places
        except Exception as e:
            return [{"error": str(e)}]

def score_location(place: dict, outfit_profile: dict) -> float:
    """Score how well a location matches the outfit"""
    score = 50.0  # Base score
    
    style = outfit_profile.get("style_category", "")
    formality = outfit_profile.get("formality_score", 5)
    color_mood = outfit_profile.get("color_mood", "neutral")
    
    place_type = place.get("type", "").lower()
    place_name = place.get("name", "").lower()
    
    # Style matching
    if style == "Traditional/Ethnic":
        if any(x in place_type or x in place_name for x in ["temple", "heritage", "monument", "cultural"]):
            score += 30
        if "park" in place_type or "garden" in place_type:
            score += 20
    
    elif style == "Formal/Business":
        if any(x in place_type for x in ["hotel", "restaurant", "museum"]):
            score += 30
        if formality >= 7:
            score += 10
    
    elif style == "Casual":
        if any(x in place_type for x in ["cafe", "park", "bookstore"]):
            score += 30
    
    elif style == "Sporty":
        if any(x in place_type or x in place_name for x in ["beach", "park", "sports", "stadium"]):
            score += 35
    
    elif style == "Party/Glamorous":
        if any(x in place_name for x in ["rooftop", "skyline", "lounge", "bar"]):
            score += 35
        if formality >= 7:
            score += 10
    
    # Color mood matching
    if color_mood == "warm":
        if any(x in place_name for x in ["sunset", "beach", "garden"]):
            score += 10
    elif color_mood == "cool":
        if any(x in place_name for x in ["water", "lake", "modern"]):
            score += 10
    
    # Bonus for popular/named places
    if place.get("name") and place.get("name") != "Unnamed Location":
        score += 10
    
    return min(score, 100)

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution"""
    
    if name == "analyze_outfit":
        image_path = arguments.get("image_path")
        
        # Read and encode image
        try:
            with open(image_path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode()
            
            # Determine image type
            ext = Path(image_path).suffix.lower()
            mime_type = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp"
            }.get(ext, "image/jpeg")
            
            # Note: In actual MCP usage, Claude will analyze the image
            # This is a placeholder response structure
            analysis_result = {
                "status": "success",
                "message": "Image received. Claude will analyze the outfit.",
                "image_received": True,
                "next_step": "Claude will provide outfit analysis including formality, style, colors, and venue recommendations"
            }
            
            return [
                types.TextContent(
                    type="text",
                    text=json.dumps(analysis_result, indent=2)
                )
            ]
            
        except Exception as e:
            return [types.TextContent(type="text", text=f"Error reading image: {str(e)}")]
    
    elif name == "find_photo_locations":
        location = arguments.get("location")
        outfit_profile = arguments.get("outfit_profile")
        radius_km = arguments.get("radius_km", 5)
        max_results = arguments.get("max_results", 8)
        
        # Geocode location
        coords = await geocode_location(location)
        if not coords or "error" in coords:
            return [types.TextContent(type="text", text=f"Could not geocode location: {location}")]
        
        # Get venue types from outfit profile
        venue_types = outfit_profile.get("venue_types", ["park", "cafe", "monument"])
        
        # Search nearby places
        places = await search_nearby_places(
            coords["latitude"],
            coords["longitude"],
            radius_km,
            venue_types
        )
        
        # Score and sort locations
        scored_places = []
        for place in places:
            if "error" not in place:
                score = score_location(place, outfit_profile)
                place["match_score"] = score
                scored_places.append(place)
        
        scored_places.sort(key=lambda x: x["match_score"], reverse=True)
        top_places = scored_places[:max_results]
        
        # Format results
        result = {
            "location_searched": coords["display_name"],
            "coordinates": {
                "latitude": coords["latitude"],
                "longitude": coords["longitude"]
            },
            "total_found": len(top_places),
            "recommendations": []
        }
        
        for i, place in enumerate(top_places, 1):
            result["recommendations"].append({
                "rank": i,
                "name": place["name"],
                "type": place["type"],
                "match_score": round(place["match_score"], 1),
                "coordinates": {
                    "latitude": place["latitude"],
                    "longitude": place["longitude"]
                },
                "google_maps_link": f"https://www.google.com/maps?q={place['latitude']},{place['longitude']}",
                "why_this_spot": f"Great match for {outfit_profile.get('style_category')} style with {outfit_profile.get('color_mood')} tones"
            })
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_location_details":
        location_name = arguments.get("location_name")
        lat = arguments.get("latitude")
        lon = arguments.get("longitude")
        
        details = {
            "name": location_name,
            "coordinates": {"latitude": lat, "longitude": lon},
            "map_links": {
                "google_maps": f"https://www.google.com/maps?q={lat},{lon}",
                "google_maps_directions": f"https://www.google.com/maps/dir/?api=1&destination={lat},{lon}",
                "google_street_view": f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}",
                "openstreetmap": f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}&zoom=16"
            },
            "photography_tips": [
                "Visit during golden hour (sunrise/sunset) for best lighting",
                "Scout the location beforehand to find best angles",
                "Check weather forecast for clear skies",
                "Consider the background and how it complements your outfit"
            ]
        }
        
        return [types.TextContent(type="text", text=json.dumps(details, indent=2))]
    
    elif name == "suggest_photo_spots":
        # This is a combined workflow
        image_path = arguments.get("image_path")
        location = arguments.get("location")
        radius_km = arguments.get("radius_km", 5)
        
        result = {
            "workflow": "complete",
            "step_1": "Analyze outfit from image",
            "step_2": "Find matching locations",
            "message": "Please provide the outfit analysis, then I'll find the best photo spots!",
            "image_path": image_path,
            "location": location,
            "radius_km": radius_km
        }
        
        return [types.TextContent(type="text", text=json.dumps(result, indent=2))]
    
    else:
        return [types.TextContent(type="text", text=f"Unknown tool: {name}")]

async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="stylescout-ai",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())