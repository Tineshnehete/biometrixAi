import numpy as np
import pandas as pd
import json
import redis
from django.utils.timezone import now
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from ..models import UserBehavior
from background_task import background
# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=8, decode_responses=True)

def generate_synthetic_data(num_samples=1000):
    np.random.seed(42)
    keystroke_latency = np.random.normal(100, 20, num_samples)  # in ms
    key_hold_time = np.random.normal(50, 10, num_samples)  # in ms
    flight_time = np.random.normal(80, 15, num_samples)  # in ms
    typing_speed = np.random.normal(200, 30, num_samples)  # characters per minute
    return np.column_stack([keystroke_latency, key_hold_time, flight_time, typing_speed]).T


def get_user_profile(user_id):
    historical_data = UserBehavior.objects.filter(user_id=user_id).values_list(
        "keystroke_latency", "key_hold_time", "flight_time", "typing_speed"
    )
    
    if not historical_data:
        return None
    return np.column_stack(historical_data)

# @background(schedule=1)
def process_user_behavior(user_id, tp):
    key = f"user:{user_id}:behavior:kbd:{tp}"
    data_list = redis_client.lrange(key, 0, -1)
    print(key)
    # redis_client.delete(key)  # Clear Redis queue after processing

    if not data_list:
        return 0

    behavior_data = [json.loads(data) for data in data_list]
    features = np.array([[d["keystroke_latency"], d["key_hold_time"], d["flight_time"], d["typing_speed"]] for d in behavior_data])
   

    data = get_user_profile(user_id=user_id)
    if data is None:
        data = generate_synthetic_data()
    scaler = StandardScaler()
    iso_forest = IsolationForest()
    print(data.T)
    data_s = scaler.fit_transform(data.T)
    iso_forest.fit(data_s)
    

    features_scaled = scaler.transform(features)
    predictions = iso_forest.predict(features_scaled)


   
    for i, data in enumerate(behavior_data):
        UserBehavior.objects.create(
            user_id=user_id,
            keystroke_latency=data["keystroke_latency"],
            key_hold_time=data["key_hold_time"],
            flight_time=data["flight_time"],
            typing_speed=data["typing_speed"],
            is_legitimate=True if predictions[i] == 1 else False,
            timestamp=now(),
        )
        print(data)
    return predictions