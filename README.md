# 🌙 Serenipy: The Smart City Navigator

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![OpenStreetMap](https://img.shields.io/badge/Data-OpenStreetMap-7EBC6F?style=for-the-badge&logo=openstreetmap&logoColor=white)](https://www.openstreetmap.org/)
[![Live App](https://img.shields.io/badge/Live_Demo-Serenipy-purple?style=for-the-badge)](https://serenipy.streamlit.app/)

> **Navigate your city by Silence, Safety, and Comfort.**

**Serenipy** is a geospatial web application that prioritizes your well-being over speed. While Google Maps optimizes for the shortest travel time, Serenipy uses graph theory to find the "happiest" walking path—avoiding dark alleyways at night, skipping steep hills, and prioritizing green parks over noisy highways.

## 🔗 Live Demo
Check out the live application here:  
**👉 [Serenipy](https://serenipy.streamlit.app/)**

---

## 🚀 Key Features

### 🌍 Global Routing
* Works for **any two addresses on Earth** (optimized for walking distances <10km).
* Dynamically downloads live street data from OpenStreetMap (Overpass API) on demand.

### 🔦 Safe Night Mode
* **Problem:** Walking home at night can be scary on unlit streets.
* **Solution:** Checks street lighting data (`lit=yes` tags) from OSM. The algorithm applies a heavy penalty (5x cost) to unlit roads or dark alleyways, routing you through well-lit main streets even if it takes a few minutes longer.

### ⛰️ Hill Avoidance (Elevation Support)
* **Problem:** Carrying groceries up a steep hill is exhausting.
* **Solution:** Integrates the **Open-Elevation API** to calculate the gradient of the route. It detects elevation changes and finds the "flattest" path available.

### 📱 Mobile-First Design
* Custom CSS styling makes the app feel like a native mobile app.
* **Dark Mode** map tiles (CartoDB Dark Matter) for reduced eye strain and better contrast at night.

---

## 🛠️ Tech Stack

* **Frontend:** `Streamlit` (Web UI), `CSS3` (Custom Styling).
* **Geospatial Logic:** `OSMnx` (Map Data), `NetworkX` (Graph Algorithms), `Geopy` (Distance calculations).
* **Visualization:** `Folium` (Interactive Leaflet Maps).
* **APIs:** OpenStreetMap (Overpass), Open-Elevation.

---

## 📂 Project Structure

```text
Serenipy/
│
├── app.py              # The Main Interface (Streamlit)
├── map_engine.py       # The Logic Core (Routing, API calls, Weights)
├── config.py           # Configuration (Noise weights, multipliers)
├── style.css           # Custom CSS for Mobile/Dark theme
├── requirements.txt    # Library dependencies
└── README.md           # Documentation
````

-----

## ⚙️ Installation Guide

Follow these steps to run Serenipy on your local machine.

### 1\. Clone the Repository

```bash
git clone [https://github.com/your-username/serenipy.git](https://github.com/your-username/serenipy.git)
cd serenipy
```

### 2\. Create a Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate
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

### 4\. Run the App

```bash
streamlit run app.py
```

*The app will open automatically at `http://localhost:8501`*

-----

## 🧠 How the Algorithm Works

Serenipy uses **Dijkstra's Algorithm**, but instead of `Edge Weight = Distance`, we use a dynamic `Custom Cost` formula:

$$ Cost = Distance \times (NoiseFactor \times SafetyPenalty \times HillPenalty) $$

1.  **Noise Factor:**
      * *Highways/Main Roads:* 10.0 (Avoid)
      * *Parks/Footways:* 0.5 (Prefer - "Bonus")
2.  **Safety Penalty (Night Mode):**
      * If `lit=no` or unknown: Cost is multiplied by **5x**.
3.  **Hill Penalty (Elevation Mode):**
      * If gradient \> 5%: Cost increases proportionally to slope steepness.

-----
<!--
## 📸 Screenshots

| Light Mode (Default) | Dark Mode (Night Safety) |
|:---:|:---:|
| *Optimized for greenery and parks.* | *Optimized for well-lit main roads.* |

-----
-->
## 🤝 Contributing

Contributions are welcome\!

1.  Fork the repo.
2.  Create a feature branch (`git checkout -b feature/NewAlgo`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  <b>Serenipy</b> • Created by <a href="https://github.com/Dharm3112"><b>Dharm Patel</b></a>
</p>
