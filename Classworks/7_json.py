import json

def json_str_demo():

    str= '''{
        "str":"String value",
        "digital":123,
        "float": 123.456,
        "bool":true,
        "obj":{
            "x":10,
            "y":20
        },
        "arr":[1,2,3,4,5],
        "null":null
    }'''

    j = json.loads(str)
    print(j, type(j))
    for k, v in j.items():
        print(k,v,type(v))

    j['str2']="Данные кирилицей"
    print(json.dumps(j, ensure_ascii=False, indent=4))


def main() :
    json_file_demo()

def json_file_demo():
    try:
        with open(r"D:\Documents\Рабочий стол\ServerProgramming\Classworks\7_settings.json", encoding='utf-8') as file:
            j = json.load(file)
            print(type(j))
            print(j)
    except IOError as err:
        print(err)

if __name__ == '__main__': main()
