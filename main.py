import csv

def load_zipcode_database(filename="zipcodes.csv"):
    zipcode_dict = {}
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                zipcode = str(row['zip']).zfill(5)
                zipcode_dict[zipcode] = {
                    'lat': float(row['lat']),
                    'lng': float(row['lng']),
                    'city': row['city'],
                    'state_id': row['state_id'],
                    'state_name': row['state_name']
                }
        print(f"Loaded {len(zipcode_dict)} zipcodes from database.")
        return zipcode_dict
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
        return {}
    except Exception as e:
        print(f"Error loading zipcode database: {e}")
        return {}
    
def get_coords_from_zip(zipcode, zipcode_db):
    if zipcode in zipcode_db:
        data = zipcode_db[zipcode]
        return {
            'lat': data['lat'],
            'lng': data['lng'],
            'display_name': f"{data['city']}, {data['state_id']}"
        }
    
    print(f"Zipcode {zipcode} not found in database.")
    return None    

def getLocationInput():
    user_location = input("Please enter your current 5-digit Zipcode XXXXX\n-> ")
    if len(user_location) == 5 and user_location.isdigit():
        return user_location
    else:
        print(f"Supplied zipcode invalid length... {user_location}")
        retry = input("would you like to retry? (Y/n)")
        if retry.lower() == "y":
            return getLocationInput()
        else:
            print(f"Supplied zipcode invalid length... Maybe go outside to check the weather until I can implement search by city/state")
            return None

def main():
    zipcode_db = load_zipcode_database()
    
    zipcode = getLocationInput()
    
    if zipcode and zipcode_db:
        print(f"Trying to find coordinates for {zipcode}...\n")
        location_data = get_coords_from_zip(zipcode, zipcode_db)
        if location_data:
            print(f"Location: {location_data['display_name']}")
            print(f"Coordinates: {location_data['lat']}, {location_data['lng']}")
            
            print(f"Getting basic forecast for {location_data['display_name']}...")
            
            
        else:
            print("Could not find coordinates for this zipcode.")
    else:
        print("Exiting program.")
    
if __name__ =="__main__":
    main()