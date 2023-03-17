

from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast

app = Flask(__name__)
api = Api(app)

# endpoints
class Users(Resource):
    # methods go here
    
    def get(self):
        data = pd.read_csv('users.csv') # read CSV
        data = data.to_dict() # convert dataframe to dict.
        return {'data': data}, 200   # 200 is OK code.
    # pass
    
    # add records to our data.
    def post(self):
        parser = reqparse.RequestParser() # initialize
        
        parser.add_argument('userId', required=True) # add args
        parser.add_argument('name', required=True) # add args
        parser.add_argument('city', required=True) # add args
        
        args = parser.parse_args() # parse arguments to dict.
        
        # read our CSV
        data = pd.read_csv('users.csv')
        
        # adding a check if the name already exists
        if args['userId'] in list(data['userId']):
            return {
                'message': f" '{args['userId']}' already exists."
            }, 401  # 
        else:
            # create new dataframe containing new values.
            new_data = pd.DataFrame(
                {
                    'userId': args['userId'],
                    'name': args['name'],
                    'city': args['city'],
                    'locations': [[]]
                })
        
        # append new_data to dataframe
        data = data.append(new_data, ignore_index=True)
        
        # save back to csv
        data.to_csv('users.csv', index=False)
        return {'data':data.to_dict()}, 200 # return data with 200 OK
    
    # modify a user location. we want to add a cafe location to a user.
    def put(self):
        
        parser = reqparse.RequestParser()
        parser.add_argument('userId', required=True)
        parser.add_argument('location', required=True)
        
        args = parser.parse_args()
        
        # read csv
        data = pd.read_csv('users.csv')
        
        if args['userId'] in list(data['userId']):
            
            #
            data['locations'] = data['locations'].apply(lambda x: ast.literal_eval(x))
            
            # select our user.
            user_data = data[data['userId'] == args['userId']]
            
            # update the users location
            user_data['locations'] = user_data['locations'].values[0].append(args['location'])
            
            # save back to csv
            data.to_csv('users.csv', index=False)
            return {'data':data.to_dict()}, 200 # return data with 200 OK
        
        else:
            # otherwise user not found
            return {'message': f" '{args['userId']}' user not found."}, 404
        
    
    # to delete user.
    def delete(self):
        
        parser = reqparse.RequestParser()
    
        parser.add_argument('userId', required=True)
        
        args = parser.parse_args()
        
        # read csv
        data = pd.read_csv('users.csv')
        
        # check if user exists.
        if args['userId'] not in list(data['userId']):
            return 'message:' f" '{args['userId']}' does not exists ", 404
        else:
            # delete the row of userId
            data = data[data['userId'] != args['userId']]  
            
            # save as csv
            data.to_csv('users.csv', index=False)
            return {'data':data.to_dict()}, 200

class Locations(Resource):
    # methods go here
    pass


# Flask needs to know that this class is an endpoint for our API, and so we pass Resource in with the class definition.
api.add_resource(Users, '/users') # '/users' is our entry point for Users.

api.add_resource(Locations, '/locations') # '/locations is our entry point for Locations.


if __name__ == '__main__':
    app.run()  # run our Flask app
    

    




