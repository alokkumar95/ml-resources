import requests
import json

# API_REFERENCE = https://www.hackerrank.com/work/apidocs#!/Introduction/options_intro_requests

# Learn API Implementation = https://www.hackerrank.com/blog/rest-api-interview-questions-every-developer-should-know/
path = "https://jsonmock.hackerrank.com/api/food_outlets"


def write_to_file(filename, data):
    try:
        with open("food_outlets.json", "w", encoding="utf-8") as f: ## used utf-8 to throw UnicodeEncodeError, Universal Standard
            f.write(data)
    except Exception as e:
        print(f"Failed to write to file {filename}: {e}")



try:
    r = requests.get(path)
    r.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
    # print("content", r.content)
    status_code = r.status_code
    # print(r.status_code)
    # r.json() returns a Python object (dict or list) from the JSON response
    # can also use json.loads(r.content) to convert the JSON string to a Python object
    data = r.json()
    print(type(data)) # <class 'dict'>
    # use json to serialize the data and write it to a file
    write_to_file("food_outlets.json", json.dumps(data, indent=4))
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")



#learning

# json.loads() vs json.dumps()
# deserialize: json.loads() - converts a JSON string into a Python object (dict, list, etc.)
# serialize: json.dumps() - converts a Python object into a JSON string
# parsing data to be received from API
# preparing data to be sent over HTTP request 