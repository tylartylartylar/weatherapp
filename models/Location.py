# location data structures
class Location:
    
    def __init__(self, lat, lng, city, state, display_name, timezone):
        self.lat = lat
        self.lng = lng
        self.city = city
        self.state = state
        self.display_name = display_name
        self.timezone = timezone

    @classmethod
    def from_zipcode_data(cls, location_dict):
        lat = location_dict['lat']
        lng = location_dict['lng']
        city = location_dict['city']
        state = location_dict['state']
        display_name = location_dict['display_name']
        timezone = location_dict['timezone']

        return cls(lat,lng,city,state,display_name, timezone)
    
    @classmethod
    def from_zipcode(cls, zipcode, zipcode_db):
        for entry in zipcode_db:
            if entry.get('zip') == zipcode:
                
                return cls(
                    lat = float(entry.get('lat', 0)),
                    lng = float(entry.get('lng', 0)),
                    city = entry.get('city', ''),
                    state = entry.get('state_id', ''),
                    display_name = display_name,
                    timezone = entry.get('timezone', 'america/chicago'),
                )
        return None

    def to_dict(self):
        return {
            'lat': self.lat,
            'lng': self.lng,
            'city': self.city,
            'state': self.state,
            'display_name': self.display_name,
            'timezone': self.timezone
        }

    def __str__(self):
        return f"{self.display_name}"
