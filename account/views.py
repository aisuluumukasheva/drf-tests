from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import RegisterSerializer

class RegisterAPIView(APIView):
    def post(self,request):
        ser = RegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(status=201)
