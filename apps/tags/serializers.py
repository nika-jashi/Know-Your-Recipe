from rest_framework import serializers
from apps.tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """ Serializer For Tags """
    description = serializers.CharField(write_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'description', 'created_at', 'creator']
        read_only_fields = ['id', 'created_at', 'creator']


class TagDetailSerializer(TagSerializer):
    class Meta(TagSerializer.Meta):
        fields = TagSerializer.Meta.fields + ['description']
        read_only_fields = TagSerializer.Meta.read_only_fields + ['updated_at']
