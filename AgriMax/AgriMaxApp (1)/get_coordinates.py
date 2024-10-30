from geopy.geocoders import Nominatim
import geopy.exc as geo

def get_latitude_longitude(city_name):
    try:
        # Create a geolocator object
        geolocator = Nominatim(user_agent="geoapiExercises", timeout=None)

        # Get location information
        location = geolocator.geocode(city_name)

        if location:
            return (location.latitude, location.longitude)
        else:
            return None
    except geo.GeocoderInsufficientPrivileges:
        pass
