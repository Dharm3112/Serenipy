# 🌿 Serenipy: The Quiet Route Finder

**Serenipy** is a geospatial web application that prioritizes **peace over speed**. While standard navigation apps (Google Maps, Waze) optimize for the shortest travel time, Serenipy uses graph theory and OpenStreetMap data to find the **quietest walking route** between two locations anywhere in the world.

[Image of project workflow diagram]

## 🚀 Key Features

  * **Global Coverage:** Works for any two addresses on Earth (optimized for walking distances \<10km).
  * **Dual Routing Engine:**
      * 🔴 **Fast Route:** Calculates the standard shortest path (Dijkstra's Algorithm based on distance).
      * 🟢 **Quiet Route:** Calculates the path of least stress (Dijkstra's Algorithm based on "Quiet Scores").
  * **Greenery Detection:** Algorithms automatically prefer parks, footpaths, and gardens over main roads.
  * **Interactive UI:** Built with **Streamlit** for a responsive, dark-mode friendly web interface.
  * **Smart Caching:** Optimizes map downloads to prevent API throttling.

## 🛠️ Tech Stack

  * **Python:** Core logic.
  * **OSMnx:** For downloading and constructing street networks from OpenStreetMap.
  * **NetworkX:** For performing complex graph pathfinding algorithms.
  * **Folium:** For generating interactive, tile-based maps.
  * **Streamlit:** For the frontend web interface.

## 📂 Project Structure

```text
Serenipy/
│
├── app.py              # The Main Application (Streamlit UI)
├── map_engine.py       # The Logic Core (Map downloading, routing algorithms)
├── config.py           # Configuration (Noise weights, park bonuses)
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

## ⚙️ Installation Guide

Follow these steps to set up the project locally.

### 1\. Clone the Repository

```bash
git clone https://github.com/your-username/serenipy.git
cd serenipy
```

### 2\. Set up Virtual Environment (Recommended)

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ How to Run

1.  Ensure your virtual environment is active.
2.  Run the Streamlit app:
    ```bash
    streamlit run app.py
    ```
3.  A new tab will open in your browser at `http://localhost:8501`.

## 🎮 Usage

1.  **Enter Locations:** In the left sidebar, type a Start Location (e.g., *"Times Square, New York"*) and a Destination (e.g., *"Bryant Park, New York"*).
2.  **Be Specific:** For best results, include the city name to help the geocoder.
3.  **Find Route:** Click the **"Find Quiet Route"** button.
4.  **Wait:** The app will download live map data (taking 10-30 seconds depending on area size).
5.  **Explore:** Compare the **Red Line** (Fast) with the **Green Line** (Quiet) on the interactive map.

## 🧠 How It Works (The Logic)

Serenipy assigns a "Noise Cost" to every street edge in the graph based on `config.py`:

  * **High Cost (Avoid):** Highways, Primary Roads, Trunks.
  * **Low Cost (Prefer):** Residential streets, Living streets.
  * **Bonus (Target):** Parks, Footways, Cycle paths (Cost multiplied by `0.4`).

<!-- end list -->

```python
# Simplified Logic Example
if road_type == 'highway':
    cost = length * 10.0  # Very expensive to walk here
elif road_type == 'park_path':
    cost = length * 0.4   # Very cheap (attractive) to walk here
```

## 🔮 Future Roadmap

  * [ ] **Elevation Support:** Avoid steep hills for a physically easier walk.
  * [ ] **Crime Data Overlay:** Avoid high-crime zones (requires external API).
  * [ ] **Lighting Data:** "Safe Night Walk" mode preferring well-lit streets.
  * [ ] **Mobile Layout:** Optimize CSS for phone screens.

## 🤝 Contributing

Contributions are welcome\! Please fork the repository and submit a Pull Request.

-----

**License:** MIT

---

<p align="center">
  <b>SereniPy</b> • Created by <a href="https://github.com/Dharm3112"><b>Dharm Patel</b></a>
</p>
