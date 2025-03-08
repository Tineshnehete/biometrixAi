from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers, response, exceptions
from django.utils import timezone
from ..utils.crypto import decipher
from ..utils.predict import calculate_trust_score
from ..models import Visitors
from ..serializers.visitor import VisitorSerializer
from django.db.models import F
from ..models import MouseBehavior , UserBehavior

class ResultApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return response.Response(
            data={
                "mouse":MouseBehavior.objects.filter(user_id="anon").order_by("-timestamp").first().is_legitimate,
                "keyboard": UserBehavior.objects.filter(user_id="anon").order_by("-timestamp").first().is_legitimate
            }
        )