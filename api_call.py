import requests
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import orient


def api_call_multipolygons(multipolygon, coord_uncertainty="0,500", year="2010,2023"):
    if not isinstance(multipolygon, MultiPolygon):
        raise ValueError('Input is not a MultiPolygon')

    polygons = []
    for polygon in multipolygon.geoms:
        if isinstance(polygon, Polygon):
            polygons.append(polygon)
        else:
            polygons.extend(polygon.geoms)

    all_coordinates = []
    for polygon in polygons:
        poly = orient(polygon, sign=1.0)

        # Calculate the bounding box coordinates from the polygon
        min_lat, min_lon, max_lat, max_lon = poly.bounds

        # Set the query parameters to retrieve occurrences within the polygon and bounding box
        params = {
            "geometry": poly.wkt,  # Polygon coordinates in counterclockwise order
            "decimalLongitude": f"{min_lat},{max_lat}",  # Bounding box latitude range
            "decimalLatitude": f"{min_lon},{max_lon}",  # Bounding box longitude range
            "coordinateUncertaintyInMeters": coord_uncertainty,  # Filter occurrences by coordinate uncertainty
            "limit": 300,  # Maximum number of occurrences to download per batch
            "offset": 0,  # Offset for paginating through results
            "year": year,  # Filter occurrences by year
            # Add any other relevant query parameters here
        }
        # Make multiple requests with different offset values to retrieve all occurrences
        all_results = []
        while True:
            response = requests.get("https://api.gbif.org/v1/occurrence/search", params=params)
            try:
                response.raise_for_status()
                response_json = response.json()
            except requests.exceptions.RequestException as e:
                print(f"Request error: {e}")
                return None
            except ValueError as e:
                print(f"JSON decode error: {e}")
                print(f"Response content: {response.content}")
                return None

            results = response_json["results"]
            if len(results) == 0:
                break
            all_results.extend(results)
            params["offset"] += 300

        # Extract the coordinates from the results
        coordinates = []
        for result in all_results:
            if "decimalLatitude" in result and "decimalLongitude" in result:
                coordinates.append((result["decimalLatitude"], result["decimalLongitude"]))

        all_coordinates.append(coordinates)
    return all_coordinates
