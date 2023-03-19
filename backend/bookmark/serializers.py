from rest_framework import serializers

from .models import Category, Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%d.%m.%Y", required=False)

    class Meta:
        model = Bookmark
        fields = (
            "id",
            "url",
            "copy",
            "note",
            "created_at",
            "category",
            "get_absolute_url",
        )


class CategorySerializer(serializers.ModelSerializer):
    bookmarks = BookmarkSerializer(many=True, required=False)

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url",
            "bookmarks",
        )


class CategorySerializerMinimal(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug",
            "get_absolute_url",
        )


class BookmarkSerializerDetail(serializers.ModelSerializer):
    category = CategorySerializerMinimal()
    created_at = serializers.DateTimeField(format="%d.%m.%Y")

    class Meta:
        model = Bookmark
        fields = (
            "id",
            "url",
            "copy",
            "note",
            "created_at",
            "category",
            "get_absolute_url",
        )
