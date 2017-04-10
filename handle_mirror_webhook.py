from flask import Flask, request
import json

app = Flask(__name__)
app.config['DEBUG'] = False

@app.route('/',methods=['POST'])
def foo():
    data = json.loads(request.data)
    print(data)
    return "OK"
