import json
from data.db_context import DbContext


class AmData:
    def __init__(self, envs, path, controller, category, slug):
        self.db_context = DbContext()
        self.envs = envs
        self.path = path
        self.controller = controller
        self.category = category
        self.slug = slug
        self.query_params = self._parse_query_string(envs.get('QUERY_STRING', ''))

    def _parse_query_string(self, query_string):
        """Parse query string into dictionary of parameters"""
        if not query_string:
            return {}

        params = {}
        pairs = query_string.split('&')
        for pair in pairs:
            if not pair:
                continue
            if '=' in pair:
                key, value = pair.split('=', 1)
                params[key] = value
            else:
                params[pair] = None
        return params


from models.RestModel import RestModel, RestMeta


class UserBaseController:
    def serve(self, am_data: AmData):
        meta = {
            "service": "Server Application",
            "group": "KN-P-213",
            "ctr": self.__class__.__name__,
            "method": am_data.envs.get('REQUEST_METHOD', 'GET'),
            "params": am_data.query_params  
        }

        response = RestModel(
            status=200,
            meta=meta,
            data={"user": "works"}
        )

        print("Content-Type: application/json")
        print()
        print(json.dumps(response.to_json(), ensure_ascii=False))