import time
import requests
import json
import random
import string
import re

# Match Twitter verification code
def get_code(email):
    url="http://xxxx.top:8080/new?email={}".format(email)  # This is the receive email API

    response = requests.get(url, timeout=10)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse JSON data
        data = response.json()

        # Assume the parameter name you want to get is 'title'
        # You can get the value of this parameter by key-value pair
        param_value = data.get('title')
        code = re.search(r'([0-9]{6})', param_value)
        # Print parameter value
        return code.group(1)
    else:
        # Request failed, print error message
        print(f'Request failed, status code: {response.status_code}')

def get_random_mail():
    email = "".join(random.choices(string.ascii_lowercase, k=random.randint(3,9)))
    return email

if __name__ == "__main__":
    print(get_code("wtf@xxxx.top"))
