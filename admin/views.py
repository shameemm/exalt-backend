from django.shortcuts import render
from rest_framework.views import APIView
from turf.serializers import TurfDetailsSerializer,TurfUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsPartner,IsSuperUser
from turf.models import TurfDetails
from accounts.models import UserData
from accounts.serializers import UserSerializer

class UserDetailsView(APIView):
    # permission_classes = [IsSuperUser]
    def get(self,request):
        users = UserData.objects.filter(is_superuser = False,is_partner = False)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
class UserBlockView(APIView):
    # permission_classes = [IsSuperUser]
    def patch(self, request, pk):
        try:
            user = UserData.objects.get(pk=pk)
        except TurfDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.is_active = False
        user.save()
        return Response(status=status.HTTP_200_OK)
    
class UserUnBlockView(APIView):
    # permission_classes = [IsSuperUser]
    def patch(self, request, pk):
        try:
            user = UserData.objects.get(pk=pk)
        except TurfDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)
