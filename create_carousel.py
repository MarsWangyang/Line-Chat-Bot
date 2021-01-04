import os
import json

def carousel_food(name):
    curr_root = os.getcwd()
    path = os.path.join(curr_root, 'material', name, 'reply.json')
    with open(path, 'r') as file:
        json_arr = json.loads(file.read())
    return json_arr