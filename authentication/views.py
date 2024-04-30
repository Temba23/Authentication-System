from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from .serializers import UserRegistrationSerializer
from rest_framework.views import APIView
from .renderers import UserRenderer


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        serializer = UserRegistrationSerializer()
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"msg":"Registration Successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)