from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Initialize the Nominatim geocoder
geolocator = Nominatim(user_agent="uk_postcode_locator")

# Use RateLimiter to handle usage limits
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def postcode_to_latlon(postcode):
    try:
        # Use geopy's geocode to get location data
        location = geocode(postcode)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching coordinates for postcode '{postcode}': {e}")
        return None, None

# Example usage
postcode = "E78LF"  # Buckingham Palace postcode
latitude, longitude = postcode_to_latlon(postcode)
print(f"Latitude: {latitude}, Longitude: {longitude}")
