from rest_framework import serializers
from .models import *
from accounts.models import UserData
from accounts.serializers import UserSerializer


class TurfPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricing
        fields = '__all__'
        

        
        

class AddReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRatings
        fields = '__all__'
        
class EarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Earnings
        fields = '__all__'
class TurfDetailsSerializer(serializers.ModelSerializer):
    price = TurfPricingSerializer()
    turf = UserSerializer()
    class Meta:
        model = TurfDetails
        fields = '__all__'
        
    def create(self, validated_data):
        turf = TurfDetails.objects.create(turf=validated_data['turf'],price = validated_data['price'], place=validated_data['place'],lat=validated_data['lat'],lng=validated_data['lng'],fives=validated_data['fives'],sevens=validated_data['sevens'],elevens=validated_data['elevens'],cricket=validated_data['cricket'],cafe=validated_data['cafe'],first_aid=validated_data['first_aid'],locker=validated_data['locker'],parking=validated_data['parking'],shower=validated_data['shower'],logo=validated_data['logo'],approved=validated_data['approved']) 
        turf.save()
        return turf  

class ReviewRatingsSerializer(serializers.ModelSerializer):
    turf_id = serializers.PrimaryKeyRelatedField(source='turf', queryset=TurfDetails.objects.all())
    total_ratings = serializers.IntegerField(read_only=True)

    class Meta:
        model = ReviewRatings
        fields = ('turf_id', 'rating', 'total_ratings')

class ShowReviewsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    turf = TurfDetailsSerializer()
    
    class Meta:
        model = ReviewRatings
        fields = '__all__'
     
class TurfUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TurfDetails
        fields = '__all__'
        
    def create(self, validated_data):
        turf = TurfDetails.objects.create(turf=validated_data['turf'],price=validated_data['price'],place=validated_data['place'],lat=validated_data['lat'],lng=validated_data['lng'],fives=validated_data['fives'],sevens=validated_data['sevens'],elevens=validated_data['elevens'],cricket=validated_data['cricket'],cafe=validated_data['cafe'],first_aid=validated_data['first_aid'],locker=validated_data['locker'],parking=validated_data['parking'],shower=validated_data['shower'],logo=validated_data['logo'],approved=validated_data['approved']) 
        turf.save()
        return turf  

     
    
    
   