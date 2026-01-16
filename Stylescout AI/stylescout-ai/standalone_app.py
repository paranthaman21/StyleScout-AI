"""
StyleScout AI - Standalone Application
Run this directly without Claude Desktop!
"""
import asyncio
import json
import base64
from pathlib import Path
import httpx

# Import the core functions from the server
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))

from stylescout_ai.server import geocode_location, search_nearby_places, score_location

class StyleScoutApp:
    """Standalone StyleScout AI Application"""
    
    def __init__(self):
        self.outfit_profile = None
    
    async def analyze_outfit_simple(self, image_path: str, style_hints: str = None):
        """
        Simplified outfit analysis (without Claude Vision API)
        User provides style information manually
        """
        print("\n" + "="*60)
        print("📸 OUTFIT ANALYSIS")
        print("="*60)
        
        # Check if image exists
        if not Path(image_path).exists():
            print(f"❌ Error: Image not found at {image_path}")
            return None
        
        print(f"✅ Image found: {image_path}")
        print("\nSince we're running standalone, please describe your outfit:")
        
        # Get user input for outfit details
        print("\n1. Style Category:")
        print("   Options: Traditional/Ethnic, Formal/Business, Casual, Sporty, Party/Glamorous, Streetwear")
        style = input("   Your choice: ").strip() or "Casual"
        
        print("\n2. Formality Level (1-10, where 10 is most formal):")
        formality = input("   Your choice: ").strip()
        formality = int(formality) if formality.isdigit() else 5
        
        print("\n3. Color Mood:")
        print("   Options: warm, cool, neutral, vibrant")
        color_mood = input("   Your choice: ").strip() or "neutral"
        
        print("\n4. Dominant Colors (comma-separated):")
        colors_input = input("   Your choice: ").strip() or "blue, white"
        colors = [c.strip() for c in colors_input.split(",")]
        
        # Create outfit profile
        self.outfit_profile = {
            "style_category": style,
            "formality_score": formality,
            "color_mood": color_mood,
            "colors": colors,
            "occasions": ["photoshoot", "social media"],
            "best_environments": ["outdoor", "scenic"],
            "best_time": "golden hour",
            "venue_types": self._get_venue_types(style),
            "photography_tips": f"Best for {style.lower()} style with {color_mood} tones"
        }
        
        print("\n" + "="*60)
        print("✅ OUTFIT PROFILE CREATED")
        print("="*60)
        print(json.dumps(self.outfit_profile, indent=2))
        
        return self.outfit_profile
    
    def _get_venue_types(self, style: str):
        """Get venue types based on style"""
        venue_mapping = {
            "Traditional/Ethnic": ["temple", "heritage", "garden", "park", "monument"],
            "Formal/Business": ["hotel", "restaurant", "museum", "gallery"],
            "Casual": ["cafe", "park", "bookstore", "urban"],
            "Sporty": ["beach", "park", "waterfront"],
            "Party/Glamorous": ["rooftop", "bar", "hotel"],
            "Streetwear": ["urban", "park", "cafe"]
        }
        return venue_mapping.get(style, ["park", "cafe", "monument"])
    
    async def find_locations(self, location: str, radius_km: float = 5, max_results: int = 8):
        """Find photo locations based on outfit profile"""
        if not self.outfit_profile:
            print("❌ Error: Please analyze outfit first!")
            return None
        
        print("\n" + "="*60)
        print("🔍 SEARCHING FOR PHOTO LOCATIONS")
        print("="*60)
        print(f"📍 Location: {location}")
        print(f"📏 Radius: {radius_km} km")
        print(f"🎯 Looking for: {', '.join(self.outfit_profile['venue_types'])}")
        
        # Geocode location
        print("\n⏳ Geocoding location...")
        coords = await geocode_location(location)
        
        if not coords or "error" in coords:
            print(f"❌ Error: Could not find location '{location}'")
            print("💡 Tip: Try using a more specific location or nearby city name")
            return None
        
        print(f"✅ Found: {coords['display_name']}")
        print(f"   Coordinates: {coords['latitude']:.4f}, {coords['longitude']:.4f}")
        
        # Search nearby places
        print(f"\n⏳ Searching for venues within {radius_km}km...")
        places = await search_nearby_places(
            coords["latitude"],
            coords["longitude"],
            radius_km,
            self.outfit_profile["venue_types"]
        )
        
        if not places or (len(places) == 1 and "error" in places[0]):
            print(f"❌ No locations found within {radius_km}km")
            print(f"💡 Tip: Try increasing the radius to 10km or more")
            return None
        
        print(f"✅ Found {len(places)} potential locations")
        
        # Score and sort locations
        print("\n⏳ Scoring locations based on outfit match...")
        scored_places = []
        for place in places:
            if "error" not in place:
                score = score_location(place, self.outfit_profile)
                place["match_score"] = score
                scored_places.append(place)
        
        scored_places.sort(key=lambda x: x["match_score"], reverse=True)
        top_places = scored_places[:max_results]
        
        # Display results
        print("\n" + "="*60)
        print(f"🎯 TOP {len(top_places)} PHOTO LOCATIONS")
        print("="*60)
        
        results = []
        for i, place in enumerate(top_places, 1):
            result = {
                "rank": i,
                "name": place["name"],
                "type": place["type"],
                "match_score": round(place["match_score"], 1),
                "coordinates": {
                    "latitude": place["latitude"],
                    "longitude": place["longitude"]
                },
                "google_maps_link": f"https://www.google.com/maps?q={place['latitude']},{place['longitude']}",
                "google_maps_directions": f"https://www.google.com/maps/dir/?api=1&destination={place['latitude']},{place['longitude']}",
                "why_this_spot": f"Great match for {self.outfit_profile['style_category']} style with {self.outfit_profile['color_mood']} tones"
            }
            results.append(result)
            
            # Print each result
            print(f"\n#{i} - {place['name']}")
            print(f"   Type: {place['type']}")
            print(f"   Match Score: {round(place['match_score'], 1)}/100")
            print(f"   📍 Google Maps: {result['google_maps_link']}")
            print(f"   🧭 Directions: {result['google_maps_directions']}")
            print(f"   💡 Why: {result['why_this_spot']}")
        
        print("\n" + "="*60)
        print("📸 PHOTOGRAPHY TIPS")
        print("="*60)
        print(f"⏰ Best Time: {self.outfit_profile['best_time']}")
        print("💡 Tips:")
        print("   • Visit during golden hour (sunrise/sunset) for best lighting")
        print("   • Scout the location beforehand to find best angles")
        print("   • Check weather forecast for clear skies")
        print("   • Consider the background and how it complements your outfit")
        
        return results
    
    async def quick_search(self, image_path: str, location: str, radius_km: float = 5):
        """Complete workflow: analyze outfit and find locations"""
        print("\n" + "="*60)
        print("🎯 STYLESCOUT AI - QUICK SEARCH")
        print("="*60)
        
        # Analyze outfit
        outfit = await self.analyze_outfit_simple(image_path)
        if not outfit:
            return None
        
        # Find locations
        results = await self.find_locations(location, radius_km)
        
        return results

async def main():
    """Main application entry point"""
    app = StyleScoutApp()
    
    print("\n" + "="*70)
    print("🎯 STYLESCOUT AI - STANDALONE APPLICATION")
    print("="*70)
    print("Find the perfect photo locations based on your outfit!")
    print("="*70)
    
    while True:
        print("\n📋 MENU:")
        print("1. Quick Search (Analyze outfit + Find locations)")
        print("2. Analyze Outfit Only")
        print("3. Find Locations (requires outfit analysis first)")
        print("4. Exit")
        
        choice = input("\nYour choice (1-4): ").strip()
        
        if choice == "1":
            # Quick search
            image_path = input("\n📸 Enter path to outfit image: ").strip()
            location = input("📍 Enter location (e.g., 'Chennai, Tamil Nadu'): ").strip()
            radius = input("📏 Search radius in km (default: 5): ").strip()
            radius_km = float(radius) if radius else 5.0
            
            await app.quick_search(image_path, location, radius_km)
        
        elif choice == "2":
            # Analyze outfit only
            image_path = input("\n📸 Enter path to outfit image: ").strip()
            await app.analyze_outfit_simple(image_path)
        
        elif choice == "3":
            # Find locations only
            if not app.outfit_profile:
                print("\n❌ Error: Please analyze an outfit first (option 1 or 2)")
                continue
            
            location = input("\n📍 Enter location (e.g., 'Chennai, Tamil Nadu'): ").strip()
            radius = input("📏 Search radius in km (default: 5): ").strip()
            radius_km = float(radius) if radius else 5.0
            max_results = input("🎯 Max results (default: 8): ").strip()
            max_results = int(max_results) if max_results.isdigit() else 8
            
            await app.find_locations(location, radius_km, max_results)
        
        elif choice == "4":
            print("\n👋 Thanks for using StyleScout AI!")
            break
        
        else:
            print("\n❌ Invalid choice. Please enter 1-4.")
        
        # Ask if user wants to continue
        continue_choice = input("\n🔄 Continue? (y/n): ").strip().lower()
        if continue_choice != 'y':
            print("\n👋 Thanks for using StyleScout AI!")
            break

if __name__ == "__main__":
    print("\n🚀 Starting StyleScout AI Standalone Application...")
    asyncio.run(main())
