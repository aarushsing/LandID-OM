import pytest
import json
import os
from dotenv import load_dotenv
from playwright.async_api import async_playwright

# Load environment variables from .env file
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
COORDINATES = json.loads(os.getenv("COORDINATES"))

@pytest.mark.asyncio
async def test_fetch_parcel_data():
    results = {}  # Dictionary to store the geom_as_wkt (polygon) data for each coordinate

    async with async_playwright() as p:
        # Launch Chromium browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # Go to the login page
        await page.goto("https://id.land/users/sign_in", wait_until="domcontentloaded")

        # Fill in login credentials and submit
        await page.fill('input[name="email"]', EMAIL)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button[type="submit"]')

        # Wait for the profile response to extract the auth token
        profile_response = await context.wait_for_event("response", lambda response: 
            response.url == "https://api.id.land/profile.json" and response.status == 200
        )
        profile_data = await profile_response.json()
        auth_token = profile_data.get("authentication_token")
        email = profile_data.get("email")

        print(f"Logged in as: {email}")

        # Fetch parcel data for each coordinate
        for coord in COORDINATES:
            parcel_id = coord['id']
            lat = coord['lat']
            lng = coord['lng']
            print(f"Fetching parcel data for ID: {parcel_id}, Lat: {lat}, Lng: {lng}")

            # Make the request to fetch parcel data
            parcel_response = await page.request.get(
                f"https://parcels.id.land/parcels/v2/by_location.json?lng={lng}&lat={lat}",
                headers={
                    "X-Auth-Token": auth_token,
                    "X-Auth-Email": email
                }
            )

            # Process the response and save only the geom_as_wkt (polygon data) to dictionary
            if parcel_response.ok:
                parcel_data = await parcel_response.json()

                # Extract and store only the geom_as_wkt field
                geom_as_wkt = None
                if "parcels" in parcel_data and len(parcel_data["parcels"]) > 0:
                    geom_as_wkt = parcel_data["parcels"][0].get("geom_as_wkt", None)

                if geom_as_wkt:
                    results[parcel_id] = geom_as_wkt
                    print(f"geom_as_wkt for Parcel ID {parcel_id}: {geom_as_wkt}")
                else:
                    results[parcel_id] = {"error": "No geom_as_wkt found"}
                    print(f"No geom_as_wkt found for Parcel ID {parcel_id}")
            else:
                print(f"Failed to fetch data for ID {parcel_id}")
                results[parcel_id] = {"error": "Failed to fetch data"}

        # Close the browser
        await browser.close()

    # Save results to JSON file
    with open("parcel_polygon.json", "w") as json_file:
        json.dump(results, json_file, indent=4)
        print("Parcel geom_as_wkt data saved to parcel_polygon.json")

# Run the test
# pytest -s <filename>.py
