# 🌙 Serenipy: The Smart City Navigator

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit)
![OpenStreetMap](https://img.shields.io/badge/Data-OpenStreetMap-green?style=for-the-badge)

**Serenipy** is a geospatial web application that prioritizes **safety, silence, and comfort** over speed. 

While Google Maps optimizes for the shortest time, Serenipy uses graph theory to find the "happiest" path—avoiding dark alleyways at night, skipping steep hills, and prioritizing green parks over noisy highways.

---

## 🚀 Key Features

### 🌍 Global Routing
* Works for **any two addresses on Earth** (optimized for walking distances <10km).
* Dynamically downloads live street data from OpenStreetMap.

### 🔦 Safe Night Mode
* **Problem:** Walking home at night can be scary on unlit streets.
* **Solution:** Checks street lighting data (`lit=yes` tags). The algorithm applies a heavy penalty to unlit roads, routing you through well-lit main streets even if it takes a few minutes longer.

### ⛰️ Hill Avoidance (Elevation API)
* **Problem:** Carrying groceries up a steep hill is exhausting.
* **Solution:** Integrates the **Open-Elevation API** to calculate the gradient of the route. It finds the "flattest" path available.

### 📱 Mobile-First Design
* Custom CSS styling makes the app feel like a native mobile app.
* "Dark Mode" map tiles (CartoDB Dark Matter) for reduced eye strain.

---

## 🛠️ Tech Stack

* **Frontend:** `Streamlit` (Web UI), `CSS3` (Custom Styling).
* **Geospatial Logic:** `OSMnx`, `NetworkX` (Graph Theory), `Geopy`.
* **Visualization:** `Folium` (Interactive Maps).
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

Serenipy uses **Dijkstra's Algorithm**, but instead of `Edge Weight = Distance`, we use a dynamic `Custom Cost`:

$$ Cost = Distance \times (NoiseFactor \times SafetyPenalty \times HillPenalty) $$

1.  **Noise Factor:**
      * *Highways:* 10.0 (Avoid)
      * *Parks/Footways:* 0.5 (Prefer)
2.  **Safety Penalty (Night Mode):**
      * If `lit=no` or unknown: Cost is multiplied by **5x**.
3.  **Hill Penalty (Elevation Mode):**
      * If gradient \> 5%: Cost increases based on slope steepness.

-----

## 📸 Screenshots

| Light Mode (Default) | Dark Mode (Night Safety) |
|:---:|:---:|
| *Optimized for greenery and parks.* | *Optimized for well-lit main roads.* |

-----

## 🤝 Contributing

Contributions are welcome\!

1.  Fork the repo.
2.  Create a feature branch (`git checkout -b feature/NewAlgo`).
3.  Commit your changes.
4.  Push to the branch.
5.  Open a Pull Request.

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

-----

**Created with ❤️ by [Your Name]**
