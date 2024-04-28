from libs.device import Device
from libs.group import Group
from flask import Flask, render_template, request, abort
import jsonschema
import yaml


with open('./settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)

devices = Device.get_devices(settings)

app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html', devices=devices)


sync_schema = jsonschema.Draft7Validator({
    "type": "object",
    "properties": {
        "devices": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "index": {"type": "integer"},
                    "power": {"type": "boolean"},
                    "mode": {"type": "string", "enum": ["color", "temp"]},
                    "brightness": {
                        "type": "integer",
                        "minimum": 0,
                        "maximum": 100
                    },
                    "temperature": { # TODO: Replace with variable range
                        "type": "integer", 
                        "minimum": 2700, 
                        "maximum": 6500
                    },
                    "color": {
                        "type": "object", 
                        "properties": {
                            "r": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 255
                            },
                            "g": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 255
                            },
                            "b": {
                                "type": "integer",
                                "minimum": 0,
                                "maximum": 255
                            }
                        }
                    }
                },
                "required": ["devices"]
            }
        }
    },
    "required": ["name", "age"]
})


@app.post('/sync')
def sync():
    data = request.json
    # TODO: fix int error in schema
    #errors = list(sync_schema.iter_errors(data))
    #if errors:
    #    abort(400, "JSON does not match schema")
        
    devices_json = data["devices"]
    for device_json in devices_json:
        device: Device = devices[int(device_json["index"]) - 1]
        if device_json["power"]:
            device.turn_on()
            device.set_brightness(int(device_json["brightness"]))
            if device_json["mode"] == "color":
                device_json_color = {}
                for i in device_json["color"]:
                    device_json_color[i] = int(device_json["color"][i])
                device.set_color(device_json_color)
            else:
                device.set_temp(int(device_json["temperature"]))
        else:
            device.turn_off()
            
    return "success"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=settings["server_settings"]["port"], debug=True)
