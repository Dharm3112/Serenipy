import osmnx as ox
import networkx as nx
import folium
import requests
from geopy.distance import geodesic
from config import NOISE_WEIGHTS, DEFAULT_NOISE_WEIGHT, PARK_MULTIPLIER


class QuietRouteFinder:
    def __init__(self):
        self.graph = None

    def geocode_address(self, address):
        try:
            lat, lon = ox.geocode(address)
            return (lat, lon)
        except:
            return None

    def download_map_slice(self, start_coords, end_coords):
        # 1. Smart Radius Calculation
        trip_distance = geodesic(start_coords, end_coords).meters
        mid_point = ((start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2)
        radius = (trip_distance / 2) + 300  # Tight buffer

        print(f"Downloading map (Radius: {radius:.0f}m)...")
        # network_type='walk' gets us footpaths
        self.graph = ox.graph_from_point(mid_point, dist=radius, network_type='walk')

    def add_elevation_data(self):
        """Fetches elevation from Free Open-Elevation API."""
        # Note: This API can be slow. In a production app, use Google Maps Elevation API.
        try:
            print("Fetching elevation data...")
            # 1. Prepare coordinates for API
            nodes = list(self.graph.nodes(data=True))
            locations = [{"latitude": data['y'], "longitude": data['x']} for id, data in nodes]

            # 2. Chunk requests (API limits)
            chunk_size = 100
            for i in range(0, len(locations), chunk_size):
                chunk = locations[i:i + chunk_size]
                response = requests.post(
                    "https://api.open-elevation.com/api/v1/lookup",
                    json={"locations": chunk},
                    timeout=5
                )
                results = response.json()['results']

                # 3. Assign elevation back to graph nodes
                for j, result in enumerate(results):
                    node_id = nodes[i + j][0]
                    self.graph.nodes[node_id]['elevation'] = result['elevation']
            return True
        except Exception as e:
            print(f"Elevation API failed: {e}")
            return False

    def calculate_routes(self, start_coords, end_coords, avoid_hills=False, night_mode=False):
        if self.graph is None: return None, None

        # 1. Apply Weights
        for u, v, data in self.graph.edges(data=True):
            length = data.get('length', 0)
            highway = data.get('highway', 'unknown')

            # --- FACTOR 1: NOISE ---
            if isinstance(highway, list): highway = highway[0]
            noise_factor = NOISE_WEIGHTS.get(highway, DEFAULT_NOISE_WEIGHT)

            # --- FACTOR 2: PARKS ---
            if highway in ['footway', 'path', 'cycleway', 'pedestrian']:
                noise_factor *= PARK_MULTIPLIER

            # --- FACTOR 3: LIGHTING (Night Mode) ---
            if night_mode:
                # Check for 'lit' tag. Values can be 'yes', 'no', '24/7', etc.
                is_lit = data.get('lit', 'no')
                if is_lit == 'no' or is_lit is None:
                    noise_factor *= 5.0  # Massive penalty for dark streets

            # --- FACTOR 4: HILLS (Elevation) ---
            grade_penalty = 1.0
            if avoid_hills:
                # Calculate slope if elevation data exists
                try:
                    elev_u = self.graph.nodes[u].get('elevation', 0)
                    elev_v = self.graph.nodes[v].get('elevation', 0)
                    rise = abs(elev_v - elev_u)
                    if length > 0:
                        grade = rise / length
                        # If grade > 5% (steep), increase cost
                        if grade > 0.05:
                            grade_penalty = 1.0 + (grade * 10)  # 10% slope = 2x cost
                except:
                    pass

            # Final Cost Calculation
            data['custom_cost'] = length * noise_factor * grade_penalty

        # 2. Find Nodes
        start_node = ox.distance.nearest_nodes(self.graph, start_coords[1], start_coords[0])
        end_node = ox.distance.nearest_nodes(self.graph, end_coords[1], end_coords[0])

        # 3. Calculate Paths
        # FASTEST
        path_fast = nx.shortest_path(self.graph, start_node, end_node, weight='length')
        # OPTIMIZED (Quiet/Safe/Flat)
        path_opt = nx.shortest_path(self.graph, start_node, end_node, weight='custom_cost')

        return path_fast, path_opt

    def create_map(self, path_fast, path_opt, start_coords, end_coords):
        m = folium.Map(location=start_coords, zoom_start=14, tiles='CartoDB dark_matter')

        def get_coords(path):
            return [(self.graph.nodes[n]['y'], self.graph.nodes[n]['x']) for n in path]

        # Fast (Red, Dashed)
        folium.PolyLine(get_coords(path_fast), color='#FF0055', weight=4, opacity=0.8, dash_array='10',
                        tooltip='Fastest').add_to(m)

        # Optimized (Cyan, Glowing)
        coords_opt = get_coords(path_opt)
        folium.PolyLine(coords_opt, color='#00FFFF', weight=8, opacity=0.4).add_to(m)  # Glow
        folium.PolyLine(coords_opt, color='#00FFFF', weight=3, opacity=1.0, tooltip='Recommended').add_to(m)  # Core

        # Markers
        folium.Marker(start_coords, icon=folium.Icon(color='green', icon='play')).add_to(m)
        folium.Marker(end_coords, icon=folium.Icon(color='red', icon='stop')).add_to(m)
        return m