from django.db import IntegrityError
from rest_framework import serializers
from apps.tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """ Serializer For Tags """
    name = serializers.CharField(validators=[])
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']

    def create(self, validated_data):
        tag_name = validated_data['name']

        try:
            return super().create(validated_data)
        except IntegrityError:
            existing_tag = Tag.objects.get(name=tag_name)
            return existing_tag


class TagDetailSerializer(TagSerializer):
    class Meta(TagSerializer.Meta):
        fields = TagSerializer.Meta.fields + ['description']
        read_only_fields = TagSerializer.Meta.read_only_fields + ['updated_at', 'created_at', 'creator']
