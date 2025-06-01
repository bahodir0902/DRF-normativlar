from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User
from accounts.serializers import UserSerializer, LoginSerializer, RegisterUserSerializer
from django.contrib.auth import login, logout
from rest_framework.permissions import IsAuthenticated, AllowAny
#
# class LoginView(APIView):
#     permission_classes = [AllowAny]
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({"token": token.key})
#

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]
#     def delete(self, request):
#         request.auth.delete()
#         return Response({"success": True})
#

class GetSessionView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data)

class UpdateUserDataView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)






