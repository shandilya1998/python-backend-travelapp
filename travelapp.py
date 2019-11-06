from __future__ import print_function
from typing import List, Any
from app import app, db
from app.models import placeDescriptionTag, places, users, placeDescriptionTag, session, itinerary, itineraryItems, trips, experienceReview, userProfileTags
from app.APICalls import APICalls
from app.key import API_key
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import requests
import datetime
import random
import pickle
import copy
import time 

db.create_all()

class PopulatePlaces():

    def __init__(self, city):
        # City must be a string
        self.tag_lst = []
        # change the path to the Tags.csv file accordingly
#        tags = '/home/shandilya/TravelApp/backendTravelBuddyApp/Tags-Sheet1.csv'
#        df = pd.read_csv(tags)
#        df = df.fillna('')
#        columns = list(df.columns)
#        for col in columns:
#            vals = df[col].unique()
#            for ele in vals:
#                if not ele or '*' in ele:
#                    continue
#                self.tag_lst.append(ele)
        self.tag_lst = ['War Memorials', 'Milltary Bases, Ports', 'Famous Street Food ']
        self.city = city
        self.APICalls = APICalls()

    def add_city(self):
        for tag in self.tag_lst:
            print(tag)
            # create_query() creates a query to Places Text api to get a list of places for tag
            query = self.create_query_places_text_api(self.city,
                                                      tag)
            # call_places_api() calls Places Text API and Places Details API,
            # and stores the responses in the database
            self.call_places_api(query,
                                 tag)

    def call_places_api(self,
                        query,
                        tag):
        # call_place_text_api() calls places text search API with query
        # and returns data with place_id as key to retrieve all data for each place
        data = self.APICalls.call_places_text_api(query = query)
        # place_id is the place ID used by google to uniquely identify each place in their database
        for place_id in data:
            tag_place = placeDescriptionTag(place_id = place_id,
                                            tag = tag)
            exists = places().in_places(place_id)
            if exists:
                db.session.add(tag_place)
                db.session.commit()
            else:
                # Complete the initialization of the places object
                # Make changes in places table to that data can be added sequentially
                # as it is being queried from places API
                # call_places_details_api() queries for place details from places details API
                time.sleep(random.randint(5,
                                          40))
                place = places(place_id=place_id,
                               name = data[place_id]['name'],
                               city = self.city)
                # call_places_photos_api() queries place photos from places photos API
                # replace the next two statement based on the response
                # received from places details API and places photos API
                db.session.add(tag_place)
                db.session.add(place)
                db.session.commit()
                print('Place added')
                print(place.name)

    def create_query_places_text_api(self,
                                     city,
                                     tag):
        query = tag.strip(' ') + ' ' + 'in' + ' ' + city
        return query

#ob = PopulatePlaces('New York')
#ob.add_city()


class TripPlanner():

    def __init__(self,
               num_days,
               start_time,
               itinerary,
               start,
               end = None):
        self.trip = []
        self.sample_data = r'/Users/travelapp/Desktop\location.csv'
        self.df = pd.read_csv(self.sample_data) # this dataframe needs to be populated by the input from the user
        self.url_distance_matrix = 'https://maps.googleapis.com/maps/api/distancematrix/json'
        self.num_days = num_days
        self.start_time = start_time # start time should be in 24 hours format as is the response from google's places API
        self.itinerary = itinerary # list of place_ids that will be used to plan the trip
        self.start = start
        self.end = end


    def create_data_model(self):
        """retrieves data data for the problem
        calls distance matrix api
        currently test values have been plugged in"""
        data = {}
        # if the start and the end depot is the same in the time matrix
        # put the time taken to travel to the start and end depots directly to be a very large number
        """Uncomment the next statement when working with apis"""
        # data['time_matrix'] = self.create_time_matrix_from_api()
        # data['time_windows'] = self.create_windows(start_time)
        # data['num_days'] = self.num_days
        # data['start'] = self.start
        # data['end'] = self.end
        # data['ratings'] = []
        """Comment the next few statements when working with apis
        file = r'/Users/travelapp/Desktop/time-matrix.pickle'
        px = open(file,
                  'rb')
        data['time_matrix'] = pickle.load(px)
        px.close()
        Comment till here"""
        data['time_matrix'] = [
            [1000, 6, 7, 9, 7, 3, 6, 2, 3, 2, 6, 6, 4, 4, 5, 9, 7, 1000],
            [6, 1000, 8, 3, 2, 6, 8, 4, 8, 8, 13, 7, 5, 8, 12, 12, 14, 6],
            [9, 8, 1000, 11, 10, 6, 3, 9, 5, 8, 14, 15, 14, 13, 9, 18, 9, 15],
            [8, 3, 11, 1000, 1, 7, 10, 6, 10, 10, 14, 6, 7, 9, 14, 6, 16, 14],
            [7, 2, 10, 3, 1000, 6, 9, 4, 10, 19, 13, 4, 6, 18, 12, 8, 14, 9],
            [3, 6, 6, 7, 6, 1000, 2, 8, 2, 2, 7, 9, 7, 7, 6, 12, 8, 3],
            [6, 8, 3, 10, 9, 2, 1000, 6, 2, 5, 4, 12, 10, 10, 6, 15, 5, 10],
            [2, 4, 9, 6, 4, 3, 6, 1000, 4, 4, 18, 5, 4, 23, 7, 8, 10, 12],
            [3, 8, 5, 10, 8, 2, 2, 4, 1000, 3, 4, 9, 8, 7, 3, 13, 6, 5],
            [2, 8, 8, 10, 9, 2, 5, 4, 3, 1000, 4, 6, 5, 4, 3, 9, 5, 8],
            [6, 13, 4, 14, 13, 7, 4, 8, 4, 4, 1000, 10, 9, 8, 4, 13, 4, 9],
            [6, 7, 15, 6, 24, 9, 12, 5, 9, 6, 10, 1000, 1, 3, 7, 13, 10, 11],
            [4, 5, 14, 8, 6, 7, 10, 4, 8, 5, 9, 1, 1000, 2, 26, 4, 8, 1],
            [4, 8, 13, 9, 8, 7, 10, 13, 7, 4, 8, 3, 2, 1000, 4, 5, 6, 2],
            [5, 12, 9, 14, 12, 2, 6, 7, 13, 13, 4, 7, 6, 4, 1000, 9, 12, 4],
            [9, 10, 18, 6, 8, 12, 20, 8, 3, 9, 13, 3, 4, 5, 9, 1000, 9, 10],
            [7, 14, 9, 16, 14, 8, 5, 10, 6, 5, 4, 10, 8, 6, 2, 9, 1000, 13],
            [1000, 4, 4, 6, 9, 2, 5, 8, 4, 2, 5, 15, 7, 1, 5, 13, 1, 1000]
        ]

        data['time_windows'] = [
            (0, 35),  # depot
            (7, 12),  # 1
            (10, 15),  # 2
            (16, 18),  # 3
            (10, 13),  # 4
            (0, 2),  # 5
            (5, 10),  # 6
            (0, 12),  # 7
            (5, 10),  # 8
            (0, 3),  # 9
            (10, 13),  # 10
            (6, 8),  # 11
            (0, 5),  # 12
            (5, 10),  # 13
            (7, 8),  # 14
            (10, 15),  # 15
            (11, 25),  # 16
            (24, 30)  # 17, must make sure can get back to depot.
            #     anything less than 30 will fail unless you
            #     can drop destinations (using disjunctions)
        ]
        data['num_days'] = 4
        data['start'] = 0#, 0, 0, 0]  # ,17,0,17]
        #data['end'] = [0, 0, 0, 0]
        data['ratings'] = [200, 10, 1000, 20, 3000, 30, 1220, 40, 20, 5000, 30, 6000, 50, 70, 90, 8000]
        # greater penalty means that the node will not be dropped
        # test whether node index or int64 in
        #        data_ = []
        #        for rating in data['ratings']:
        #            data_.append(5-rating)
        #        data['rating'] = data_
        return data


    def create_time_windows(self):
        """Create the time windows for all places in the itinerary based on opening and closing times in the database"""
        self.start_time = (self.start_time/100)*60*60
        time_windows = []
        for place_id in self.itinerary:
            place = db.session.query(places).filter_by(place_id=place_id).first()
            opening_hours = place.openingHours
            weekday = datetime.datetime.now().weekday()

            if 'Open 24 hours' in opening_hours['periods']['weekday_texts'][weekday]:
                opening_time = int('0000')
                closing_time = int('2359') # review this later
            else:
                times = opening_hours['periods'][weekday]
                opening_time = int(times['open']['time'])
                closing_time = int(times['close']['time'])
            opening_time = (opening_time/100)*60*60
            closing_time = (closing_time/100)*60*60

            if opening_time - self.start_time < 0:
                opening_time = 0
            else:
                opening_time = opening_time - self.start_time

            if closing_time > self.start_time:
                closing_time = closing_time - self.start_time
            else:
                raise ValueError('Start time should be less than the closing time of all places in itinerary')

            time_windows.append((opening_time, closing_time))
        return time_windows


    def create_time_matrix_from_api(self):
        """helper function to create the time matrix from Google maps Distance Matrix API"""
        addresses = ''
        time_matrix = []
        for place_id in self.df['place_id'].values:
            addresses = addresses + '|' + 'place_id:' + place_id

        addresses = addresses[1:]

        for place_id in self.df['place_id'].values:
            search_payload = {"key": API_key,
                              "origins": 'place_id:' + place_id,
                              "destinations": addresses}
            response = requests.get(self.url_distance_matrix,
                                    search_payload)
            data = response.json()
            temp = []
            for ele in data['rows'][0]['elements']:
                if ele['status'] == 'OK':
                    temp.append(ele['duration']['value'])
                else:
                    temp.append(0)
            time_matrix.append(copy.deepcopy(temp))

        return time_matrix


    def print_solution(self,
                       data,
                       manager,
                       routing,
                       assignment):
        """prints the final routing solution on the console"""
        time_dimension = routing.GetDimensionOrDie('Time')
        total_time = 0

        for vehicle_id in range(data['num_days']):
            index = routing.Start(vehicle_id)
            plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
            while not routing.IsEnd(index):
                time_var = time_dimension.CumulVar(index)
                plan_output += '{0} Time({1},{2}) -> '.format(
                    manager.IndexToNode(index), assignment.Min(time_var),
                    assignment.Max(time_var))
                index = assignment.Value(routing.NextVar(index))
            time_var = time_dimension.CumulVar(index)
            plan_output += '{0} Time({1},{2})\n'.format(
                manager.IndexToNode(index), assignment.Min(time_var),
                assignment.Max(time_var))
            plan_output += 'Time of the route: {}min\n'.format(
                assignment.Min(time_var))
            print(plan_output)
            total_time += assignment.Min(time_var)

        print('Total time of all routes: {}min'.format(total_time))

    def plan_trip(self, disjunction):
        """Entry point of the program."""
        # Instantiate the data problem.
        data = self.create_data_model()

        # set the time horizon based on the time windows, to be safe
        horizon = 0
        for w in data['time_windows']:
            horizon = max(w)

        # Create the routing index manager.
        if type(data['start']) == list and data['end']:
            manager = pywrapcp.RoutingIndexManager(
                len(data['time_matrix']), data['num_days'], data['start'], data['end'])
        else:
            manager = pywrapcp.RoutingIndexManager(
                len(data['time_matrix']), data['num_days'], data['start'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)
        try:
            # Create and register a transit callback.
            def time_callback(from_index, to_index):
                """Returns the distance between the two nodes."""
                # Convert from routing variable Index to distance matrix NodeIndex.
                from_node = manager.IndexToNode(from_index)
                to_node = manager.IndexToNode(to_index)
                return data['time_matrix'][from_node][to_node]
        except Exception as e:
            print(e)

        try:
            transit_callback_index = routing.RegisterTransitCallback(time_callback)

            # Define cost of each arc.
            routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
            print(horizon)

            # Add Distance constraint.
            dimension_name = 'Time'
            routing.AddDimension(
                transit_callback_index,
                0,  # maximum waiting time for a vehicle (slack)--full simulation time
                horizon,  # model horizon time
                False,  # start cumul to zero
                dimension_name)
            time_dimension = routing.GetDimensionOrDie(dimension_name)
            # Add time window constraints for each location except depot.
            for location_idx, time_window in enumerate(data['time_windows']):
                # do not set time windows for depot nodes here
                if location_idx in data['start'] or location_idx in data['end']:
                    continue
                index = manager.NodeToIndex(location_idx)
                print('location', location_idx, 'index', index, time_window, time_dimension.CumulVar(index))
                time_dimension.CumulVar(index).SetRange(time_window[0], time_window[1])
                print('location', location_idx, 'index', index, time_window, time_dimension.CumulVar(index))
            # Add time window constraints for each vehicle start node.
            print('set vehicle start and end node time windows')
            for vehicle_id in range(data['num_days']):
                index = routing.Start(vehicle_id)
                time_dimension.CumulVar(index).SetRange(data['time_windows'][0][0],
                                                        data['time_windows'][0][1])
                print('index', index, data['time_windows'][0], time_dimension.CumulVar(index))

                # setting a time window on the routing end node is a
                # bad idea if you can't actually get back to the depot
                endindex = routing.End(vehicle_id)
                time_dimension.CumulVar(endindex).SetRange(data['time_windows'][17][0],
                                                           data['time_windows'][17][1])
                print('index', endindex,
                      data['time_windows'][17][0],
                      data['time_windows'][17][1],
                      time_dimension.CumulVar(endindex))
            for i in range(data['num_days']):
                routing.AddVariableMinimizedByFinalizer(
                    time_dimension.CumulVar(routing.Start(i)))
                routing.AddVariableMinimizedByFinalizer(
                    time_dimension.CumulVar(routing.End(i)))

            time_dimension.SetSpanCostCoefficientForAllVehicles(30)
        except Exception as e:
            print(e)

        i = 0
        if disjunction:
            for node in range(0, len(data['time_matrix']) - 1):
                if type(data['start']) == list and (node in data['start'] or node in data['end']):
                    continue
                elif type(data['start']) == int and node == data['start']:
                    continue
                penalty = data['ratings'][i]
                routing.AddDisjunction([manager.NodeToIndex(node)], penalty)
                i += 1
                if i >= len(data['ratings']):
                    break

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        # set guided local to perturb solutions
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        # must have a time limit for guided local, or it will run forever
        search_parameters.time_limit.seconds = 10  # 1 * 60  # timelimit minutes
        # dump the log to the screen
        search_parameters.log_search = pywrapcp.BOOL_TRUE

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)
        # Print solution on console.
        print(bool(solution))
        print(disjunction)

        if solution:
            self.print_solution(data, manager, routing, solution)
        elif not solution and disjunction:
            print('no solution')
        else:
            print('Trip Not possible')
            print('here is a possible trip for you')
            self.plan_trip(disjunction=True)


#ob = TripPlanner()
#ob.plan_trip(disjunction=False)
#ob = PopulatePlaces('New York')
#ob.add_city()
