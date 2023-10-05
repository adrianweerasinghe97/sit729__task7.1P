import time
import json
import random
from pymongo import MongoClient
import paho.mqtt.client as mqtt

NUM_LIGHTS = 1000
NUM_ROOMS = 10
LIGHTS_PER_ROOM = NUM_LIGHTS // NUM_ROOMS

# Global MongoDB variables
mongo_uri = "mongodb+srv://username:pwd@sit729.xs2wk12.mongodb.net/?retryWrites=true&w=majority"
mongo_client = MongoClient(mongo_uri)
db = mongo_client.test
collection = db.task7


def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("motion/detections")


def on_message(client, userdata, msg):
    room_with_motion = int(msg.payload)
    motion_detected(room_with_motion)


def motion_detected(room_with_motion):
    data = {
        "rooms": [],
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    for room in range(1, NUM_ROOMS + 1):
        room_data = {"room_id": room, "lights": []}
        for light in range(LIGHTS_PER_ROOM):
            status = "ON" if room == room_with_motion else "OFF"
            room_data["lights"].append({
                "light_id": (room - 1) * LIGHTS_PER_ROOM + light + 1,
                "status": status
            })
        data["rooms"].append(room_data)

    with open('lights_data.json', 'w') as f:
        json.dump(data, f)

    try:
        collection.insert_one(data)
        print(f"Motion detected in Room {room_with_motion}, data saved.")
    except Exception as e:
        print(f"Error while inserting data to MongoDB: {e}")


mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.connect("localhost", 1883, 60)

try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("Quitting.")
