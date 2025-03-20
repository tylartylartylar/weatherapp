# main.py
"""
Main entry point for the weather application.
"""

from utils.location import load_zipcode_database, get_coords_from_zip, getLocationInput
from forecasts.weekly import display_weekly_forecast
from forecasts.extended import display_extended_forecast
from forecasts.daily import display_day_forecast

def main():
    # Load zipcode database
    zipcode_db = load_zipcode_database()
    
    # Get user location
    zipcode = getLocationInput()
    
    if zipcode and zipcode_db:
        print(f"Trying to find coordinates for {zipcode}...\n")
        location_data = get_coords_from_zip(zipcode, zipcode_db)
        
        if location_data:
            print(f"Location: {location_data['display_name']}")
            print(f"Coordinates: {location_data['lat']}, {location_data['lng']}")

            choice = input("Options: Extended, Weekly, Daily (extended / weekly (default) / daily)?\n ")

            filtered_choice = choice.lower()

            if filtered_choice == "extended":
                display_extended_forecast(location_data)
            elif filtered_choice == "daily":
                display_day_forecast(location_data)

            else:
                display_weekly_forecast(location_data)
        else:
            print("Could not find coordinates for this zipcode.")
    else:
        print("Exiting program.")

if __name__ == "__main__":
    main()