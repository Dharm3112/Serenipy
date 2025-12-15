import streamlit as st
from streamlit_folium import st_folium
from map_engine import QuietRouteFinder
from geopy.distance import geodesic

# --- CONFIG ---
st.set_page_config(page_title="Serenipy", layout="wide", initial_sidebar_state="expanded")


# --- LOAD CSS ---
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


local_css("style.css")  # Make sure style.css is in the same folder

# --- TITLE ---
st.title("🌙 Serenipy: Smart City Routing")
st.markdown("Navigate your city by **Silence**, **Safety**, and **Comfort**.")

if "map_obj" not in st.session_state: st.session_state.map_obj = None

# --- SIDEBAR ---
with st.sidebar:
    st.header("📍 Trip Details")
    start = st.text_input("Start", "Montmartre, Paris")
    end = st.text_input("End", "Eiffel Tower, Paris")

    st.divider()

    st.header("⚙️ Preferences")
    # THE NEW TOGGLES
    night_mode = st.checkbox("🔦 Safe Night Mode", help="Avoids unlit streets/alleys.")
    avoid_hills = st.checkbox("⛰️ Avoid Steep Hills", help="Prioritizes flat routes (Slower processing).")

    btn = st.button("Find My Route", type="primary")

# --- LOGIC ---
if btn:
    finder = QuietRouteFinder()
    with st.spinner("🔍 Locating..."):
        s_coords = finder.geocode_address(start)
        e_coords = finder.geocode_address(end)

    if s_coords and e_coords:
        dist = geodesic(s_coords, e_coords).kilometers
        if dist > 5:
            st.error(f"Distance is {dist:.1f}km. Please keep it under 5km for walking routes.")
        else:
            try:
                with st.spinner("🌍 Downloading Map Data..."):
                    finder.download_map_slice(s_coords, e_coords)

                # Fetch Elevation ONLY if requested (saves time)
                if avoid_hills:
                    with st.spinner("⛰️ Fetching Elevation Data (This takes time)..."):
                        success = finder.add_elevation_data()
                        if not success: st.warning("Elevation server busy. Ignoring hills.")

                with st.spinner("⚡ Calculating Best Path..."):
                    path_fast, path_opt = finder.calculate_routes(
                        s_coords, e_coords,
                        avoid_hills=avoid_hills,
                        night_mode=night_mode
                    )

                if path_opt:
                    st.session_state.map_obj = finder.create_map(path_fast, path_opt, s_coords, e_coords)

                    # Display Stats
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Fastest", "Red Path")
                    c2.metric("Recommended", "Cyan Path")
                    c3.metric("Safety Score", "High" if night_mode else "Standard")

            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.error("Address not found.")

# --- RENDER MAP ---
if st.session_state.map_obj:
    st_folium(st.session_state.map_obj, width=1200, height=600, returned_objects=[])