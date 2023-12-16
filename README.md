# FlickrTool
## Description
This program is designed to help users to find the most popular places all around the world based on the photos uploaded to Flickr. Based on recommender analogous or customized drawing polygons, the user will get the information of all photos taking within a specific region, and the program will generate interactive plots and urls of photos for users to browse.
## Instructions
This program requires 2 kinds of API Key, one is for accessing photos from Flickr, which needs to be filled in “FlickrWrapper.py”, the other is for accessing basemap from Mapbox, which needs to be filled in “index.html” in the templates folder. The program starts at main.py, which is also the main logics of the codes are located. 

Once the users click “run” in the main.py, the program will start and provide a few options for the users to access photos of certain place: 

1. Recommendation
   
The code will generate a recommender analogous based on pre-defined binary tree cache, when the user agree with the recommendation, the code will call flickrapi to get all information of the photos within the region, and the locations and the hourly frequency of the photos will be handled and displayed based on the users’ preference. 

If none of the option suits the users’ appetite, the program will ask the user to draw and name a region in a interactive map it provides and record the box boundary and name of the region to the tree structure, then generate the plots and urls. 

After displaying the information of the photos of the region, the program will ask the users whether they want to play again or save the search logs, the search logs can be loaded in next time’s search if the user want to use it.

2. Free Exploration
   
If the users don’t want to get recommendations from the program, they can select this option to explore and draw any area they want, or they can access the logs of areas where they search and record in the previous search, again the program will generate interactive plots using plotly based on the locations and hourly distribution of the photos in the region.
## Data Structure
The program uses binary tree structure to organize the flickr data. Each node in this tree is structured as a dictionary with three keys: "question", "yes", and "no". The "question" key at the root contains the initial question posed to the user, while in the leaf nodes, it contains an array with the location name and coordinates. The "yes" and "no" keys represent the subsequent paths based on the user's response, leading either to further questions (in a more complex tree) or terminating at leaf nodes that conclude the decision-making process.

The example of the tree structure in this program like:
```python
{
    "question": "Do you like places that snow all the time?",
    "yes": {
        "question": [
            "Minnesota",
            "-96.075269,46.012721,-92.863071,48.611106"
        ],
        "yes": null,
        "no": null
    },
    "no": {
        "question": [
            "California",
            "-118.512951,33.505042,-115.300753,36.103427"
        ],
        "yes": null,
        "no": null
    }
}
``` 

## Requirement Packages

*[Flask](http://flask.pocoo.org/)*
*[requests](http://docs.python-requests.org/en/latest/)*
*[multiprocessing](https://docs.python.org/2/library/multiprocessing.html)*
*[webbrowser](https://docs.python.org/2/library/webbrowser.html)*
*[threading](https://docs.python.org/2/library/threading.html)*
*[json](https://docs.python.org/2/library/json.html)*
*[pandas](http://pandas.pydata.org/)*
*[plotly](https://plot.ly/)*
*[flickrapi](https://stuvel.eu/flickrapi)*
