import numpy as np
import pandas as pd
import json
import redis
from django.utils.timezone import now
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from scipy.spatial.distance import mahalanobis
from ..models import MouseBehavior

# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=8, decode_responses=True)

# Generate synthetic data for mouse dynamics (Replace with real data)
def generate_mouse_data(num_samples=1000):
    np.random.seed(42)
    mouse_speed = np.random.normal(300, 50, num_samples)  # pixels per second
    mouse_acceleration = np.random.normal(10, 2, num_samples)  # change in speed per second
    click_variance = np.random.normal(5, 1, num_samples)  # variability in click timing
    return np.column_stack([mouse_speed, mouse_acceleration, click_variance])



def get_mouse_profile(user_id):
    historical_data = MouseBehavior.objects.filter(user_id=user_id).values_list(
        "mouse_speed", "mouse_acceleration", "click_variance"
    )
    if not historical_data:
        return None
    return np.array(historical_data)

def process_mouse_behavior(user_id, tp):
    key = f"user:{user_id}:behavior:mouse:{tp}"
    data_list = redis_client.lrange(key, 0, -1)
    redis_client.delete(key)  # Clear Redis queue after processing

    if not data_list:
        return 0

    # Load and preprocess data
    mouse_data = generate_mouse_data() if get_mouse_profile(user_id) is None else get_mouse_profile(user_id)
    mouse_scaler = StandardScaler()
    mouse_data_scaled = mouse_scaler.fit_transform(mouse_data)

    # Train Isolation Forest model
    mouse_iso_forest = IsolationForest(contamination=0.05, random_state=42)
    mouse_iso_forest.fit(mouse_data_scaled)
    behavior_data = [json.loads(data) for data in data_list]
    mouse_features = np.array([[d["mouse_speed"], d["mouse_acceleration"], d["click_variance"]] for d in behavior_data])

    # Normalize and predict
    mouse_features_scaled = mouse_scaler.transform(mouse_features)
    mouse_predictions = mouse_iso_forest.predict(mouse_features_scaled)

    # Store results in SQLite
    for i, data in enumerate(behavior_data):
        MouseBehavior.objects.create(
            user_id=user_id,
            mouse_speed=data["mouse_speed"],
            mouse_acceleration=data["mouse_acceleration"],
            click_variance=data["click_variance"],
            is_legitimate=True if mouse_predictions[i] == 1 else False,
            timestamp=now(),
        )
        print(True if mouse_predictions[i] == 1 else False, "Legitimate")
    return mouse_predictions

# Example real-time analysis
# new_mouse_data = [320, 12, 6]  # Example new user's mouse behavior
# print("User Mouse Analysis:", detect_mouse_legitimacy(new_mouse_data, user_id=1))
