import requests

class Device:
    @staticmethod
    def get_devices(settings: dict) -> list:
        token = settings['auth']['token']
        endpoint = settings['api']['endpoint'] + settings['api']['devices']
        
        headers = {'Govee-API-Key': token}
        data = requests.get(endpoint, headers=headers).json()
        
        if data["code"] != 200:
            raise ConnectionError(f"Error {data['code']}: {data['message']}")
        
        devices = data["data"]["devices"]
        
        out = []
        for data in devices:
            out.append(Device(data, settings))
        
        return out
        
        
    def __init__(self, data: dict, settings: dict):
        self.model = data["model"]
        self.device = data["device"]
        self.device_name = data["deviceName"]
        self.controllable = data["controllable"]
        self.retrievable = data["retrievable"]
        self.support_cmds = data["supportCmds"]
        self.cmd_turn = "turn" in self.support_cmds
        self.cmd_brightness = "brightness" in self.support_cmds
        self.cmd_color = "color" in self.support_cmds
        self.cmd_color_tem = "colorTem" in self.support_cmds
        self.settings = settings
        self.url = settings["api"]["endpoint"]
        self.url_devices = self.url + settings["api"]["devices"]
        self.url_device_control = self.url + settings["api"]["device_control"]
        self.url_device_state = self.url + settings["api"]["device_state"]
        self.token = settings["auth"]["token"]
        
        self.state = {
            "online": "false",
            "power_state": "off",
            "brightness": 60,
            "color": {"r": 255, "g": 255, "b": 255},
            "mode": "color", # or "temp"
            "color_temp": 5000
        }
        
        self.get_state()
        
    
    def __str__(self) -> str:
        return self.state_
    
    def get_state(self) -> dict:
        endpoint = self.url_device_state
        token = self.token
        
        headers = {'Govee-API-Key': token}
        params = {"device": self.device, "model": self.model}
        
        data = requests.get(endpoint, headers=headers, params=params).json()
        
        if data["code"] != 200:
            raise ConnectionError(f"Error {data['code']}: {data['message']}")
        
        properties = data["data"]["properties"]
        properties_json = {}
        
        property_map = {
            "online": "online", 
            "powerState": "power_state", 
            "brightness": "brightness", 
            "color": "color", 
            "colorTem": "color_temp",
            "colorTemInKelvin": "color_temp"
            }
        
        for property in properties:
            key = list(property.keys())[0]
            value = property[key]
            
            if property_map[key] == "color_temp":
                self.state["mode"] = "temp"
            
            self.state[property_map[key]] = value
            properties_json[property_map[key]] = value
        
        return properties_json

    def send_cmd(self, cmd):
        endpoint = self.url_device_control
        token = self.token
        
        headers = {'Govee-API-Key': token, "Content-Type": "application/json"}
        json = {'device': self.device, 'model': self.model, 'cmd': cmd}
        
        # TODO: Fix this
        # TODO: Find what "Fix this" means
        try:
            data = requests.put(endpoint, headers=headers, json=json).json()
        except:
            raise ConnectionError
        
        if data.get('code') != 200:
            raise ConnectionError(f"Command {cmd} raised error {data.get('code')}: {data.get('message')}")
        
        return data
    
    def turn_on(self) -> str:
        if self.state["power_state"] == "off":
            
            data = self.send_cmd({'name': 'turn', 'value': 'on'})

            if data["message"] == "success":
                self.state["power_state"] = "on"

            return data["message"]
        else:
            return "already on"
    
    def turn_off(self) -> str:
        if self.state["power_state"] == "on":
            data = self.send_cmd({'name': 'turn', 'value': 'off'})

            if data["message"] == "success":
                self.state["power_state"] = "off"

            return data["message"]
        else:
            return "already off"
    
    def set_brightness(self, value: int) -> str:
        data = self.send_cmd({'name': 'brightness', 'value': value})
        
        if data["message"] == "success":
            self.state["brightness"] = value
        
        return data["message"]
    
    def set_color(self, color: dict) -> str:
        data = self.send_cmd({'name': 'color', 'value': color})
        
        if data["message"] == "success":
            self.state["color"] = color
            self.state["mode"] = "color"
        
        return data["message"]
    
    def set_temp(self, temp: int) -> str:
        data = self.send_cmd({'name': 'colorTem', 'value': temp})
        
        if data["message"] == "success":
            self.state["color_temp"] = temp
            self.state["mode"] = "temp"
        
        return data["message"]