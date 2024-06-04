import folium
from folium.plugins import HeatMap
import googlemaps
from datetime import datetime
import random
import time
import math
import json

# Initialize Google Maps API client with your API key
gmaps = googlemaps.Client(key='YOUR API KEY')

def setup_places_dictionary():
    """
    Function to set up a dictionary of places of interest with their coordinates.
    Returns:
        dict: Dictionary where keys are places of interest and values are lists of tuples representing coordinates.
    """
    places_of_interest = {
        'Badhus': [(59.44794994058488, 18.09073220888018), (59.44327283001473, 18.065148230546228), (59.3940580882556, 18.0465748756148),
                   (59.44294690341515, 17.951456125147537), (59.34213307384247, 17.92922574800689), (59.36848145660429, 17.96696396344869),
                   (59.373678599785706, 18.00764687527639), (59.347172347378155, 18.078902018640967), (59.352239168351254, 18.148202266792293),
                   (59.30473033637376, 18.075206029221288), (59.31069541706914, 18.1539393711438), (59.293319676076614, 17.977897819740964),
                   (59.2851454870178, 18.094011376277788), (59.314113235604886, 18.07295482853831), (59.33091714763001, 18.037861816003097),
                   (59.41874666361195, 17.824867463846186)],
        'Tennishall': [(59.3501962370499, 18.095751708652116), (59.34874720119235, 18.08313804196687), (59.3324466676996, 17.981359732506032), 
                       (59.375556381577084, 17.986536438679696), (59.33758858955645, 18.00321046868277), (59.41604246528463, 18.04245433894756),
                       (59.44350160117587, 18.100037886323506), (59.287983965333936, 17.954513484329027), (59.304545335829054, 18.07071649876507),
                       (59.38433664402812, 17.894767876148297), (59.44987318401051, 17.967173646558418), (59.37118119512312, 18.15961267171182),
                       (59.2879047834095, 18.057986242840663)],
        'Discgolfbana_18': [(59.32350186795648, 17.911360196467406), (59.45063248709513, 17.9691486511224), (59.46162211388245, 18.049088564443075),
                            (59.4893221976484, 18.305325544593938), (59.40252647092484, 17.898801867490835), (59.21778694999464, 17.96743346242743),
                            (59.164689681994815, 18.124480022234106), (59.136804455813, 18.103454681479874), (59.49232613948348, 17.71946439217541)],
        'Discgolfbana_9': [(59.39138180094271, 18.066490231019213), (59.384711530750664, 18.032091005887377), (59.334133684955916, 18.12819468549615),
                           (59.34409035598181, 17.95766743127115), (59.388695875477445, 17.960269810262897), (59.38106748939514, 18.182999276899434),
                           (59.31398403600785, 18.051342384182814), (59.50819458918449, 17.905708709034503)],
        'Mataffär': [(59.45942049110496, 18.137812949509772), (59.44482721528757, 18.07319897568153), (59.37965345565431, 17.948142418126775),
                     (59.361951173833575, 17.964295358587435), (59.40852027801632, 17.84261343915583), (59.437645403161284, 17.93234304321843),
                     (59.370421175759496, 17.855948553536024), (59.33452448584052, 18.032917674939775), (59.31870062061573, 18.056967291904893),
                     (59.34855784401132, 18.152145376742485), (59.30466053361985, 18.12951678272072), (59.275513878330834, 18.012816523256696),
                     (59.276398254296936, 17.9087208469111), (59.39844778002036, 18.03607397787578), (59.42714087161466, 17.950889922337314),
                     (59.35875758139302, 17.98053014518063), (59.35514929495639, 17.955900121105348),
                     (59.34718999741302, 18.11308098944579), (59.30928937656159, 18.02412055333962), (59.31230706389273, 18.065861265887122),
                     (59.413953984785884, 17.863957282494365), (59.3589016028862, 18.002787389164666), (59.3853467985427, 18.045151211524637),
                     (59.44339525869676, 18.09864435524354), (59.43001565086347, 17.936159459520844), (59.36115730588976, 17.96932022031216),
                     (59.361034677016875, 17.874944186292968), (59.36334624505896, 18.12350647820769), (59.28526198369383, 18.050227149359138),
                     (59.30203198601589, 18.102494629797835), (59.37751124823749, 17.908303123309892), (59.43996564769844, 18.037970470308885)],
        'Kommunikation': [(59.33081705024508, 18.058704819937034), (59.34284718480286, 18.04959980950945)],
        'Multimat': [(59.360427753860264, 17.87511813412005), (59.37599822460281, 17.969157187280697), (59.409967134253826, 17.84283263273642),
                     (59.393738577854975, 17.903280631046417), (59.29459996620017, 17.933771869543538)]
    }

    return places_of_interest

def get_commute_time_public_transport(start_coordinate, destination_coordinate):
    """
    Function to get commute time via public transport using Google Maps API.
    Args:
        start_coordinate (tuple): Coordinates of the starting point.
        destination_coordinate (tuple): Coordinates of the destination.
    Returns:
        int: Commute time in minutes.
    """
    # Perform directions API request
    directions_result = gmaps.directions(start_coordinate, destination_coordinate, mode="transit", departure_time=datetime.now())
    # Extract duration from the response
    if directions_result:
        commute_time = directions_result[0]['legs'][0]['duration']['value'] // 60
    else:
        commute_time = 600

    return commute_time

def get_commute_time_cycling(start_coordinate, destination_coordinate):
    """
    Function to get commute time by cycling using Google Maps API.
    Args:
        start_coordinate (tuple): Coordinates of the starting point.
        destination_coordinate (tuple): Coordinates of the destination.
    Returns:
        int: Commute time in minutes.
    """
    # Perform directions API request
    directions_result = gmaps.directions(start_coordinate, destination_coordinate, mode="bicycling", departure_time=datetime.now())

    # Extract duration from the response
    if directions_result:
        commute_time = directions_result[0]['legs'][0]['duration']['value'] // 60
    else:
        commute_time = 600

    return commute_time

def calculate_commute_times(start_coordinates, places_of_interest):
    """
    Function to calculate commute times from a starting coordinate to places of interest.
    Args:
        start_coordinate (tuple): Coordinates of the starting point.
        places_of_interest (dict): Dictionary where keys are places of interest and values are lists of tuples representing coordinates.
    Returns:
        dict: Dictionary where keys are places of interest and values are commute times in minutes.
    """
    commute_times = {'Coordinates': start_coordinates}

    for place, coordinates in places_of_interest.items():
        times = []
        for start_coordinate in start_coordinates:

            closest_point_1, closest_point_2 = closest_points(start_coordinate, coordinates)
            # Calculate commute time via public transport
            public_transport_time_1 = get_commute_time_public_transport(start_coordinate, closest_point_1)
            public_transport_time_2 = get_commute_time_public_transport(start_coordinate, closest_point_2)

            # Calculate commute time by cycling
            cycling_time_1 = get_commute_time_cycling(start_coordinate, closest_point_1)
            cycling_time_2 = get_commute_time_cycling(start_coordinate, closest_point_2)


            # Store the minimum of the two commute times
            cycling_time = min(cycling_time_1, cycling_time_2)
            public_transport_time = min(public_transport_time_1, public_transport_time_2)

            if cycling_time > 20:
                times.append(min(public_transport_time, 90))
            else:
                times.append(min(public_transport_time, cycling_time))
        commute_times[place] = times

    return commute_times


def distance_between_points(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance

def closest_points(reference_point, points_list):
    closest_point_1 = None
    closest_point_2 = None
    min_distance = float('inf')

    for point in points_list:
        distance = distance_between_points(reference_point, point)
        if distance < min_distance:
            min_distance = distance
            closest_point_2 = closest_point_1
            closest_point_1 = point
        elif closest_point_2 == None:
            closest_point_2 = point

    return closest_point_1, closest_point_2


def display_results(places_of_interest, commute_times):
    """
    Function to display commute times on a map of Stockholm and save it as an HTML file.
    Args:
        places_of_interest (dict): Dictionary where keys are places of interest and values are lists of tuples representing coordinates.
        commute_times (dict): Dictionary where keys are places of interest and values are commute times in minutes.
    """
    for place, coordinates in places_of_interest.items():
        # Create map centered around the first coordinate
        map_obj = folium.Map(location=coordinates[0], zoom_start=12)

        # Convert coordinates to list for HeatMap
        coords_list = [list(coord)+[commute_times[place][i]**(1/3)] for i,coord in enumerate(commute_times['Coordinates'])]
 
        # Add heatmap overlay with commute times
        HeatMap(coords_list, name="Heatmap", min_opacity=0.2, max_zoom=18, radius=50, blur=70).add_to(map_obj)

        # Add markers for places of interest
        for coord in coordinates:
            folium.Marker(location=coord, popup=place).add_to(map_obj)

        # Save map as HTML file
        map_filename = f"{place}_commute_map.html"
        map_obj.save(map_filename)
        print(f"Map saved as {map_filename}")

    # Weights for creating aggregated map
    badhus_w = 2
    tennis_w = 3
    discgolf_w = 3
    mataffär_w = 2
    kommunikation_w = 1
    multimat_w = 4

    coords_list = []
    for i, coord in enumerate(commute_times['Coordinates']):
        badhus_agg = commute_times['Badhus'][i] / badhus_w
        tennis_agg = commute_times['Tennishall'][i] / tennis_w
        discgolf_agg = min(commute_times['Discgolfbana_18'][i], commute_times['Discgolfbana_9'][i]) / discgolf_w
        mataffär_agg = commute_times['Mataffär'][i] / mataffär_w
        kommunikation_agg = commute_times['Kommunikation'][i] / kommunikation_w
        multimat_agg = commute_times['Multimat'][i] / multimat_w


        agg_time = badhus_agg + tennis_agg + discgolf_agg + mataffär_agg + kommunikation_agg + multimat_agg

        coords_list.append(list(coord) + [agg_time**(1/3)])

    map_obj = folium.Map(location=coordinates[0], zoom_start=12)

    # Add heatmap overlay with commute times
    HeatMap(coords_list, name="Heatmap", min_opacity=0.2, max_zoom=18, radius=50, blur=70).add_to(map_obj)

    # Add markers for places of interest
    #for coord in coordinates:
    #    folium.Marker(location=coord, popup=place,).add_to(map_obj)

    # Save map as HTML file
    map_filename = "Aggregated_commute_map.html"
    map_obj.save(map_filename)
    print(f"Map saved as {map_filename}")

def create_grid(north_west, south_east):
    north, west = north_west
    south, east = south_east

    grid_coordinates = []
    grid_coordinate = (north, west)

    grid_distance = 0.005

    while grid_coordinate[0] > south:
        while grid_coordinate[1] < east:
            grid_coordinates.append(grid_coordinate)
            grid_coordinate = (grid_coordinate[0], grid_coordinate[1] + grid_distance)
        grid_coordinate = (grid_coordinate[0] - grid_distance/2, west)
    return grid_coordinates

def main():
    # Set up places of interest dictionary
    places_of_interest = setup_places_dictionary()

    option = input('Which option do you want to do (answer 1, 2 or 3)\nOption 1: Do a whole new grid search\nOption 2: Only create new display\nOption 3: Calculate times on one apartment\n')
    
    if option == '1':
        # Specify starting coordinate (e.g., city center)
        start_coordinates = [(59.3293, 18.3686)]  # Example coordinate for city center
        north_west_corner = (59.43858280540564, 17.800689567052935)
        south_east_corner = (59.251883513114635, 18.208838342524505)
        start_coordinates = create_grid(north_west_corner, south_east_corner)

        # Calculate commute times
        commute_times = calculate_commute_times(start_coordinates, places_of_interest)

        # Save the results
        with open('commute_times.json', 'w') as json_file:
            json.dump(commute_times, json_file)    
        with open('places_of_interest.json', 'w') as json_file:
            json.dump(places_of_interest, json_file)    

        # Display results on map
        display_results(places_of_interest, commute_times)
    elif option == '2':
        # Load the results
        with open('commute_times.json', 'r') as json_file:
            commute_times  = json.load(json_file)  
        with open('places_of_interest.json', 'r') as json_file:
            places_of_interest = json.load(json_file)  

        # Display results on map
        display_results(places_of_interest, commute_times)
    elif option == '3':
        start_coordinate = input('What is the coordinates of the apartment?')

        commute_times = calculate_commute_times(start_coordinate, places_of_interest)
        print(commute_times)
    else:
        print(f'{option} is not a valid option')


if __name__ == "__main__":
    main()
