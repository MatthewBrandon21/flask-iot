#This routine for sending IoT data sensor to server

import requests
import json
import time

#ID hardware & Securitu Code added and set from dashboard
security_code = "kukuhgilahehe"
id_hardware = 1

#Infinite looping (ctrl + C to stop the worker)
while True:
    #URL of the api
    url = "https://flaskiot.herokuapp.com/addhardwarelog"
    body = {
        "id_hardware":1,
        "security_code":security_code,
        "ph_level":15,
        "temperature":17,
        "humidity":23,
        "water_level":27,
        #Image must be a base64 or blob format
        "image":"blob"
    }
    response = requests.post(url, json=body)
    responsejson = json.loads(response.text)
    print(responsejson["message"])
    #sleep 5 second
    time.sleep(5)
    continue