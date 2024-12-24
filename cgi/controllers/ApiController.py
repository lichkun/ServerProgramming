import json
from models.RestModel import *

class ApiController:

    def  __init__(self):
        self.response = RestModel()
        self.response.meta= RestMeta({
            'service': 'Server Application', 
            'group': 'KNP-213',
        })

    def end_with(self, status_code: int=200, data: any = None):
        if status_code !=200:
            self.response.status = RestStatus(status_code)
            print("Status: %d %s" % (status_code, self.response.status.reasonPhrase))
        self.response.data = data
        print("Access-Control-Allow-Origin: *")
        print("Access-Control-Allow-Headers: Сontent-Type, Authorization")
        print("Access-Control-Allow-Credentials: true")
        print("Content-Type: application/json; charset=utf-8")
        print()
        print(json.dumps(self.response, default=vars))

    def serve(self, am_data):
        self.am_data = am_data
        method = am_data['envs']["REQUEST_METHOD"]

        content_type = am_data['envs'].get('CONTENT_TYPE', '')
        if content_type.startswith("multipart/form-data"):
            self.handle_multipart(am_data)
            return

        self.response.meta.add('method', method)
        action_name = f"do_{method.lower()}"
        controller_action = getattr(self, action_name , None)
        if controller_action is None:
            self.end_with(405, f"Method {method} not supported in requested endpoint")
        else: 
            self.end_with(data=controller_action())

    def do_options(self):
        '''CORS/CORP - info about supported items'''
        print("Access-Control-Allow-Origin: *")
        print("Access-Control-Allow-Headers: Content-Type, Authorization")
        print("Access-Control-Allow-Credentials: true")
        print("Access-Control-Allow-Methods: GET, POST, PUT, DELETE")
        print()
        exit()

    