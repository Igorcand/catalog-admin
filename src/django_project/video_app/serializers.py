from rest_framework import serializers

class SetField(serializers.ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))
    
    def to_representation(self, data):
        return list(super().to_representation(data))
    
class CreateVideoWithoutMediaInputSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=10000, decimal_places=2)
    rating = serializers.CharField()
    categories = SetField(child=serializers.UUIDField())
    genres = SetField(child=serializers.UUIDField())
    cast_members = SetField(child=serializers.UUIDField())


class CreateVideoWithoutMediaOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class ListOutputMetaSerializer(serializers.Serializer):
    current_page = serializers.IntegerField()
    per_page = serializers.IntegerField()
    total = serializers.IntegerField()

class VideoOutputSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)
    launch_year = serializers.IntegerField()
    duration = serializers.DecimalField(max_digits=10000, decimal_places=2)
    rating= serializers.CharField() 
    opened = serializers.BooleanField()
    published = serializers.BooleanField()
    categories = serializers.ListField(child=serializers.UUIDField())
    genres = serializers.ListField(child=serializers.UUIDField())
    cast_members = serializers.ListField(child=serializers.UUIDField())

class ListOutputSerializer(serializers.Serializer):
    data = VideoOutputSerializer(many=True)
    meta = ListOutputMetaSerializer()

class RetrieveVideoInputSerializer(serializers.Serializer):
    id = serializers.UUIDField()

class RetrieveVideoOutputSerializer(serializers.Serializer):
    data = VideoOutputSerializer(source="*")