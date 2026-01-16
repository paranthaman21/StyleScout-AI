# 🚀 StyleScout AI - Standalone Usage Guide

You can now run StyleScout AI **without Claude Desktop**! Choose from two options:

---

## 🌐 Option 1: Web Application (Easiest!)

### How to Use:

1. **Open the web app:**
   ```powershell
   cd "D:\Stylescout AI\stylescout-ai"
   start index.html
   ```
   
   Or simply double-click `index.html` in File Explorer!

2. **Fill in the form:**
   - Select your outfit style (Traditional, Casual, Formal, etc.)
   - Set formality level (1-10)
   - Choose color mood (warm, cool, neutral, vibrant)
   - Enter your location (e.g., "Chennai, Tamil Nadu")
   - Set search radius (default: 5km)

3. **Click "Find Photo Spots"**

4. **Get Results:**
   - See top 8 matching locations
   - Each with match score (0-100)
   - Google Maps links for navigation
   - Photography tips

### Features:
- ✅ **No installation needed** - runs in your browser
- ✅ **Beautiful modern UI** - gradient design, smooth animations
- ✅ **100% free** - uses free OpenStreetMap APIs
- ✅ **Instant results** - real-time location search
- ✅ **Mobile friendly** - works on any device

### Screenshot:
The web app has a purple gradient background with a clean card-based interface!

---

## 💻 Option 2: Command-Line Application (Advanced)

### How to Use:

1. **Run the application:**
   ```powershell
   cd "D:\Stylescout AI\stylescout-ai"
   python standalone_app.py
   ```

2. **Choose from the menu:**
   ```
   1. Quick Search (Analyze outfit + Find locations)
   2. Analyze Outfit Only
   3. Find Locations (requires outfit analysis first)
   4. Exit
   ```

3. **Follow the prompts:**
   - Enter path to outfit image (for reference)
   - Describe your outfit style
   - Enter formality level
   - Choose color mood
   - Enter location
   - Set search radius

4. **Get detailed results in terminal:**
   - Outfit profile analysis
   - Top matching locations
   - Match scores
   - Google Maps links
   - Photography tips

### Features:
- ✅ **Interactive menu** - easy to navigate
- ✅ **Detailed output** - comprehensive information
- ✅ **Reusable profiles** - analyze once, search multiple times
- ✅ **Customizable** - adjust all parameters

---

## 📊 Comparison

| Feature | Web App | Command-Line |
|---------|---------|--------------|
| **Ease of Use** | ⭐⭐⭐⭐⭐ Very Easy | ⭐⭐⭐ Moderate |
| **Visual Appeal** | ⭐⭐⭐⭐⭐ Beautiful | ⭐⭐ Basic |
| **Speed** | ⭐⭐⭐⭐⭐ Instant | ⭐⭐⭐⭐ Fast |
| **Customization** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent |
| **Installation** | None needed | Python required |
| **Best For** | Quick searches | Detailed analysis |

---

## 🎯 Example Usage

### Web App Example:

1. Open `index.html`
2. Select "Traditional/Ethnic"
3. Set formality to 8
4. Choose "warm" color mood
5. Enter "Chennai, Tamil Nadu"
6. Click "Find Photo Spots"
7. Get instant results with temples, heritage sites, gardens!

### Command-Line Example:

```powershell
python standalone_app.py
```

```
Choose option: 1
Enter image path: C:\Users\YourName\Pictures\outfit.jpg
Style: Traditional/Ethnic
Formality (1-10): 8
Color mood: warm
Location: Chennai, Tamil Nadu
Radius: 5

Results:
#1 - Kapaleeshwarar Temple (Match: 95/100)
#2 - Santhome Cathedral (Match: 88/100)
...
```

---

## 🆓 Both Options Use Free APIs

- ✅ **Nominatim** - Location geocoding
- ✅ **Overpass API** - OpenStreetMap location data
- ✅ **No API keys needed!**
- ✅ **No rate limits for normal use**

---

## 💡 Tips for Best Results

### 1. **Be Specific with Location**
- ✅ Good: "Anna Nagar, Chennai, Tamil Nadu"
- ✅ Good: "Chetpet, Tamil Nadu, 606801"
- ❌ Too vague: "India"

### 2. **Adjust Search Radius**
- Urban areas: 3-5 km
- Suburban areas: 5-10 km
- Rural areas: 10-20 km

### 3. **Match Style to Venues**
- **Traditional** → Temples, heritage sites, gardens
- **Formal** → Hotels, museums, galleries
- **Casual** → Cafes, parks, urban spots
- **Sporty** → Beaches, parks, stadiums
- **Party** → Rooftop bars, modern architecture

### 4. **Try Different Times**
- Morning: Parks, gardens, temples
- Afternoon: Indoor locations (museums, cafes)
- Evening: Waterfront, rooftops, skyline views

---

## 🔧 Troubleshooting

### Web App Issues:

**"No locations found"**
- Increase search radius
- Try a nearby major city
- Check internet connection

**"Location not found"**
- Use more specific location name
- Try adding state/country
- Use nearby landmark

### Command-Line Issues:

**"Module not found"**
```powershell
cd "D:\Stylescout AI\stylescout-ai"
pip install -e .
```

**"Connection error"**
- Check internet connection
- Try again after a few seconds
- Overpass API might be busy

---

## 🎨 Customization

### Web App:
You can customize the colors by editing `index.html`:
- Line 15-16: Change gradient colors
- Line 60-62: Change button colors
- Line 100-102: Change card colors

### Command-Line:
You can modify `standalone_app.py`:
- Add more venue types
- Adjust scoring algorithm
- Change output format

---

## 📸 Sample Workflow

### For a Traditional Saree Photoshoot:

1. **Open web app** or run command-line app
2. **Select:**
   - Style: Traditional/Ethnic
   - Formality: 8/10
   - Color Mood: Warm
   - Location: Your city
   - Radius: 5km

3. **Get results like:**
   - Ancient temples
   - Heritage monuments
   - Botanical gardens
   - Cultural centers

4. **Visit locations:**
   - Check Google Maps links
   - Get directions
   - Visit during golden hour
   - Take amazing photos! 📸

---

## 🚀 Quick Start Commands

### Web App:
```powershell
cd "D:\Stylescout AI\stylescout-ai"
start index.html
```

### Command-Line:
```powershell
cd "D:\Stylescout AI\stylescout-ai"
python standalone_app.py
```

---

## 📱 Mobile Usage

The web app works on mobile devices too!

1. Copy `index.html` to your phone
2. Open with any browser
3. Use on-the-go to find photo spots!

Or host it on GitHub Pages for easy access anywhere.

---

## 🎉 You're Ready!

Choose your preferred method and start finding amazing photo locations!

**Recommended:** Start with the **Web App** for the best experience! 🌐✨

---

## 📞 Need Help?

- Web app not working? Check browser console (F12)
- Command-line errors? Check Python version (3.10+)
- No results? Try increasing search radius
- Location not found? Use a major city nearby

---

**Happy Photo Hunting! 📸**
