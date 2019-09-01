import requests
import json
import zlib


URL = "https://www.pathofexile.com/api/public-stash-tabs?id={}"
idx = '0'


class File():

    def __init__(self, name, data):
        self.name = name
        self.data = json.dumps(data)
        self.save()

    def save(self):
        file = open(f"temp/{self.name}", 'wb+')
        file.write(zlib.compress(self.data.encode('utf-8'), 9))
        file.close()


for i in range(100):
    r = json.loads(requests.get(URL.format(idx)).text)
    idx = r['next_change_id']
    a = File(idx, r)
    k = len(r['stashes'])
    tot = 0
    for i in r['stashes']:
        tot += len(i['items'])
    print(f"{idx:<30} {k} {tot}")
