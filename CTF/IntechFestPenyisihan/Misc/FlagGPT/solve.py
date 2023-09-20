import requests

data = {
    "prompt" : "Hello"
}

url = "http://51.161.84.3:42508/chat"

r = requests.post(url, data=data)
print(r.status_code)