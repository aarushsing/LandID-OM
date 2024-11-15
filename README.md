
# LandID-OM

**LandID-OM** is a Python-based tool that integrates **Land.ID** and **Overture Maps** functionalities to retrieve and filter geospatial data. It automates the process of fetching parcel polygon data from **Land.ID**, uses it to define bounding boxes, and retrieves building data from the **Overture Maps dataset**. The filtered building data is saved in GeoJSON format for further analysis or use.

---

## Features

1. **LandID Integration**:
   - Automates fetching polygon details for multiple parcels based on longitude and latitude coordinates.
   - Stores polygon data in `polygon_parcel.json`.

2. **Overture Maps Integration**:
   - Uses parcel polygon data to generate bounding boxes.
   - Downloads building data from the Overture Maps dataset.
   - Filters and stores only the buildings within the parcel polygons.

3. **Organized Data Management**:
   - Saves filtered building data as individual GeoJSON files in the `building_data/` directory.

---

## Files

### 1. **LandID: `test_fetch.py`**
- **Command**: 
  ```bash
  pytest -s test_fetch.py
  ```
- **Purpose**:
  - Reads longitude and latitude coordinates from an `.env` file.
  - Fetches parcel polygon details from **Land.ID**.
  - Stores the retrieved polygon data in `polygon_parcel.json`.

### 2. **Overture Maps: `OM_building_data.py`**
- **Command**: 
  ```bash
  python OM_building_data.py
  ```
- **Purpose**:
  - Reads polygon data from `polygon_parcel.json`.
  - Creates bounding boxes around parcels.
  - Retrieves building data using Overture Maps.
  - Filters buildings inside each parcel polygon using the `filter_buildings_in_polygon` function.
  - Saves the filtered building data in the `building_data/` directory as `filtered_building_<building_id>.geojson`.

---

## Installation

### 1. **LandID Automation with Playwright**
Automates fetching land parcel data using **Playwright** in Python.

#### Prerequisites
- Python
- Playwright
- `dotenv` library

#### Installation
1. Install **Playwright** and the Pytest plugin:
   ```bash
   pip install pytest-playwright
   playwright install
   ```
2. Set up a `.env` file with the following structure:
   ```env
   EMAIL=your_email
   PASSWORD=your_password
   COORDINATES=[{"id":3071,"lat":29.1489,"lng":-82.174222}, ...]
   ```

#### Usage
Run the test script:
```bash
pytest -s test_fetch.py
```

---

### 2. **Overture Maps Building Data**
Retrieves building polygon data from the **Overture Maps** dataset using bounding boxes.

#### Prerequisites
- Python
- **Overture Maps CLI**

#### Installation
1. Install the **Overture Maps** CLI:
   ```bash
   pip install overturemaps
   ```
2. Clone the repository:
   ```bash
   git clone https://github.com/aarushsing/LandID-OM.git
   cd LandID-OM
   ```

#### Usage
Run the building data script:
```bash
python OM_building_data.py
```
The script will:
- Generate bounding boxes from the parcel polygons.
- Fetch building data.
- Save filtered building GeoJSON files in the `building_data/` directory.

---

## Output Structure

1. **Polygon Parcel Data**:
   - File: `polygon_parcel.json`
   - Format: JSON

2. **Filtered Building Data**:
   - Directory: `building_data/`
   - File Format: GeoJSON (e.g., `filtered_building_<building_id>.geojson`)

---

## Contributions

Contributions are welcome! If you encounter issues or have ideas for improvement:
- Open an issue in the repository.
- Submit a pull request with detailed changes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

For questions or support, contact **Aarush** at [aarushs505@gmail.com](mailto:aarushs505@gmail.com).
