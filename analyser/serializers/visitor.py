from rest_framework import serializers
from ..models import Visitors
class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitors
        fields = "__all__"