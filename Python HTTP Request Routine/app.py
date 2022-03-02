#Complete routine for get status hardware and sending sensor data

import requests
import json
import time

#ID hardware & Securitu Code added and set from dashboard
security_code = "kukuhgilahehe"
id_hardware = 1
motor = 1
#URL of the api
url1 = "https://flaskiot.herokuapp.com/checkhardwarestatus/"+str(id_hardware)
url2 = "https://flaskiot.herokuapp.com/addhardwarelog"

#Infinite looping (ctrl + C to stop the worker)
while True:
    # Phase 1 get hardware status
    response1 = requests.get(url1)
    responsejson1 = json.loads(response1.text)
    print("Hardware Status: "+responsejson1["data"]["status"])
    # Hardware status saved on "motor" variable for next processing (like stop the motor, etc)
    # 0 -> off & 1 -> on
    motor = responsejson1["data"]["status"]

    #phase 2 send sensor data
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
    response2 = requests.post(url2, json=body)
    responsejson2 = json.loads(response2.text)
    print(responsejson2["message"])
    #sleep 5 second
    time.sleep(5)
    continue