from django.shortcuts import render
from rest_framework.views import APIView
from django.db.models import Q
from .models import Bookings
from rest_framework import status
from .serializers import BookingsSerializer
from rest_framework.response import Response
from datetime import datetime, date
from turf.models import TurfDetails,Earnings
from accounts.permissions import IsUser, IsPartner, IsSuperUser


# Create your views here.

def add_earnings(turf, amount):
    current_date = date.today()
    if Earnings.objects.filter(turf_id=turf).exists():
        print(True)
        earnings = Earnings.objects.filter(turf_id=turf)
        if earnings[0].day == current_date:
            print(earnings[0].amount,"======",amount,"  123",earnings[0].amount + amount)
            total = earnings[0].amount + amount
            earnings[0].amount = total
            earnings[0].save()
        else:
            earning = Earnings.objects.create(turf_id=turf, amount=amount)
            earning.save()
    else:
        earning = Earnings.objects.create(turf_id=turf, amount=amount)
        earning.save()

class CheckSlotAvailibilityView(APIView):
    def post(self, request):
        turf = request.data.get('turf')
        court = request.data.get('court')
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        date = datetime.strptime(date,'%d-%m-%Y')
        format_date = date.strftime('%Y-%m-%d') 
        if Bookings.objects.filter(Q(turf=turf) & Q(date=format_date) & Q(start_time__gte=start_time) & Q(end_time__lte=end_time) & Q(court=court)).exists():
            return Response(False)
        else:
            return Response(True)

class CreateBookingView(APIView):
    def post(self, request):
        user = int(request.data.get('user'))
        print(request.data)
        turf = request.data.get('turf')
        court = request.data.get('court')
        date = request.data.get('date')
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')
        date = datetime.strptime(date,'%d-%m-%Y')
        format_date = date.strftime('%Y-%m-%d')
        cash = request.data.get('cash')
        print(turf)
        # t=TurfDetails.objects.get(turf_id=turf)
        
        add_earnings(turf, cash)
        booking = Bookings.objects.create(user_id=user,turf_id=turf,court=court,date = format_date,start_time=start_time,end_time=end_time,cash=cash)
        booking.save()
        return Response(True)
    
class ViewBookings(APIView):
    def get(self,request):
        bookings = Bookings.objects.all()
        serializer = BookingsSerializer(bookings,many=True)
        return Response(serializer.data)
    
class ViewBookingForTurf(APIView):
    permission_classes = [IsPartner]
    def get(self,request,pk):
        turf = TurfDetails.objects.get(turf_id = pk)
        if Bookings.objects.filter(turf_id=turf.id).exists():
            bookings = Bookings.objects.filter(turf_id=turf.id)
            serilaizer = BookingsSerializer(bookings, many=True)
            return Response(serilaizer.data)
        else:
            return Response("Turf not Found")
        
class ViewBookingForUser(APIView):
    # permission_classes = [IsUser]
    def get(self,request,pk):
        if Bookings.objects.filter(user_id=pk).exists():
            bookings = Bookings.objects.filter(user_id=pk).order_by('-id')
            serilaizer = BookingsSerializer(bookings, many=True)
            return Response(serilaizer.data)
        else:
            return Response("You have no bookings")
        
class CancelBookingAdmin(APIView):
    def patch(self,request,pk):
        if Bookings.objects.filter(id=pk).exists():
            booking = Bookings.objects.get(id=pk)
            booking.is_canceled = True
            booking.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
            
        