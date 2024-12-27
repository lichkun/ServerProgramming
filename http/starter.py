import sys
import urllib.parse
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import HomeController


static_files_path = './wwwroot'

def ucfirst( input:str ) :
    if len( input ) == 0 : return input
    if len( input ) == 1 : return input[0].upper()
    return input[0].upper() + input[1:].lower()

class MainHandler( BaseHTTPRequestHandler ) :
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self.query_parameters = None

    def parse_urlencoded(self, input: str) -> dict:
        return dict(pair.split('=', maxsplit=1) if '=' in pair else (pair, None)
                    for pair in input.split('&') if pair != "") if input is not None else {}

    def serve( self ) :
        if '?' in self.path:
            path, qs = map(urllib.parse.unquote, self.path.split('?', 1))
        else:
            path, qs = urllib.parse.unquote(self.path), None

        if '../' in path:
            self.send_404()

        if self.command == "GET":
            fname = static_files_path + path
            if os.path.isfile(fname):
                self.send_file(fname)
                return


        self.query_parameters = self.parse_urlencoded(qs)

        parts = path.split('/', maxsplit=3)
        self.controller = parts[1] if len(parts) > 1 and len(parts[1]) > 0 else 'Home'
        self.action     = parts[2] if len(parts) > 2 and len(parts[2]) > 0 else 'Index'
        self.slug       = parts[3] if len(parts) > 3 else None
        controller_name = ucfirst(self.controller) + "Controller"

        controller_module = getattr(sys.modules[__name__], controller_name, None)

        print(controller_name, controller_module, sep=' | ')

        if controller_module is None:
            self.send_404()
            return

        controller_class = getattr(controller_module, controller_name, None)

        if controller_class is None:
            self.send_404()
            return


        controller_instance = controller_class(self)
        controller_action = getattr(controller_instance, self.action.lower(), None)

        if controller_action is None:
            self.send_404()
            return

        action_result = controller_action()
        if action_result.type == 'View':
            with open(static_files_path + './index.html', 'r', encoding='utf-8') as f:
                layout = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(layout.replace('@RenderBody', action_result.payload).encode())
        elif action_result.type == 'Error':
            self.send_response(action_result.code)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(action_result.payload.encode())
        elif action_result.type == 'Redirect':
            self.send_response(action_result.code if action_result.code in (301, 302) else 301)
            self.send_header('Location', action_result.payload)
            self.end_headers()




    def do_GET(self):
        self.serve()

    def do_POST(self):
        self.serve()



    def send_file(self, fname):
        ext = fname.split('.')[-1] if '.' in fname else ''
        if ext == 'txt' : mime_type = 'text/plain'
        elif ext == 'ico':
            mime_type = 'image/x-icon'
        elif ext == 'js': mime_type = 'text/x-icon'
        elif ext in ('html', 'css'): mime_type = 'text/' + ext
        else:
            mime_type = 'application/octet-stream'
        self.send_response(200)
        self.send_header('Content-Type', mime_type)
        self.end_headers()
        with open(fname, 'rb') as f:
            self.wfile.write(f.read())

    def send_404(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(static_files_path + '/404.html', 'rb') as f:
            self.wfile.write(f.read())


def main() :
    httpServer = HTTPServer( ('127.0.0.1', 81), MainHandler )
    try :
        print("Server starting ... ")
        httpServer.serve_forever()
    except:
        print("Server stopped")


if __name__ == "__main__":
    main()



'''

 Власний сервер. HTTP.
 Інший підхід до стоверння серверних програм - власний сервер
 відповідною мовою програмування
 + Немає потреби у сторонньому сервері
 - Такі сервери зазвичай повільніші
 + Робота єдиною мовою програмування
 - Потреба у гарантії вільного порту
 + Самостійний деплой, у т.ч. хостінга
 - Аналіз параметрів запиту - задача програми
 CGI
HTTP
Host

 - не "рідний" сторонній (окремий) сервер
 - власний сервер (як частина коду)
 - "рідний" сторонній сервер
'''