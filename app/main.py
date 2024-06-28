from flask import Flask, request
from get_earthquake_df import get_earthquake_df
from create_heatmap import create_heatmap

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to KandilliAPI!'

@app.route('/earthquakes',methods=['GET'])
def earthquakes():
    #Get the parameters from the request.
    filter = request.args.get('filter')
    limit = request.args.get('limit')
    url = request.args.get('url')
    if filter is None:
        filter = {}
    else:
        eval(filter)
    if limit is None:
        limit = 50
    else:
        limit = int(limit)
    if url is None:
        url = 'http://www.koeri.boun.edu.tr/scripts/lst2.asp'
    else:
        url = str(url)

    return get_earthquake_df(filter=filter,limit=limit,url=url).to_json(orient='records')

@app.route('/heatmap',methods=['GET'])
def heatmap():
    #Get the parameters from the request.
    filter = request.args.get('filter')
    limit = request.args.get('limit')
    url = request.args.get('url')
    if filter is None:
        filter = {}
    else:
        eval(filter)
    if limit is None:
        limit = 50
    else:
        limit = int(limit)
    if url is None:
        url = 'http://www.koeri.boun.edu.tr/scripts/lst2.asp'
    else:
        url = str(url)

    return create_heatmap(_filter=filter,_limit=limit,_url=url)

app.run()