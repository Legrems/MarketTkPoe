import requests
from bs4 import BeautifulSoup
import re
import json
from flask import Flask, Response, request, render_template
from settings import *


app = Flask(__name__)


stock_re = r"Stock: [0-9]+"


class Result():

    def __init__(self):
        self.URL = "http://currency.poe.trade/search?league={}&want={}&have={}"

    def getData(self, league='', want=0, have=0):

        html_doc = requests.get(self.URL.format(league, want, have)).text
        # print(html_doc)

        soup = BeautifulSoup(html_doc, 'html.parser')

        offers = soup.findAll("div", {"class": "displayoffer"})

        js = {
            'want': want,
            'have': have,
            'offers': [],
        }

        for o in offers:
            soup = BeautifulSoup(str(o), 'html.parser')
            offer = str(soup.findAll("div", {"class": "displayoffer-middle"})[0])[33:][:-6]
            name = str(soup.findAll("a")[0])[75:][:-13]
            s = [i for i in re.finditer(stock_re, str(o))]
            if s == []:
                s = '?'
            else:
                # print(f"{s[0].start()}:{s[0].end()}")
                s = int(str(o)[s[0].start()+7:s[0].end()])
            x, _, y = offer.split(' ')
            x, y = float(x), float(y)
            r = x / y if x > y else y / x
            # print(f"{r:4.2f}{x:>7} << {y:<7} S:{s:<4}=> {name}")
            js['offers'].append({
                'from': x,
                'to': y,
                'stock': s,
                'name': name,
            })

        return json.dumps(js, indent=2)


class Currency():

    def __init__(self, idx, name):
        self.id_list = idx
        self.name_list = name
    
    def get_id(self, name):
        for i in range(len(self.name_list)):
            if name.upper() in self.name_list[i].upper():
                return self.id_list[i]
        
        return -1


currency = Currency([i[0] for i in TAB_ALL], [i[1] for i in TAB_ALL])


@app.route('/')
def hello_world():

    return render_template('base.html')


@app.route('/dashboard')
def dashboard():

    context = {
        'projects': [
            {'name': 'Database storage', 'done':5},
            {'name': 'Search for item', 'done':10},
            {'name': 'Customization', 'done':0},
            {'name': 'Currency graph list', 'done':10},
            {'name': 'API', 'done':20},
        ],
    }

    return render_template('theme/index.html', context=context)


@app.route('/api')
def api():
    try:
        want = request.args['want']
    except:
        want = 0
    try:
        have = request.args['have']
    except:
        try:
            have = reuest.args['inexchangeof']
        except:
            have = 0
    try:
        league = request.args['league']
    except:
        league = 'Standard'
    
    print(f"{want} {have}")
    
    want = currency.get_id(want)
    have = currency.get_id(have)

    print(f"{want} {have}")

    res = Result()

    js = res.getData(league, want, have)
    return Response(js, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
