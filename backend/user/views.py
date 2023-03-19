from rest_framework import authentication, permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from .models import User
from .serializers import UserSerializer


class MyAccount(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        try:
            user = request.user

            new_password = request.data.get('new_password', '').strip()
            if len(new_password) > 0:
                old_password = request.data.get('old_password', '').strip()
                if user.check_password(old_password):
                    try:
                        password_validation.validate_password(
                            new_password, user)
                        user.set_password(new_password)
                        user.save()
                        return Response({"status": "success", "data": "Update password!"})
                    except ValidationError as error:
                        return Response(error, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"data": "The old password is incorrect!"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                serializer = UserSerializer(
                    user, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "success", "data": serializer.data})
                else:
                    return Response({"status": "error", "data": serializer.errors})
        except User.DoesNotExist:
            raise Http404
