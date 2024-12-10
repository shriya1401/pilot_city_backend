from flask import Blueprint
from flask_restful import Api, Resource  # used for REST API building

# Create a Blueprint for the API
student_api = Blueprint('student_api', __name__,
                        url_prefix='/api')

# Initialize the Flask-RESTful API
api = Api(student_api)

# Define the StudentAPI with its individual endpoints
class StudentAPI:
    class _Spencer(Resource): 
        def get(self):
            # Create a dictionary for John's data
            spencer_data = {
                "FirstName": "Spencer",
                "LastName": "Lyons",
                "DOB": "September 11, 2009",
                "Residence": "San Diego",
                "Email": "spencerl11709@stu.powyusd.com",
                "age": "15"
            }
            return spencer_data  # Return the dictionary
    class _Kushi(Resource): 
        def get(self):
            # Create a dictionary for Jeff's data
            Kushi_data = {
                "FirstName": "Kushi",
                "LastName": "Gade",
                "DOB": "January 23, 2009",
                "Residence": "San Diego",
                "Email": "kushig507@gmail.com",
                "age": "15"
            }
            return Kushi_data  # Return the dictionary
        
    class _Nora(Resource): 
        def get(self):
            # Create a dictionary for Jeff's data
            Nora_data = {
                "FirstName": "Nora",
                "LastName": "Ahadian",
                "DOB": "May 24, 2009",
                "Residence": "San Diego",
                "Email": "Nahadian@stu.powayusd.com",
                "age": "15"
            }
            return Nora_data  # Return the dictionary

    class _Soni(Resource): 
        def get(self):
            # Create a dictionary for Soni's data
            soni_data = {
                "FirstName": "Soni",
                "LastName": "Dhenuva",
                "DOB": "January 29, 2009",
                "Residence": "San Diego",
                "Email": "sonika.dhenuva@gmail.com",
                "age": "15"
            }
            return soni_data  # Return the dictionary

    class _Vibha(Resource): 
        def get(self):
            # Create a dictionary for Soni's data
            vibha_data = {
                "FirstName": "Vibha",
                "LastName": "Mandayam",
                "DOB": "October 19, 2008",
                "Residence": "San Diego",
                "Email": "vibhamandayam08@gmail.com",
                "age": "16"
            }
            return vibha_data  
        
    # Building REST API endpoints
    api.add_resource(_Spencer, '/student/spencer')          
    api.add_resource(_Kushi, '/student/kushi') 
    api.add_resource(_Soni, '/student/soni')  
    api.add_resource(_Nora, '/student/nora')  
    api.add_resource(_Vibha, '/student/vibha')  
