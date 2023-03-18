import yaml
import requests
from time import sleep
from libs.device import Device
from libs.group import Group

with open('./settings.yaml', 'r') as f:
    settings = yaml.safe_load(f)


devices = Device.get_devices(settings)
bedroom = Group()

choice = 0
while choice != 5:
    print("""Choose an option below:
          ---------------------
          1. Add devices
          2. Change color
          3. Change brightness
          4. Change temperature
          5. Quit""")
    choice = int(input("> "))
    if choice == 1:
        print("""Available devices: 
          ---------------------""")
        
        for index, device in enumerate(devices):
            assert isinstance(device, Device)
            print(f"  {index + 1}. {device.device_name}")
            
        device = int(input("""
Choose one of the listed devices to add to the control group.
> """))
        
        bedroom.add_device(devices[device - 1])
        print(f"Added device '{devices[device - 1].device_name} to the group.'")
    if choice == 2:
        print("Enter the red, green, and blue values of your color (0-255).")
        r = int(input("r: \n> "))
        g = int(input("g: \n> "))
        b = int(input("b: \n> "))
        
        bedroom.set_color({"r": r, "g": g, "b": b})
        print("Changed light colors.")
    if choice == 3:
        print("Enter the brightness (0-100)")
        brightness = int(input("> "))
        
        bedroom.set_brightness(brightness)
        print("Changed brightness.")
    if choice == 4:
        print("Enter the temperature (2000-9000?)")
        temp = int(input("> "))
        
        bedroom.set_temp(temp)
        print("Changed temperature.")
    if choice == 6:
        print(f"bedroom state: {bedroom.state}")
        for i in bedroom.device_list:
            print(f"{i.device_name}: {i.state}, {i.cmd_color}, {i.cmd_color_tem}")
        
        
    
        