import time
import json
import random
from pymongo import MongoClient

NUM_LIGHTS = 1000
NUM_ROOMS = 10
LIGHTS_PER_ROOM = NUM_LIGHTS // NUM_ROOMS


def motion_detected(room_with_motion):
    data = {
        "rooms": [],
        "time": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    # Simulate lights status for each room
    for room in range(1, NUM_ROOMS + 1):
        room_data = {"room_id": room, "lights": []}
        for light in range(LIGHTS_PER_ROOM):
            status = "ON" if room == room_with_motion else "OFF"
            room_data["lights"].append({
                "light_id": (room - 1) * LIGHTS_PER_ROOM + light + 1,
                "status": status
            })
        data["rooms"].append(room_data)

    # Save to a JSON file
    with open('lights_data.json', 'w') as f:
        json.dump(data, f)

    # Connect to MongoDB on AWS EC2
    client = MongoClient('mongodb://3.223.6.139:27017/')
    db = client.lightsDB
    collection = db.motionLights

    # Insert the data
    collection.insert_one(data)

    print(f"Motion detected in Room {room_with_motion}, data saved.")


try:
    while True:
        # Simulating motion detection in a random room
        room_with_motion = random.randint(1, NUM_ROOMS)
        motion_detected(room_with_motion)
        time.sleep(10)  # Simulating checking for motion every 10 seconds
except KeyboardInterrupt:
    print("Quitting.")
