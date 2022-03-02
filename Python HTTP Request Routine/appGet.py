#This routine for get status hardware from the server

import requests
import json
import time

#ID hardware & Securitu Code added and set from dashboard
security_code = "kukuhgilahehe"
id_hardware = 1

#Infinite looping (ctrl + C to stop the worker)
while True:
    #URL of the api
    url = "https://flaskiot.herokuapp.com/checkhardwarestatus/"+str(id_hardware)
    response = requests.get(url)
    #recieve status of hardware
    responsejson = json.loads(response.text)
    print(responsejson["data"]["status"])
    #sleep 5 second
    time.sleep(5)
    continue