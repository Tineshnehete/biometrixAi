from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import serializers, response, exceptions
from django.utils import timezone
from ..utils.crypto import decipher
from ..utils.predict import calculate_trust_score
from ..models import Visitors
from ..serializers.visitor import VisitorSerializer
from django.db.models import F

class StaticAnalyserSerializer(serializers.Serializer):
    fp = serializers.CharField(max_length=255)
    cpp = serializers.CharField(max_length=255)
    blb = serializers.ListField()


class StaticAnanlyzeApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        req_serialiser = StaticAnalyserSerializer(data=request.data)
        print(req_serialiser.is_valid())
        if req_serialiser.is_valid():
            fingerprint = decipher(request.data.get("blb"))
            print(calculate_trust_score(fingerprint))
            v ,_ = Visitors.objects.update_or_create(
                visitorID=request.data.get("cpp"),
                defaults={
                    "visitorID":request.data.get("cpp"),
                    "fingerprint": request.data.get("fp"),
                    "last_visit": timezone.now(),
                    "static_trust_score":calculate_trust_score(fingerprint)
                }
            )
            v.visits= v.visits + 1 
            v.save()

            res = {
                
            }

            return response.Response(data={**VisitorSerializer(v).data, **res })
        raise exceptions.ValidationError(detail=req_serialiser.errors)
