import json
import redis
import numpy as np
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import views ,permissions
from ..task import keystrokes , mouse
# Redis setup
redis_client = redis.StrictRedis(host='localhost', port=6379, db=8, decode_responses=True)

class KeyStrokAnalysisView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
      
        data = json.loads(request.body)
        user_id = data.get("user_id")

        print(json.dumps(data))
        tp=timezone.now().timestamp()
        if data["typing_speed"] or data["key_hold_time"] or data['flight_time'] or data['keystroke_latency']:

            redis_client.rpush(f"user:{user_id}:behavior:kbd:{tp}", json.dumps(data))
            print(keystrokes.process_user_behavior(user_id, tp ))
        
        if data["mouse_speed"] or data["mouse_acceleration"] or data["click_variance"]:
            redis_client.rpush(f"user:{user_id}:behavior:mouse:{tp}", json.dumps(data))
            print(mouse.process_mouse_behavior(user_id, tp ))

        return JsonResponse({"e":True}, status=200)
    
class MousePatternAnalysisView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
      
        data = json.loads(request.body)
        user_id = data.get("user_id")

        print(json.dumps(data))
        tp=timezone.now().timestamp()
        redis_client.rpush(f"user:{user_id}:behavior:mouse:{tp}", json.dumps(data))
        print(mouse.process_user_behavior(user_id, tp ))

        return JsonResponse({"e":True}, status=200)