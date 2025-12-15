from map_engine import QuietRouteFinder
from config import PLACE_NAME


def main():
    finder = QuietRouteFinder(PLACE_NAME)

    # Central Park Coordinates
    start_coords = (40.7681, -73.9819)
    end_coords = (40.7794, -73.9632)

    try:
        fast_route, quiet_route = finder.get_routes(start_coords, end_coords)
        finder.visualize_routes(fast_route, quiet_route)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()