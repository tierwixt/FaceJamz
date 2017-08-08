# Lightning talk demo: Tierney & Annie. Beginner Python project FaceJamz! 
# This IoT project will take a picture on the Pi & play songs for emotions.
########### Python 2.7 #############

import os
import time
import httplib, urllib, base64
import json

# step 1: take pic on pi
os.system("raspistill -o face.jpg -q 40")

# step 2: API call - Cognitive Services Emotion API
headers = {
    # Request headers
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'e959e4db119b45d88af3368880e7e640',
}

params = urllib.urlencode({
})

f = open("face.jpg", "rb")
body = f.read()
f.close()

try:
    conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))

result = json.loads(data)

# Define each emotion score from array values. Grab information from the JSON array. 
HappinessScore = result[0]["scores"]["happiness"]
SadnessScore = result[0]["scores"]["sadness"]
NeutralScore = result[0]["scores"]["neutral"]

# step 4: detect emotion & match song
# using if / and statements to determine the picture's emotion
if(HappinessScore > SadnessScore) and (HappinessScore > NeutralScore):
    # HappinessScore is largest
    # Play HappySong
    os.system("mpg321 ./AudioFiles/putyourrecordson.mp3")
    print "Happy " + str(HappinessScore*100) + "%"
if(SadnessScore > HappinessScore) and (SadnessScore > NeutralScore):
    # SadnessScore is largest
    # Play SadSong
    os.system("mpg321 ./AudioFiles/imissyou.mp3")
    print "Sad " + str(SadnessScore*100) + "%"
if (NeutralScore > HappinessScore) and (NeutralScore > SadnessScore):
    # NeutralScore is largest
    # Play NeutralSong
    os.system("mpg321 ./AudioFiles/stoletheshow.mp3")
    print "Neutral " + str(NeutralScore*100) + "%"
