# 🎯 StyleScout AI: Product Documentation

## 🌟 Overview
**StyleScout AI** is a cutting-edge aesthetic recommendation engine designed to bridge the gap between fashion and photography. By analyzing a user's outfit—specifically its style, formality, and color palette—the platform identifies the most visually compatible photography locations in their immediate vicinity.

Whether you are an influencer, a professional photographer, or someone who just wants better Instagram photos, StyleScout AI eliminates the "where should we shoot?" guesswork.

---

## 🚀 Core Features

### 1. **Magic Scan™ Image Analysis**
Users can upload photos of their outfits directly. The application uses a custom browser-based algorithm to "scan" the image pixels, identifying the dominant color tones to automatically suggest a "Color Mood" (Warm, Cool, Vibrant, or Neutral).

### 2. **Smart Style Matching**
The engine uses a weighted scoring algorithm to match outfit categories with specific venue types:
*   **Traditional/Ethnic**: Prioritizes temples, heritage sites, and monuments.
*   **Formal/Business**: Prioritizes upscale hotels, museums, and galleries.
*   **Casual/Streetwear**: Prioritizes urban art, cafes, and parks.
*   **Sporty**: Prioritizes beaches, stadiums, and waterfronts.

### 3. **Triple-Mirror Location Search**
Powered by OpenStreetMap and the Overpass API, StyleScout searches for real-world locations within a user-defined radius (up to 50km). It uses a "Triple Mirror" system to ensure that if one map server is busy, the app automatically fails over to another, ensuring 99.9% uptime.

### 4. **Photography Pro-Tips**
For every recommended spot, the app provides tailored advice:
*   **Best Time to Visit**: Suggestions for "Golden Hour" or midday lighting.
*   **Direct Navigation**: Instant links to Google Maps and Directions.
*   **Aesthetic Reasoning**: Explains *why* the spot matches the outfit (e.g., "The warm tones of this park complement your red saree").

---

## 💎 Why This is Useful

### **For Content Creators & Influencers**
*   **Efficiency**: Find 5-10 shoot locations in seconds rather than hours of manual searching.
*   **Consistency**: Ensure your outfit "vibe" matches the background for a more professional-looking feed.

### **For Travelers**
*   **Local Exploration**: Discover hidden heritage sites or "hidden gem" cafes in new cities that you wouldn't find on standard travel guides.

### **For Privacy-Conscious Users**
*   **Zero Server Uploads**: Unlike other AI tools, StyleScout processes images locally in the user's browser. Your photos never leave your device.

---

## 🛠️ Technical Architecture

*   **Frontend**: HTML5, Vanilla CSS3 (Modern UI/UX), and ES6+ JavaScript.
*   **Data APIs**: 
    *   **Nominatim**: For accurate geocoding of addresses and pincodes.
    *   **Overpass API**: For real-world OpenStreetMap feature extraction.
*   **Intelligence**: Manual style classification combined with Canvas-based RGB pixel analysis for color mood detection.

---

## 📂 Project Structure

```text
stylescout-ai/
├── index.html          <-- The main production web application
├── standalone_app.py     <-- Command-line version for developers
├── README.md             <-- Quick-start guide
├── DOCUMENTATION.md      <-- This file (the product blueprint)
├── pyproject.toml        <-- Configuration for MCP server usage
└── src/                  <-- Core logic for advanced AI integrations
```

---

## 📈 Future Roadmap
*   **Weather Integration**: Automatically filter out outdoor spots if rain is detected in the location.
*   **Crowd Density Prediction**: Use historical data to suggest the quietest times for a shoot.
*   **Full AI Vision**: Integrating deeper vision models to detect specific clothing items (e.g., "denim jacket") for even more granular spot matching.

---

## ⚖️ License & Privacy
*   **Privacy**: 100% Client-side processing.
*   **Open Source**: Built using OpenStreetMap data under the ODbL license.

---

**Developed with ✨ for the modern creator.**
