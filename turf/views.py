from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg
from django.db.models import Sum
from accounts.permissions import IsPartner,IsSuperUser,IsUser
from datetime import date
from .models import *

class AddTurfDetailsView(APIView):
    permission_classes = [IsPartner]
    def post(self, request):
        print(request.data)
        serializer = TurfUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class EditTurfView(APIView):
    def put(self, request, pk):
        try:
            turf = TurfDetails.objects.get(turf_id=pk)
        except TurfDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        print(request.data)
        serializer = TurfUpdateSerializer(turf, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ShowReviewView(APIView):
    def get(self, request,pk):
        if ReviewRatings.objects.filter(turf_id=pk).exists():
            reviews = ReviewRatings.objects.filter(turf_id=pk)
            serializer = ShowReviewsSerializer(reviews, many=True)
            return Response(serializer.data)
        else:
            return Response(False)
        
        
class AddReviewRatingView(APIView):
    permission_classes = [IsUser]
    def post(self, request):
        serializer = AddReviewRatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class TurfDetailsView(APIView):
    def get(self, request):
        turfs = TurfDetails.objects.filter(approved=True, unlisted=False)
        serializer = TurfDetailsSerializer(turfs, many=True)
        return Response(serializer.data)
    
class ApproveTurfView(APIView):
    # permission_classes = [IsSuperUser]
    def patch(self, request, pk):
        try:
            turf = TurfDetails.objects.get(pk=pk)
        except TurfDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        turf.approved = True
        turf.save()
        return Response(status=status.HTTP_200_OK)
    
class RejectTurfView(APIView):
    # permission_classes = [IsSuperUser]
    def patch(self, request, pk):
        try:
            turf = TurfDetails.objects.get(pk=pk)
        except TurfDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        turf.approved = False
        turf.save()
        return Response(status=status.HTTP_200_OK)
        
class ViewTurfUserView(APIView):
    # permission_classes = 
    def get(self, request, pk):
        if TurfDetails.objects.filter(id=pk).exists():
            turf = TurfDetails.objects.get(id=pk)
            serializer = TurfDetailsSerializer(turf)
            return Response(serializer.data)
        else:
            return Response(False)
             
class TurfRetrieveUpdateDestroyView(APIView):
    permission_classes = [IsPartner]
    def get(self, request, pk):
        if TurfDetails.objects.filter(turf_id=pk).exists():
            turf = TurfDetails.objects.get(turf_id=pk)
            # courts = turf.price.all()
            # print(courts)
            serializer = TurfDetailsSerializer(turf)
            return Response(serializer.data)
        else:
            return Response(False)
            
    def put(self, request, pk):
        turf = TurfDetails.objects.get(id=pk)
        print(request.data)
        serializer = TurfDetailsSerializer(turf, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        turf = TurfDetails.objects.get(pk=pk)
        turf.delete()
        return Response("Turf deleted successfully")
    
class SetTurfPriceView(APIView):
    permission_classes = [IsPartner]
    def post(self, request):
        print(request.data)
        serializer =  TurfPricingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        # return Response("done")
        
class UpdateTurfPriceView(APIView):
    def put(self, request, pk):
        print(request.data)
        turf = Pricing.objects.get(id=pk)
        serializer = TurfPricingSerializer(turf, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
        
class TopRatedView(APIView):
    def get(self, request):
        turf_ratings = TurfDetails.objects.annotate(avg_rating=Avg('reviewratings__rating')).order_by('avg_rating').all()
        print(turf_ratings[0])
        turf_serializer = TurfDetailsSerializer(turf_ratings, many=True)
        return Response(turf_serializer.data)
    
class WithdrawnEarningsView(APIView):
    def patch(self,request,pk):
        if Earnings.objects.filter(id=pk).exists():
            earnings = Earnings.objects.get(id=pk)
            earnings.status = "Withdrawn"
            earnings.save()
            return Response("Withdrawn")
        else:
            return Response("Not found")
            
    
class UnlistTurfView(APIView):
    # permission_classes = [IsPartner]
    def patch(self, request, pk):
        try:
            turf = TurfDetails.objects.get(pk=pk)
        except TurfDetails.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        turf.unlisted = True
        turf.save()
        return Response(status=status.HTTP_200_OK)
        
        
class EarningsView(APIView):
    def get(self, request, pk):
        if Earnings.objects.filter(turf_id=pk).exists():
            earnings = Earnings.objects.filter(turf_id=pk)
            serializer = EarningsSerializer(earnings, many=True)
            return Response(serializer.data)
        else:
            return Response(False)