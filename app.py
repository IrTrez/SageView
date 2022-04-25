from flask import Flask, render_template, Response, stream_with_context
from pricewebsocket import priceDataWS
import time
import json
import datetime

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

coins = ["XLM", "XRP", "ICP"]
intervals = ["1m"]
base = "BTC"
ws = priceDataWS(coins, intervals, base)
update = None
# while True:
#     print()
    # if ws.updated["1m"]:
    #     update = ws.histData
    #     ws.updated["1m"] = False
    #     break

print(update)
# time.sleep(10000)

# @app.route("/", methods=['POST', 'GET'])
def hello_world():

    def gen(coin, base=base):
        while True:
            try:
                yield ws.liveData[coin+base]
            except:
                print("error")
            time.sleep(1)
    return Response(stream_with_context(gen("XLM")))


@app.route('/')
def index():
    return render_template('test.html')


@app.route('/chart-data')
def chart_data():
    def gen(coin, base=base):
        while True:
            try:
                json_data = json.dumps(
                    {'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': ws.liveData[coin+base]})
                yield f"data:{json_data}\n\n"
            except Exception as e:
                print(e)
            time.sleep(1)


    response = Response(stream_with_context(gen("BTC", base="BNB")), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

# @app.route("/")
# def hello_world():
#     return render_template("templates/main.html")
