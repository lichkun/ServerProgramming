import json

def parse_http() -> dict | None:
    with open("file2.txt", "r", encoding="utf-8") as file:
        return {
            k.strip(): v.strip()
            for line in file
            if ':' in line
            for k, v in [line.split(':', 1)]
        }

def load_config(*file_paths: str) -> dict:
    config = {}
    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            config.update(json.load(file))
    return config


result = parse_http()
print(result)


config = load_config("file1.json", "file2.json")
print(config)