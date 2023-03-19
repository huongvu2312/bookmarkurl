from django.db.models import Q, Case, When, Value, IntegerField
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Bookmark, Category
from .serializers import BookmarkSerializer, CategorySerializer, BookmarkSerializerDetail, CategorySerializerMinimal
from user.models import User


class NewestBookmarksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        bookmarks = Bookmark.objects.filter(
            user=request.user).order_by('-created_at')[0:5]
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)


class UsedBookmarksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        bookmarks = Bookmark.objects.filter(
            user=request.user).order_by('-copy')[0:5]
        serializer = BookmarkSerializer(bookmarks, many=True)
        return Response(serializer.data)


class BookmarksList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, bookmark_id=None):
        if bookmark_id:
            bookmark = Bookmark.objects.get(id=bookmark_id)
            serializer = BookmarkSerializerDetail(bookmark)
            return Response(serializer.data, status=status.HTTP_200_OK)

        bookmarks = Bookmark.objects.filter(
            user=request.user).order_by('-created_at')
        serializer = BookmarkSerializerDetail(bookmarks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookmarkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, bookmark_id=None):
        try:
            bookmark = Bookmark.objects.get(id=bookmark_id)
            removeCategory = request.data.get('removeCategory', '')
            if removeCategory:
                noCategory = Category.objects.filter(
                    user=request.user).get(slug='no-category')
                request.data["category"] = noCategory.id
            serializer = BookmarkSerializer(
                bookmark, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data})
            else:
                return Response({"status": "error", "data": serializer.errors})
        except Bookmark.DoesNotExist:
            raise Http404

    def delete(self, request, bookmark_id=None):
        bookmark = get_object_or_404(Bookmark, id=bookmark_id)
        bookmark.delete()
        return Response({"status": "success", "data": "Bookmark deleted!"})


class CategoryList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, category_slug=None):
        if category_slug:
            category = Category.objects.filter(
                user=request.user).get(slug=category_slug)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        categorys = Category.objects.filter(
            user=request.user).annotate(
            custom_order=Case(
                When(slug="no-category", then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('custom_order', 'name')
        serializer = CategorySerializer(categorys, many=True)
        return Response(serializer.data)

    def post(self, request):
        slug = slugify(request.data.get('name', ''))
        request.data["slug"] = slug
        serializer = CategorySerializerMinimal(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_slug=None):
        try:
            slug = slugify(request.data.get('name', ''))
            request.data["slug"] = slug
            category = Category.objects.filter(
                user=request.user).get(slug=category_slug)
            serializer = CategorySerializer(
                category, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "data": serializer.data})
            else:
                return Response({"status": "error", "data": serializer.errors})
        except Bookmark.DoesNotExist:
            raise Http404

    def delete(self, request, category_slug=None):
        category = Category.objects.filter(
            user=request.user).get(slug=category_slug)
        category = get_object_or_404(
            Category, user=request.user, slug=category_slug)
        category.delete()
        return Response({"status": "success", "data": "Category deleted!"})


@api_view(['POST'])
def newCategoryDefault(request):
    try:
        email = request.data.get('email', '')
        user = User.objects.get(email=email)
        serializer = CategorySerializer(data={
            'name': 'No category',
            'slug': 'no-category'
        })

        if serializer.is_valid():
            try:
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        raise Http404


@api_view(['PUT'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def addCopy(request, bookmark_id, format=None):
    try:
        bookmark = Bookmark.objects.get(id=bookmark_id)
        bookmark.copy += 1
        bookmark.save()
        serializer = BookmarkSerializer(bookmark)
        return Response(serializer.data)
    except Bookmark.DoesNotExist:
        raise Http404
