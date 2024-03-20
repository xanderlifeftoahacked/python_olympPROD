import requests
from polyline import decode
import folium

# Define the GraphHopper API key and the base URL for routing requests
api_key = '41b99b2f-0843-4ccc-947b-89ef6cefade4'
base_url = 'https://graphhopper.com/api/1/'

# Specify the starting and ending coordinates for the route
start_location = '40.730610,-73.935242'  # New York City coordinates
end_location = '37.773972,-122.431297'   # San Francisco coordinates

# Construct the request URL with the necessary parameters
url = f"{base_url}route?point={start_location}&point={end_location}&vehicle=car&key={api_key}"

# Make a GET request to the GraphHopper API to calculate the route
response = requests.get(url)

# Check if the request was successful and extract the route data
if response.status_code == 200:
    route_data = response.json()

    if 'paths' in route_data:
        # Extract the route geometry (encoded polyline) from the response
        encoded_polyline = route_data['paths'][0]['points']
        print("Route calculated successfully.")
    else:
        print("Error: No route found.")
else:
    print("Error: Failed to retrieve route data.")

# Display or use the encoded polyline to visualize the route on a map
print("Encoded Polyline:", encoded_polyline)

decoded_polyline = decode(encoded_polyline)

# Create a map centered at the starting location
map_center = [start_location[0], start_location[1]]
map_route = folium.Map(location=map_center, zoom_start=5)

# Add the route as a Polyline to the map
folium.PolyLine(locations=decoded_polyline, color='blue').add_to(map_route)

# Save the map as an HTML file
map_route.save('route_map.html')

print("Route map saved as 'route_map.html'.")
