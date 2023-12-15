from flickrapi import FlickrAPI
from dotenv import load_dotenv
import json
import pandas as pd

class FlickrAPIWrapper:
    def __init__(self):
        load_dotenv()
        self.FLICKR_PUBLIC = 'fae09b3743b16c9ce4756b8c694da718'
        self.FLICKR_SECRET = '6bc603a9fa92c094'
        self.flickr = FlickrAPI(self.FLICKR_PUBLIC, self.FLICKR_SECRET, format='parsed-json')
        self.extras_str = 'geo, date_taken'

    def get_geojson(self, bbox_str):
        """
        Retrieves photo data from Flickr API within a specified bounding box and converts it to GeoJSON format.

        Parameters:
            bbox_str (str): A string representing the bounding box coordinates in the format
                            "min_longitude,min_latitude,max_longitude,max_latitude".

        Returns:
            dict: A GeoJSON dictionary representing the photo data. Each photo is a feature with its
                location as a point (longitude and latitude) and other data as properties.
        """
        params = {
            'method': 'flickr.photos.search',
            'api_key': self.FLICKR_PUBLIC,
            'bbox': bbox_str,
            'extras': self.extras_str,
            'format': 'json',
            'nojsoncallback': 1
        }
        response = self.flickr.photos.search(**params)
        data = json.loads(response)
        if data['stat'] =='fail':
            raise Exception("API request failed")
        data = data['photos']['photo']
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
        return geojson
    
    def get_dataframe(self, bbox_str):
        """
        Fetches photo data from the Flickr API within a specified bounding box and converts it into a pandas DataFrame.Each row in the DataFrame represents a photo, and includes data such as its Flickr URL, server, id, and secret.

        Parameters:
            bbox_str (str): A string representing the bounding box coordinates in the format
                            "min_longitude,min_latitude,max_longitude,max_latitude".

        Returns:
            pandas.DataFrame: A DataFrame containing the photo data. Includes a custom 'url' column
                            that constructs the direct URL to each photo on Flickr.
        """
        params = {
            'method': 'flickr.photos.search',
            'api_key': self.FLICKR_PUBLIC,
            'bbox': bbox_str,
            'extras': self.extras_str,
            'format': 'json',
            'nojsoncallback': 1
        }
        response = self.flickr.photos.search(**params)
        data = json.loads(response)
        if data['stat'] =='fail':
            raise Exception("API request failed")
        data = data['photos']['photo']
        df  = pd.DataFrame(data)
        df['url'] = df.apply(lambda row: f"https://live.staticflickr.com/{row['server']}/{row['id']}_{row['secret']}.jpg", axis=1)
        return df


if __name__ == '__main__':
    FlickrWrapper = FlickrAPIWrapper()
    # result = FlickrWrapper.get_photo("53115458025")
    # # webbrowser.open(result['photo']['urls']['url'][0]['_content'])
    # print(result['photo']['title']['_content'])
    try:
        result1 = FlickrWrapper.get_dataframe("33.505042,-115.300753,36.103427,-118.512951")
        print(result1)
    except Exception as e:
        print(e)
    try:
        result2 = FlickrWrapper.get_dataframe("-96.075269,46.012721,-92.863071,48.611106")
        print(result2)
    except Exception as e:
        print(e)
    #save to csv
    # result.to_csv('flickr.csv')
