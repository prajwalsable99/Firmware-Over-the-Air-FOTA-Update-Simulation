import streamlit as st
import paho.mqtt.client as mqtt
import hashlib
import os
import json

BROKER = "broker.emqx.io"  
PORT = 1883
TOPIC = "notifications/firmware_update"


UPLOAD_PATH = "uploads/"


def publish_message(firmware_version, update_desc, file_path, checksum):
    client = mqtt.Client()
    client.connect(BROKER, PORT)
    
    # Prepare the message payload
    message = {
        "firmware_version": firmware_version,
        "update_description": update_desc,
        "file_location": file_path,
        "checksum": checksum
    }
    
 
    client.publish(TOPIC, payload=json.dumps(message), qos=1)
    client.disconnect()
    return True


def calculate_checksum(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()




st.title("Firmware Update  Simulation using MQTT(FOTA)")
st.write('---')

# Input fields for firmware details
firmware_version = st.text_input("Enter Firmware Version:")
update_desc = st.text_area("Enter Update Description:")


uploaded_file = st.file_uploader("Upload Firmware Binary File (.bin)", type=["bin"])

if st.button("Notify Firmware Update to Devices"):
    if firmware_version and update_desc and uploaded_file:
        
        if not os.path.exists(UPLOAD_PATH):
            os.makedirs(UPLOAD_PATH)
        
        
        file_path = os.path.join(UPLOAD_PATH, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        
        file_url = f"http://localhost:8080/{uploaded_file.name}"

       
        checksum = calculate_checksum(file_path)
        
     
        success = publish_message(firmware_version, update_desc, file_url, checksum)
        
        if success:
            st.success("Firmware update published successfully!")
            st.write(f"**Firmware Version:** {firmware_version}")
            st.write(f"**Update Description:** {update_desc}")
            st.write(f"**File Path:** {file_url}")
            st.write(f"**Checksum:** {checksum}")
        else:
            st.error("Failed to publish firmware update. Please try again.")
    else:
        st.error("Please fill in all fields and upload a firmware file.")
