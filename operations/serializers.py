from rest_framework import serializers
from .models import Box


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            "id",
            "length",
            "breadth",
            "height",
            "area",
            "volume",
            "created_by",
            "last_updated",
        ]


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = [
            "id",
            "length",
            "breadth",
            "height",
            "area",
            "volume",
            "last_updated",
        ]



class BoxSerializerRestricted(serializers.Serializer):
    id = serializers.IntegerField()
    length = serializers.FloatField()
    breadth = serializers.FloatField()
    height = serializers.FloatField()
    area = serializers.FloatField()
    volume = serializers.FloatField()
