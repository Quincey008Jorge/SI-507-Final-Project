from flask import Flask, render_template, request, jsonify
from FlickrWrapper import FlickrAPIWrapper as FlickrWrapper
import threading
import time




app = Flask(__name__)
should_shutdown = False
flickr_wrapper = FlickrWrapper()
current_bbox = None
geojson_cache = {}
shutdown_flag = threading.Event()

def run_flask():
    # Function to run the Flask app
    app.run(debug=True, use_reloader=False)

def check_shutdown():
    while not shutdown_flag.is_set():
        time.sleep(1)
    func = request.environ.get('werkzeug.server.shutdown')
    if func is not None:
        func()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    global current_bbox
    bbox_str = request.form['bbox']
    current_bbox = bbox_str
    # Check if GeoJSON is already in the cache
    if bbox_str in geojson_cache:
        geojson_result = geojson_cache[bbox_str]
    else:
        # Query Flickr API and store the result in the cache
        geojson_result = flickr_wrapper.get_geojson(bbox_str)
        geojson_cache[bbox_str] = geojson_result
    return jsonify(geojson_result)

@app.route('/update_geojson', methods=['POST'])
def update_geojson():
    global current_bbox
    if current_bbox:
        updated_geojson = flickr_wrapper.get_geojson(current_bbox)
        return jsonify(updated_geojson)
    else:
        return jsonify({})
    
@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    data = request.get_json()
    region_name = data['name']
    bbox = data['bbox']
    with open('./cache/coordinates.txt', 'w') as f:
        f.write(f"{region_name}\n{bbox}\n")
    return jsonify({"status": "success", "message": "Data saved successfully"})

@app.route('/shutdown', methods=['POST'])
def shutdown():
    global should_shutdown
    should_shutdown = True
    return jsonify({'status': 'success', 'message': 'Server will shut down.'})

@app.before_request
def before_request():
    if should_shutdown:
        func = request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running the Werkzeug Server')
        func()

if __name__ == '__main__':
    threading.Thread(target=check_shutdown).start()
    run_flask()

