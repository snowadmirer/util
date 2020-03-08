import json

def read_json(json_file):
    with open(json_file) as f:
        return json.loads(f.read())

def write_json(json_label, json_file):
    with open(json_file, 'w') as f:
        f.write(json.dumps(json_label))
