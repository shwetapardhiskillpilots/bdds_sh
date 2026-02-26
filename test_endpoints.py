import requests

BASE = "http://127.0.0.1:8000"
TOKEN = "afc90e4278fec7f69fdea02a7f879886835098a6"
HEADERS = {"Authorization": f"Token {TOKEN}"}

# All endpoints from the mobile app
endpoints = {
    "loginUrl":        ("POST", "/logine/",           None),
    "logoutApiUrl":    ("POST", "/logoutapi",          HEADERS),
    "masterPostApiUrl":("POST", "/master/postapi",     HEADERS),
    "locationUrl":     ("GET",  "/apilocation",        HEADERS),
    "juridictionUrl":  ("GET",  "/apijuridiction",     HEADERS),
    "incidentUrl":     ("GET",  "/apiincident",        HEADERS),
    "weightUrl":       ("GET",  "/apiweight",          HEADERS),
    "explosiveUrl":    ("GET",  "/master/apiexplosive", HEADERS),
    "dalamUrl":        ("GET",  "/master/dalam",       HEADERS),
    "desposeUrl":      ("GET",  "/master/despose",     HEADERS),
    "ditectionapiUrl": ("GET",  "/master/ditectionapi",HEADERS),
    "AccusedApiUrl":   ("GET",  "/master/assusedapi",  HEADERS),
    "serdesignationUrl":("GET", "/serdesignation",     HEADERS),
    "formApiUrl":      ("POST", "/formapi",            HEADERS),
    "imageapi":        ("POST", "/imageapi",           HEADERS),
    "listOnlyUrl":     ("GET",  "/listonly",           HEADERS),
    "formViewApiUrl":  ("GET",  "/formviewapi",        HEADERS),
}

print(f"{'Endpoint':<22} {'Method':<6} {'Path':<25} {'Status':<8} {'Result'}")
print("-" * 90)
for name, (method, path, hdrs) in endpoints.items():
    url = BASE + path
    try:
        if method == "POST":
            r = requests.post(url, headers=hdrs, json={}, timeout=5)
        else:
            r = requests.get(url, headers=hdrs, timeout=5)
        
        ok = "OK" if r.status_code in [200, 400, 401] else "FAIL"
        # 200 = success, 400 = bad data (but route works), 401 = needs auth (route works)
        # 404/405 = route not found / wrong method
        if r.status_code == 404:
            ok = "NOT FOUND"
        elif r.status_code == 405:
            ok = "WRONG METHOD"
        print(f"{name:<22} {method:<6} {path:<25} {r.status_code:<8} {ok}")
    except Exception as e:
        print(f"{name:<22} {method:<6} {path:<25} {'ERR':<8} {str(e)[:40]}")
