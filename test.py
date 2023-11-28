import os
from flickrapi import FlickrAPI
from dotenv import load_dotenv
import json



# Load the credentials
load_dotenv()
FLICKR_PUBLIC = 'fae09b3743b16c9ce4756b8c694da718'
FLICKR_SECRET = '6bc603a9fa92c094'

# Initialize FlickrAPI with your credentials
flickr = FlickrAPI(FLICKR_PUBLIC, FLICKR_SECRET, format='parsed-json')

# Define the rectangle region - min latitude, min longitude, max latitude, max longitude
bbox_str = '-130, 40, -120, 50'

# Define extra parameters: geo location and date taken
extras_str = 'geo, date_taken'

# Define the parameters for the API request
params = {
    'method': 'flickr.photos.search',
    'api_key': FLICKR_PUBLIC,
    'bbox': bbox_str,
    'extras': extras_str,
    'format': 'json',
    'nojsoncallback': 1
}

# Make the API request
response = flickr.photos.search(bbox=bbox_str, extras=extras_str, format='json', nojsoncallback=1)
a = json.loads(response)
# Check the result
data = a['photos']['photo']

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry" : {
                "type": "Point",
                "coordinates": [float(d['longitude']), float(d['latitude'])],
                },
            "properties" : d,
        } for d in data]
}

# Save the result as a GeoJSON file
geojson_str = json.dumps(geojson, indent=2)
output_filename = 'flickr_photos.geojson'
with open(output_filename, 'w') as output_file:
    output_file.write('{}'.format(geojson_str))