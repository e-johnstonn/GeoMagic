from geopy.geocoders import Nominatim
from geopy.location import Location


class Geocoder:

    USER_AGENT = "geo-magic-1.0"

    def __init__(self):
        self.geolocator = Nominatim(user_agent=self.USER_AGENT)

    def geocode_from_address(self, address: str) -> Location:
        return self.geolocator.geocode(address, addressdetails=True)

    def geocode_from_coordinates(self, lat: float, lon: float) -> Location:
        return self.geolocator.reverse((lat, lon), addressdetails=True)
