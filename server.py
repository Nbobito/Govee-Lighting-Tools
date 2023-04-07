from libs.device import Device
from libs.group import Group
from flask import Flask, render_template, request
import yaml


with open('./settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

devices = Device.get_devices(settings)

app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html', devices=devices)

@app.post('/api')
def api(): 
    print(request.json["apiTest"])
    return "OOF"