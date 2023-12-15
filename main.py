import webbrowser
import time
import requests
import os
from multiprocessing import Process
from app import app
from FlickrWrapper import FlickrAPIWrapper
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import load_json



def run_flask():
    app.run(debug=True, use_reloader=False)

def get_coordinates():
    """
    Launches a Flask server in a separate process and opens a web browser to a specified local URL. 
    The function waits for a file containing coordinates to be created by the Flask application. 
    Once the file is detected, it posts a request to shut down the Flask server, reads the coordinates 
    from the file, cleans up by deleting the file, and then terminates the server process.

    Returns:
        list: A list of strings, each representing a line from the 'coordinates.txt' file, 
              typically containing coordinate data.
    """
    server = Process(target=run_flask)
    server.start()
    webbrowser.open('http://localhost:5000/')
    time.sleep(5)
    while not os.path.exists('./cache/coordinates.txt'):
        time.sleep(1)
    requests.post('http://localhost:5000/shutdown')
    time.sleep(2)  
    with open('./cache/coordinates.txt', 'r') as file:
        text = file.read().splitlines()
    file.close()
    os.remove('./cache/coordinates.txt')
    server.terminate()  
    server.join()
    return text

def main():
    print("Welcome to Time Tool Flickr!")
    while True:
        print("-------------------------------------------------")
        recommend_answer = input("How would you like to use this tool?\n1. Recommendation\n2. Free Exploration\n3. Exit\n")
        if recommend_answer == "3":
            print("Thank you for using this tool. Goodbye!")
            break
        while recommend_answer not in ["1", "2"]:
            recommend_answer = input("Your answer is not accepected, please answer again: ")
        if recommend_answer == "1":
            print("-------------------------------------------------")
            load_answer = input("Would you like to load a log from previous search?")
            while load_answer.lower() not in ["yes", "y", "yup", "sure", "no", "n", "nope", "nah"]:
                    load_answer = input("Your answer is not accepected, please answer again: ")
            if load_answer.lower() in ["yes", "y", "yup", "sure"]:
                filename = input("What is the name of the file?")
                TreeFile = f'{filename}.json'
                try:
                    load = load_json.TreeConverter()
                    tree = load.json_to_tree(TreeFile)
                except Exception as e:
                    print("The file is not in the correct format. Please try again.")
                    continue
            else:
                try:
                    load = load_json.TreeConverter()
                    start_tree = load.json_to_tree("startTree.json")
                    tree = start_tree
                except Exception as e:
                    print("The file is not in the correct format or not exist. Please check the filename, path or redefine a start tree")
                    continue
            playagain = "yes"
            while playagain.lower() not in ["no", "n", "nope", "nah"]:
                playtree = Play(tree)
                playagain = input("Would you like to search your destination again?")
                while playagain.lower() not in ["yes", "y", "yup", "sure", "no", "n", "nope", "nah"]:
                    playagain = input("Your answer is not accepected, please answer again: ")
                tree = playtree
            save_answer = input("Would you like to save this log for later?")
            while save_answer.lower() not in ["yes", "y", "yup", "sure", "no", "n", "nope", "nah"]:
                    save_answer = input("Your answer is not accepected, please answer again: ")
            if save_answer.lower() in ["no", "n", "nope", "nah"]:
                print("Thank you! You'll be back to the main page")
            if save_answer.lower() in ["yes", "y", "yup", "sure"]:
                filename = input("Please enter a file name:")
                TreeFile = open(filename+'.json',"w")
                load = load_json.TreeConverter()
                json = load.tree_to_json(playtree)
                TreeFile.write(json)
                TreeFile.close()
                print("Thank you! The file has been saved.\nYou'll be back to the main page")
        if recommend_answer == "2":
            while True:
                print("-------------------------------------------------")
                free_area_answer = input("Would you like to explore an area you have saved?\n1. Yes\n2. No\n3. Back to main menu\n")
                if free_area_answer == "3":
                    break
                while free_area_answer not in ["1", "2", "3"]:
                    free_area_answer = input("Your answer is not accepted, please answer again: ")

                if free_area_answer == "1":
                    while True:  # Start of nested loop for log_name
                        log_name = input("Please input the name of your area: ")
                        if log_name.lower() == "exit":
                            break  # Exit the nested loop, goes back to free_area_answer prompt
                        if os.path.exists(f'./cache/{log_name}.txt') and os.path.exists(f'./cache/{log_name}_coords.txt'):
                            # Process the file here
                            df = pd.read_csv(f'./cache/{log_name}.txt')
                            with open(f'./cache/{log_name}_coords.txt', 'r') as file:
                                coordinate = file.read().splitlines()
                            file.close()
                            coordinates_list = [log_name,coordinate]
                            coordinates = [item if isinstance(item, str) else item[0] for item in coordinates_list]
                            print(coordinates)
                            displayphoto(df,coordinates)
                            break  # Optionally break after processing if needed
                        else:
                            print("The files don't exist or are incomplete.")
                if free_area_answer == "2":
                    print("Please draw your interested area on the map!")
                    coordinates = get_coordinates()
                    flickr = FlickrAPIWrapper()
                    try:
                        df = flickr.get_dataframe(coordinates[1])
                        displayphoto(df,coordinates)
                    except:
                        print("Sorry, we cannot find any photos in this area.")

def isLeaf(tree):
    """Returns True if the tree is a leaf and False if it is an internal node."""
    return tree[1] is None

def yes(prompt):
    """Uses the prompt to ask the user a yes/no question and returns True if the answer is yes, False if it is no."""
    answer = input(prompt)
    while answer.lower() not in ["yes", "y", "yup", "sure", "no", "n", "nope", "nah"]:
        answer = input("Your answer is not accepected, please answer again: ")
    if answer.lower() in ["yes", "y", "yup", "sure"]:
        return True
    elif answer.lower() in ["no", "n", "nope", "nah"]:
        return False

def playAnswer(tree):
    """Plays a leaf node by suggesting an answer and deciding whether it was correct."""
    suggestion = "Is it " + tree[0][0] + "? "
    return yes(suggestion)


def Play(tree):
    """Recommend the destination starting at the given tree."""
    if isLeaf(tree):
        if playAnswer(tree):
            print("I think I know a place that will suit your preference!")
            print("The location of the place is: ",tree[0][1])
            flickr = FlickrAPIWrapper()
            try:
                df = flickr.get_dataframe(tree[0][1])
                displayphoto(df,tree[0])
            except:
                print("Sorry, we cannot find any photos in this area.")
            return tree
        else:
            print(("Sorry, but could you please tell me something about your place?"))
            newAnswer,newAnswerLocation = get_coordinates()
            newQuestion = input("What's the recommendation question that distinguishes between {} from {}? ".format(newAnswer,tree[0][0]))
            newAnswerResponse = yes("And what's the answer for {}? ".format(newAnswer))
            return (newQuestion, ([newAnswer,newAnswerLocation], None, None), (tree[0], None, None)) if newAnswerResponse else (newQuestion, (tree[0], None, None), ([newAnswer,newAnswerLocation], None, None))
    else:
        question = tree[0]
        if yes(question):
            return (question, Play(tree[1]), tree[2])
        else:
            return (question, tree[1], Play(tree[2]))



def Plotly(df,coordinates):
    """
    Creates a combined Plotly visualization consisting of two subplots: a map showing the geographical 
    distribution of data points and a bar chart displaying the hourly distribution.

    Parameters:
        df (pandas.DataFrame): A DataFrame containing the data to be plotted. 
        coordinates (str): A string representing geographical coordinates. 

    Returns:
        str: The name of the HTML file where the plot is saved.
    """
    hour_colors = {i: f'hsl({int(360*i/24)},100%,50%)' for i in range(24)}
    fig = make_subplots(
    rows=1,
    cols=2,
    subplot_titles=("Map", "Hourly Distribution"),
    specs=[[{"type": "mapbox"}, {"type": "xy"}]]
)
    hour_counts = df['hour'].value_counts(normalize=True).reset_index()
    hour_counts.columns = ['hour', 'proportion']
    # Scatter plot for map
    map_fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', hover_name='hour',
                                color='hour', color_discrete_map=hour_colors, zoom=6, height=300)
    fig.add_trace(map_fig.data[0], row=1, col=1)

    bar_fig = px.bar(hour_counts, x='hour', y='proportion',color='hour',
                 color_discrete_map=hour_colors)
    for trace in bar_fig.data:
        fig.add_trace(trace, row=1, col=2)

    center_lat = float(coordinates.split(',')[1]) + (float(coordinates.split(',')[3]) - float(coordinates.split(',')[1]))/2
    center_lon = float(coordinates.split(',')[0]) + (float(coordinates.split(',')[2]) - float(coordinates.split(',')[0]))/2

    zoom_level = 8
    fig.update_layout(
        mapbox=dict(
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom_level
        ),
        mapbox_style="open-street-map"
    )

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_geos(fitbounds="locations")
    html_file = 'combined_distribution.html'
    fig.write_html(html_file)

    return html_file

def displayphoto(df,coordinates):
    print("-------------------------------------------------")
    print("How would you like to explore this area?")
    while True:
        explore_answer = input("1. See the distribution and statistical plot of time slots of photos \n2. Check out the photos by hours\n3. Back\n")
        while explore_answer.lower() not in ["1", "2", "3"]:
            explore_answer = input("Your answer is not accepected, please answer again: ")
            if explore_answer == "3":
                break
        if explore_answer == "3":
            break
        if explore_answer == "1":
            flickr = FlickrAPIWrapper()
            if not os.path.exists(f'./cache/{coordinates[0]}.txt'):
                df = flickr.get_dataframe(coordinates[1])
                df['time'] = pd.to_datetime(df['datetaken'])
                df['hour'] = df['time'].dt.hour
                df['latitude'] = pd.to_numeric(df['latitude'], downcast='float')
                df['latitude'] = round(df['latitude'], 4)
                df['longitude'] = pd.to_numeric(df['longitude'], downcast='float')
                df['longitude'] = round(df['longitude'], 4)
                df.to_csv(f'./cache/{coordinates[0]}.txt')
            if not os.path.exists(f'./cache/{coordinates[0]}_coords.txt'):
                with open(f'./cache/{coordinates[0]}_coords.txt', 'w') as f:
                    f.write(coordinates[1])
            else:
                df = pd.read_csv(f'./cache/{coordinates[0]}.txt')
            html = Plotly(df,coordinates[1])
            webbrowser.open(html)
            continue
        if explore_answer == "2":
            flickr = FlickrAPIWrapper()
            if not os.path.exists(f'./cache/{coordinates[0]}.txt'):
                df = flickr.get_dataframe(coordinates[1])
                df['time'] = pd.to_datetime(df['datetaken'])
                df['hour'] = df['time'].dt.hour
                df['latitude'] = pd.to_numeric(df['latitude'], downcast='float')
                df['latitude'] = round(df['latitude'], 4)
                df['longitude'] = pd.to_numeric(df['longitude'], downcast='float')
                df['longitude'] = round(df['longitude'], 4)
                df.to_csv(f'./cache/{coordinates[0]}.txt')
            else:
                df = pd.read_csv(f'./cache/{coordinates[0]}.txt')
            unique_hours = df['hour'].unique()
            print("-------------------------------------------------")
            print("Here are the time slots of photos in this area: ")
            for i in sorted(unique_hours):
                print(i,end=" ")
            print("\n")
            print("-------------------------------------------------")
            time_slot = input("\nPlease enter the time slot you would like to see, or enter 'exit' to end:\n ")
            while int(time_slot) not in unique_hours:
                time_slot = input("Your answer is not accepected, please answer again: ")
            df = df[df['hour'] == int(time_slot)]

            while True:
                print("-------------------------------------------------")
                print("Here are the time slots of photos in this area: ")
                for i in range(len(df['url'])):
                    print("{}. {}".format(i+1,df['title'].iloc[i]))
                print("-------------------------------------------------")
                photo_num = input("Please enter the number of the photo you would like to see, or enter 'exit' to end:\n")
                if photo_num == "exit":
                    break
                else:
                    while int(photo_num) not in [i+1 for i in range(len(df['url']))]:
                        photo_num = input("Your answer is not accepected, please answer again: ")
                        if photo_num == "exit":
                            break
                    location  = [df['latitude'].iloc[int(photo_num)-1],df['longitude'].iloc[int(photo_num)-1]]
                    fig = px.scatter_mapbox(df, lat='latitude', lon='longitude', zoom=15, height=300)
                    fig.add_scattermapbox(lat=[location[0]], lon=[location[1]], mode='markers', marker=dict(size=20, color='red'))
                    fig.update_layout(mapbox_style="open-street-map")
                    fig.update_layout(mapbox=dict(
            center=dict(lat=location[0], lon=location[1])),margin={"r":0,"t":0,"l":0,"b":0})
                    html_file = 'photo_location.html'
                    fig.write_html(html_file)
                    webbrowser.open(html_file)
                    webbrowser.open(df['url'].iloc[int(photo_num)-1])
            continue


if __name__ == '__main__':
    main()