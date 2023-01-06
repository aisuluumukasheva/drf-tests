from rest_framework.serializers import ModelSerializer
from .models import Post


class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        exclude = ('author',)

    def validate(self, attrs):
        super().validate(attrs)
        attrs['author'] = self.context.get('request').user
        return attrs

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['author'] = instance.author.id
        return rep