#!C:/Users/nikit/AppData/Local/Programs/Python/Python313/python.exe
import os, json ,urllib.parse, sys,codecs

sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())

#os.environ - переменные окружения, через которые передаются данные от сервера (Apache) до CGI-скрита

def send_error(code: int=400, phrase: str = "Bad Request", explain: str =None):
    print("Status: %d %s" % (code, phrase))
    print("Content-Type: text/plain; charset=utf-8")
    print()
    print( explain if explain != None else phrase, end='')
    exit()


envsUL = '<ul>'+ ''.join("<li>%s= %s</li>" % (k,v) for k,v in os.environ.items())+ "</ul>"

envs= {k: v for k,v in os.environ.items() if k in ('REQUEST_METHOD', 'QUERY_STRING', 'REQUEST_URI')}
# в переменные окружения заголовки идут с ключами, которые начинаются "HTTP_"
# дальше в верхнем регистре идёт заголовок, в котором "-" измененые на "_"
# Исключения: Content-Type и Content-Lenght, которые будут без префикса
headers =  {(k[5:] if k.startswith('HTTP_') else k).lower().replace("_","-"): v
             for k,v in os.environ.items() 
             if k.startswith("HTTP_") or k in ('CONTENT_TYPE,CONTENT_LENGTH')} 

query_string = urllib.parse.unquote(envs['QUERY_STRING'], encoding="utf-8")
query_params= dict( pair.split('=', maxsplit=1 )if '=' in pair  else (pair, None)
                for pair in query_string.split('&') if pair != "")

body_parameters={}
body = sys.stdin.read()
if body != '' :
    # если есть тело, то нужно определить Content-Type
    if headers['content-type'] == 'application/json':
        body_parameters = json.loads(body)
    elif headers['content-type'] == 'application/x-www-form-urlencoded':
        body_parameters = dict( pair.split('=', maxsplit=1 )  
                for pair in urllib.parse.unquote(body).split('&') if pair != "" and '=' in pair )
    else :
        send_error(415, "Unsupported Media Type", "Supported MIME: 'application/json' , 'aplication/x-www-form-urlencoded' ")

# envs['REQUEST_URI'] - адрес запроса (без хоста), но с QUERY_STRING 
# поскольку QUERY_STRING обработан отдельно, убираем его из адресса
# В файл .htaccess добавляем шаблонное правило (которое содержит .+ или .*) и это позволяет 
# переходить к основному скрипту из разных запросов, то есть реализовать маршрутизацию
path = envs['REQUEST_URI']
if '?' in path :
    path = path[:(path.index('?'))]


print("Content-Type: application/json; charset=utf-8")
print()
print(json.dumps(body_parameters, ensure_ascii=False), end="")
#print(envsUL+ "<pre>"+body+"</pre>", end="")

