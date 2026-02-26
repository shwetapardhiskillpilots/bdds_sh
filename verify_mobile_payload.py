import requests
import json

BASE = "http://127.0.0.1:8000"
# Using the token from earlier or a known valid one
TOKEN = "14fd6f770b7fac5ae80d3ccfc6a8cc5ed9f3cce5" 
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "user" : "2",
    "fserial" : "2022_test_" + str(json.dumps(True)), # avoid duplicate serial
    "d_bomb" : "22222",
    "fdate" : "2026-2-24 14:25:25",
    "flocation" : "21.1205687,79.1441542",
    "flocation_type" : "5",
    "flocation_description" : "w2qwqwq",
    "fjuridiction" : "7",
    "fincident" : "4",
    "fweight_data" : "4",
    "fexplosive" : "5",
    "fdetonator" : "wqweqwe",
    "fswitch" : "wewqewq",
    "ftarget" : "vbhh",
    "fdistruction" : "gggvgv",
    "fassume" : "hjunui7",
    "radio_data" : "",
    "fdalam" : "4",
    "flearning" : "jnjnkkkk",
    "fassume_status_new" : "3",
    "edit_request" : "0",
    "delete_request" : "0",
    "mode_of_detection" : "10",
    "detected_description" : "cvghhh",
    "detected_pname" : "huujjj",
    "detcted_contact" : "9958598996",
    "detected_dispose" : "3",
    "dispose_name" : "bnjjhnhb",
    "dispose_contact" : "9969999998",
    "explode" : [ ],
    "death" : [ {
        "death_contact" : "3956596998",
        "death_name" : "SkillPilots Cluematrix"
    } ]
}

# Fix serial for unique test
import time
payload["fserial"] = f"TEST_{int(time.time())}"

print(f"Sending payload to {BASE}/formapi...")
r = requests.post(f"{BASE}/formapi", data=json.dumps(payload), headers=HEADERS)

print(f"Status Code: {r.status_code}")
try:
    print(f"Response: {json.dumps(r.json(), indent=2)}")
except:
    print(f"Response (text): {r.text}")

if r.status_code == 201 or r.status_code == 200:
    print("\nSUCCESS! The server accepted the exact mobile payload.")
else:
    print("\nFAILED. Check the response errors above.")
