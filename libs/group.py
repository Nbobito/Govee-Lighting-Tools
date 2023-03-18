from time import sleep
from libs.device import Device

class Group:
    def __init__(self, device_list: list[Device] = [], settings: dict = {}):
        self.device_list = device_list
        if len(self.device_list) > 0:
            self.state = device_list[0].state
            self.settings = device_list[0].settings
        else: 
            self.state = {
                "online": "false",
                "power_state": "off",
                "brightness": 60,
                "color": {"r": 255, "g": 255, "b": 255},
                "mode": "color", # or "temp"
                "color_temp": 5000
            }
            self.settings = settings
    
    def __str__(self):
        print(self.state)
    
    def sync_state(self) -> list[Device]:
        errors = []
        
        for device in self.device_list:
            try:
                sleep(self.settings["api"]["timeout"])
                if device.cmd_turn:
                    if self.state["power_state"] == "on":
                        device.turn_on()
                    else:
                        device.turn_off()
                        
                sleep(self.settings["api"]["timeout"])
                if device.cmd_brightness:  
                    device.set_brightness(self.state["brightness"])
                
                sleep(self.settings["api"]["timeout"])
                if self.state["mode"] == "color":
                    if device.cmd_color:
                        device.set_color(self.state["color"])
                else:
                    if device.cmd_color_tem:
                        device.set_temp(self.state["color_temp"])
                        
            except ConnectionError:
                errors.append(device)
                
        return errors
    
    def add_device(self, device: Device) -> None:
        if len(self.device_list) == 0:
            self.state = device.state
            self.settings = device.settings
        self.device_list.append(device)
    
    def remove_device(self, mac_address: str) -> None:
        for index, device in enumerate(self.device_list):
            if device.device == mac_address:
                self.device_list.pop(index)

    def turn_on(self) -> list[Device]:
        self.state["power_state"] = "on"
        
        errors = self.sync_state()
        return errors
    
    def turn_off(self) -> list[Device]:
        self.state["power_state"] = "off"
        
        errors = self.sync_state()
        return errors
    
    def set_brightness(self, value: int) -> list[Device]:
        self.state["brightness"] = value
        
        errors = self.sync_state()
        return errors
    
    def set_color(self, color: dict) -> list[Device]:
        self.state["color"] = color
        self.state["mode"] = "color"
        
        errors = self.sync_state()
        return errors
    
    def set_temp(self, temp: int) -> list[Device]:
        self.state["color_temp"] = temp
        self.state["mode"] = "temp"
        
        errors = self.sync_state()
        return errors