from os import error
import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from rest_framework import generics, serializers, status, viewsets, views
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from .serializers import (
    LoginSerializer,
    RegistrationSerializer,
    ProfileSerializer,
)


def homepage(request):
    return render(request, "api/home.html")


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        if request.data == {}:
            return Response(
                {"message": "Send request Body"}, status=status.HTTP_204_NO_CONTENT
            )
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("api:home")
            return Response(
                {"message": "Your account has been disabled"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return render(
            request,
            "api/login.html",
            {"message": "Invalid Credentials"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request, format=None):
        return render(request, "api/login.html", {})


@api_view(["GET"])
@permission_classes((IsAuthenticated,))
def logout_view(request):
    logout(request)
    return redirect("api:home")


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, format=None):
        if request.data == {}:
            return Response(
                {"message": "Send request Body"}, status=status.HTTP_204_NO_CONTENT
            )

        register_serializer = RegistrationSerializer(data=request.data)
        if register_serializer.is_valid():
            register_serializer.save()
            return redirect("api:login")
        errors = [
            register_serializer.errors[error][0] for error in register_serializer.errors
        ]
        for i in range(len(errors)):
            if errors[i] == "This field must be unique.":
                errors[i] = "Email must be unique"
        return render(
            request,
            "api/signup.html",
            {"errors": errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def get(self, request, format=None):
        return render(request, "api/signup.html")


class ProfileView(generics.CreateAPIView):
    http_method_names = ["get", "put"]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return ProfileSerializer

    def get(self, request, format=None):
        if request.method == "GET":
            username = str(request.user)
            user = User.objects.get(username=username)
            if user.is_active:
                return render(request, "api/profile.html", {"person": user})
            logout(request)
            return Response(
                {"message": "Your account is disabled. Please log in again"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

    def put(self, request, format=None):
        if request.method == "PUT":
            try:
                user = User.objects.get(username=str(request.user))
            except User.DoesNotExist:
                return Response(
                    {"message": "User doesn't exist"}, status=status.HTTP_404_NOT_FOUND
                )

            user_data = JSONParser().parse(request)
            user_serializer = self.get_serializer_class()
            user_serializer = user_serializer(user, user_data)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(
                    {
                        "message": "Data has been updated succesfully",
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Invalid Information"}, status=status.HTTP_400_BAD_REQUEST
            )
