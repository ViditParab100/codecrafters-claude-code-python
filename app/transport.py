import json


def read_message():
    """
    Reads a message from the console and returns it as a Python object.
    """
    return json.loads(input())

def write_message(message):
    """
    Writes a message to the console as a JSON string.
    """
    print(json.dumps(message), flush=True)