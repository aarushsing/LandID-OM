import json
import subprocess
import os
from shapely.geometry import Polygon, shape


def parse_polygon(polygon_string):
    """
    Parse the WKT polygon string and return a list of coordinates.
    """
    coordinates = polygon_string.replace("POLYGON((", "").replace("))", "").split(",")
    coordinates = [tuple(map(float, coord.split())) for coord in coordinates]
    return coordinates


def generate_bbox_from_polygon(coordinates):
    """
    Generate a bounding box from the polygon coordinates without a buffer.
    """
    polygon = Polygon(coordinates)
    minx, miny, maxx, maxy = polygon.bounds
    return (minx, miny, maxx, maxy)


def filter_buildings_in_polygon(parcel_polygon, building_geojson):
    """
    Filter buildings that are entirely within the given parcel polygon.
    """
    filtered_features = []
    parcel_shape = Polygon(parcel_polygon)

    for feature in building_geojson["features"]:
        building_shape = shape(feature["geometry"])
        if building_shape.within(parcel_shape):
            filtered_features.append(feature)

    return filtered_features


def download_polygon_data(bbox, building_id, parcel_polygon):
    """
    Download building polygon data using the bounding box and building ID, 
    then filter buildings that are inside the parcel polygon.
    """
    output_file = f"building_{building_id}.geojson"

    try:
        command = [
            "overturemaps",
            "download",
            f"--bbox={','.join(map(str, bbox))}",
            "-f",
            "geojson",
            "-t",
            "building",
            "-o",
            output_file,
        ]

        print(f"Downloading data for Building ID {building_id}...")
        subprocess.run(command, check=True)
        print(f"Polygon data for Building ID {building_id} saved to {output_file}")

        # Load the downloaded GeoJSON file
        with open(output_file, "r") as file:
            building_geojson = json.load(file)

        # Filter buildings that are inside the parcel polygon
        filtered_features = filter_buildings_in_polygon(parcel_polygon, building_geojson)

        # Ensure the folder exists
        output_folder = "building_data"
        os.makedirs(output_folder, exist_ok=True)

        # Save the filtered data to the folder
        filtered_file = os.path.join(output_folder, f"filtered_building_{building_id}.geojson")
        with open(filtered_file, "w") as file:
            json.dump({"type": "FeatureCollection", "features": filtered_features}, file)

        print(
            f"Filtered polygon data for Building ID {building_id} saved to {filtered_file}"
        )

    except subprocess.CalledProcessError as e:
        print(f"Error downloading data for Building ID {building_id}: {e}")
    except FileNotFoundError:
        print("Error: Make sure the 'overturemaps' utility is installed and available in PATH.")


def main():
    # Load polygon data from the parcel_polygon.json file
    with open("parcel_polygon.json", "r") as file:
        data = json.load(file)

    for building_id, polygon_string in data.items():
        # Skip entries with errors
        if isinstance(polygon_string, dict) and "error" in polygon_string:
            print(f"Skipping Building ID {building_id}: {polygon_string['error']}")
            continue

        try:
            # Parse the polygon string into a list of coordinates
            coordinates = parse_polygon(polygon_string)

            # Generate the bounding box for the polygon
            bbox = generate_bbox_from_polygon(coordinates)

            # Download the polygon data from Overture Maps using the bounding box
            download_polygon_data(bbox, building_id, coordinates)
        except Exception as e:
            print(f"Error processing Building ID {building_id}: {e}")


if __name__ == "__main__":
    main()
