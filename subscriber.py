import paho.mqtt.client as mqtt
import json
import hashlib
import os
import time
import requests 
from tqdm import tqdm


BROKER = "broker.emqx.io"  
PORT = 1883
TOPIC = "notifications/firmware_update"


SAVE_PATH = "./subsciber-dir/"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[ Connected to MQTT broker ]")
        client.subscribe(TOPIC, qos=1)
    else:
        print(f"Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    # print(f"Received message: {msg.payload.decode()}")
    
    firmware_info = json.loads(msg.payload.decode())
    
   
    firmware_version = firmware_info.get("firmware_version")
    file_location = firmware_info.get("file_location")
    checksum = firmware_info.get("checksum")
    
    print('------------------------------------------------------------------------------')
    print(f"Firmware Version: {firmware_version}")
    print(f"File Location: {file_location}")
    print(f"Checksum: {checksum}")
    print('\n------------------------------------------------------------------------------')
    
 
    firmware_data, file_name = download_firmware(file_location)

    if firmware_data:
        if save_firmware(firmware_data, file_name):
            print(f"[Firmware saved successfully as {file_name} ]")
        
            print('------------------------------------------------------------------------------')

        if verify_firmware(firmware_data, checksum):
            apply_firmware(firmware_data)
            print('------------------------------------------------------------------------------')
        else:
            print("Firmware update failed: checksum mismatch.")
    else:
        print("Failed to download firmware.")

def download_firmware(file_location):
    print(f"[ Downloading firmware from {file_location}... ]")
    
    if file_location.startswith("http://") or file_location.startswith("https://"):
        response = requests.get(file_location)
        if response.status_code == 200:
            file_data = response.content
            file_name = file_location.split("/")[-1]  
            return file_data, file_name
        else:
            print("Error: Failed to download the file from the server.")
            return None, None
    else:
        print("Unsupported file location format")
        return None, None

def save_firmware(firmware_data, file_name):
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)  
    save_file_path = os.path.join(SAVE_PATH, file_name)
    try:
        with open(save_file_path, "wb") as save_file:
            save_file.write(firmware_data)
        print(f"[ Firmware saved to {save_file_path} ]")
        return True
    except Exception as e:
        print(f"Error saving firmware: {e}")
        return False

def verify_firmware(firmware_data, expected_checksum):
    actual_checksum = hashlib.sha256(firmware_data).hexdigest()
    if actual_checksum == expected_checksum:
        print("[ Firmware checksum verified successfully. ]")
        return True
    else:
        print(f"Checksum mismatch! Expected: {expected_checksum}, Actual: {actual_checksum}")
        return False

# Simulate a delay for the firmware update process
def apply_firmware(firmware_data):
    print("[ Simulating applying firmware update... ]")
    
    total_steps = 100  # Total steps to apply firmware
    for step in tqdm(range(total_steps), desc="Applying Firmware", unit="step"):
        time.sleep(0.1)  # Simulate time taken for each step (e.g., flashing or verifying)
    print(f"Firmware update  successfully!")
    print('------------------------------------------------------------------------------')


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT)
    client.loop_forever()  

if __name__ == "__main__":
    main()
