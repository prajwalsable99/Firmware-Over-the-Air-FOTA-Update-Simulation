# Firmware Over-the-Air (FOTA) Update Simulation


## Description
This project demonstrates a simple simulation of a Firmware Over-the-Air (FOTA) update process using MQTT and Streamlit. The system consists of a **publisher** that sends firmware update notifications (including version, description, file location, and checksum) to an MQTT broker, and a **subscriber** that receives these updates, downloads the firmware, verifies the checksum, and simulates applying the firmware update.

## Project Structure
```
FOTA-IMPLEMENTATION/
│
├── publisher.py          # Publisher script (Streamlit interface)
├── subscriber.py         # Subscriber script (MQTT listener and update handler)
├── uploads/              # Directory for storing uploaded firmware files (for publisher)
├── subscriber-dir/       # Directory for storing received firmware files (for subscriber)
└── README.md             # Project documentation
    
```


## How to Execute and Configure


Follow these steps to run the system:

**1. Start a Simple HTTP Server for File Access**

Before running the publisher, we need to make sure that the uploaded firmware files are accessible over HTTP. 

To do this, start a simple HTTP server to serve the uploads/ directory (where the publisher stores the firmware files).

```
Run the following command in the terminal (from the /uploads directory):


python -m http.server 8080
```

This command will start a basic HTTP server at http://localhost:8080, which will serve files from your current directory. It is necessary because the publisher provides a URL for the firmware that the subscriber will use to download the firmware. Make sure this server is running before you publish any updates.

**2. Start the Publisher (Streamlit Interface)**
Now, run the publisher script, which uses Streamlit to provide an interface for uploading firmware details and files. This will allow you to publish firmware updates to the MQTT broker.

```
Run the following command in another terminal:


streamlit run publisher.py
```

This command will start the Streamlit web interface, usually accessible at http://localhost:8501. From this interface, you can:

Enter the firmware version and description.
Upload a firmware binary file (.bin).
Click "Notify Firmware Update to Devices" to send the update notification via MQTT.

**3. Start the Subscriber (MQTT Listener)**
Finally, you need to run the subscriber script, which listens for MQTT messages and processes the firmware updates.

```
In yet another terminal window, run:


python subscriber.py
```

This will start the subscriber, which connects to the MQTT broker (broker.emqx.io) and waits for firmware update notifications. Upon receiving a message, the subscriber will download the firmware, verify the checksum, and simulate applying the firmware update with a progress bar.

## Order of Commands
-Start the HTTP server: python -m http.server 8080 – This makes the uploaded firmware files accessible over HTTP.

-Run the publisher script: streamlit run publisher.py – This opens the web interface where you can publish firmware updates.

-Run the subscriber script: python subscriber.py – This listens for update notifications and handles the firmware update process.



## Outputs 
![image](https://github.com/user-attachments/assets/376346eb-f89a-443f-aa4e-bd2347500af6)
![image](https://github.com/user-attachments/assets/fc6416c8-d6d3-4c1f-963c-ffe540f142b2)



## Technologies
```
Programming Language: Python 3.6+
Libraries:
Streamlit: For creating the user interface in the publisher.
paho-mqtt: For MQTT communication.
requests: For downloading the firmware binary.
tqdm: For showing a progress bar during the firmware update.
MQTT Broker: broker.emqx.io (public broker)
```


## How It Works

### Publisher:
The publisher script uses Streamlit to create an interface where the admin can upload a firmware file (.bin).
After filling in the firmware details (version, description), the admin can publish the update.
The publisher sends an MQTT message to the notifications/firmware_update topic containing:
firmware_version: Version of the firmware.
update_description: Description of the update.
file_location: URL of the firmware file (accessible via HTTP).
checksum: SHA-256 checksum of the firmware file.

### Subscriber:
The subscriber listens for incoming messages on the notifications/firmware_update topic.
Upon receiving a message, it downloads the firmware from the URL provided in the message.
It calculates the checksum of the downloaded firmware and verifies it against the provided checksum.
If the checksum matches, it simulates applying the firmware update with a progress bar.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
