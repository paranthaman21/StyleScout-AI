# 🎯 StyleScout AI - Quick Start Guide

## ✅ All Issues Fixed!

Your MCP server is now properly configured and ready to use.

---

## 🔧 What Was Fixed

### 1. **Working Directory Issue**
- **Before:** Config pointed to project root
- **After:** Config now points to `src` directory
- **File:** `claude_desktop_config.json`

### 2. **Package Configuration**
- **Before:** Incomplete build configuration
- **After:** Added proper setuptools configuration
- **File:** `pyproject.toml`

### 3. **Package Installation**
- **Action:** Reinstalled package in editable mode
- **Command:** `pip install -e .`
- **Result:** Entry point created successfully

---

## 🚀 How to Use

### Step 1: Restart Claude Desktop

**IMPORTANT:** You must completely close and reopen Claude Desktop for changes to take effect.

1. Close Claude Desktop (don't just minimize)
2. Wait 5 seconds
3. Reopen Claude Desktop

### Step 2: Verify Tools Are Available

Look for the 🔌 **tools icon** at the bottom of Claude Desktop.

You should see **4 StyleScout AI tools**:
- ✅ `analyze_outfit`
- ✅ `find_photo_locations`
- ✅ `get_location_details`
- ✅ `suggest_photo_spots`

### Step 3: Try It Out!

**Example 1: Quick Analysis**
```
Upload a photo of your outfit and say:
"Use StyleScout to find photo spots near Chennai within 5km"
```

**Example 2: Detailed Search**
```
Upload your outfit photo and say:
"Analyze my outfit and suggest the best photo locations 
near Chetpet, Tamil Nadu, 606801 within 3km radius"
```

**Example 3: Traditional Outfit**
```
Upload a traditional outfit photo and say:
"Find me heritage sites and temples for photos 
near Anna Nagar, Chennai within 10km"
```

---

## 📋 Current Configuration

### Claude Desktop Config
**Location:** `C:\Users\PARANTHAMAN V\AppData\Roaming\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "stylescout-ai": {
      "command": "python",
      "args": [
        "-m",
        "stylescout_ai.server"
      ],
      "cwd": "D:\\Stylescout AI\\stylescout-ai\\src"
    }
  }
}
```

### Installed Components
- ✅ Python Module: `stylescout_ai`
- ✅ Entry Point: `stylescout-ai.exe`
- ✅ Dependencies: `mcp 1.25.0`, `httpx 0.28.1`

---

## 🧪 Verify Installation

Run this command to test:

```powershell
cd "D:\Stylescout AI\stylescout-ai"
python test_server.py
```

You should see:
```
🎉 All tests passed! The MCP server is ready to use.
```

---

## 🎨 What StyleScout Does

### 1. **Analyzes Your Outfit**
- Style category (Traditional, Formal, Casual, etc.)
- Formality level (1-10)
- Color palette and mood
- Best occasions

### 2. **Finds Perfect Photo Spots**
- Searches nearby locations (5-10km radius)
- Matches locations to your outfit style
- Scores each location (0-100)
- Provides Google Maps links

### 3. **Gives Photography Tips**
- Best time of day for photos
- Recommended angles
- Background suggestions

---

## 📸 Example Outfit → Location Matching

| Your Outfit | StyleScout Finds |
|-------------|------------------|
| **Traditional Saree** | Temples, heritage sites, gardens |
| **Formal Business** | Hotels, museums, corporate buildings |
| **Casual Streetwear** | Cafes, parks, urban art spots |
| **Party/Glamorous** | Rooftop bars, skyline views |
| **Sporty** | Beaches, parks, stadiums |

---

## 🆓 100% Free APIs

StyleScout uses only free APIs:
- ✅ **Nominatim** - Location geocoding
- ✅ **Overpass API** - OpenStreetMap data
- ✅ **Claude Vision** - AI outfit analysis

**No API keys needed!**

---

## ❓ Troubleshooting

### Tools Not Showing in Claude Desktop?

1. **Completely close Claude Desktop** (check Task Manager)
2. **Reopen Claude Desktop**
3. **Wait 10 seconds** for MCP servers to initialize
4. **Look for 🔌 icon** at the bottom

### Still Not Working?

Run the verification:
```powershell
cd "D:\Stylescout AI\stylescout-ai"
python test_server.py
```

If tests fail, reinstall:
```powershell
pip install -e .
```

### Import Errors?

Make sure you're in the right directory:
```powershell
cd "D:\Stylescout AI\stylescout-ai\src"
python -c "import stylescout_ai.server; print('OK')"
```

---

## 📞 Support Commands

### Check if module is installed:
```powershell
pip show stylescout-ai
```

### Check if entry point exists:
```powershell
where stylescout-ai
```

### Check dependencies:
```powershell
pip list | Select-String -Pattern "mcp|httpx"
```

### Reinstall package:
```powershell
cd "D:\Stylescout AI\stylescout-ai"
pip install -e .
```

---

## 🎉 You're All Set!

Your StyleScout AI MCP server is now fully functional and ready to help you find amazing photo locations!

**Next Step:** Restart Claude Desktop and start uploading outfit photos! 📸✨

---

## 💡 Pro Tips

1. **Be specific** - "Red traditional saree" gets better results than just "outfit"
2. **Try different radii** - Start with 5km, expand to 10km if needed
3. **Visit during golden hour** - Sunrise/sunset for best lighting
4. **Scout first** - Check Google Street View before visiting
5. **Combine tools** - Use `analyze_outfit` first, then `find_photo_locations`

---

**Happy Photo Hunting! 📸**
