import argparse
import json
import zlib
import os


parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

filepath = args.file if args.file else None

try:
    file = open(filepath, 'rb')
    content = file.read()
    file.close()
except:
    print('error on opening')

try:
    js = json.loads(zlib.decompress(content).decode('utf-8'))
    print(json.dumps(js, indent=2))
except:
    print('error on json')

try:
    file = open('temp.json', 'w+')
    file.write(json.dumps(js, indent=2))
    file.close()
except:
    print('error on writing')

os.system('code temp.json')
