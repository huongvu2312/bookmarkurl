from rest_framework import serializers

from .models import User
from bookmark.serializers import CategorySerializer, BookmarkSerializer


class UserSerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(many=True)
    categorys = CategorySerializer(many=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "bookmarks",
            "categorys"
        )
