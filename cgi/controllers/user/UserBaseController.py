from controllers.ApiController import ApiController
import sys
from data.user_dao import *
import json

class UserBaseController(ApiController):

    def __init__(self):
        super().__init__()
        self.response.meta.add('ctr', 'UserBaseController')

    def do_get(self):
        return{'user': 'works'}
    
    def do_post(self): # Signup
        self.db_context = self.am_data['db_context']
        body= sys.stdin.read()
        if len(body) <3: 
            self.end_with(400, "Body must not be empty")
        j =json.load(body)
        user= User( 
                name = j['user-name'], 
                email = j['user-email'],
                password = j['user-password'])
        return {'post': body,
                'db': self.db_context.test_connection(),
                'user': user}
    