from rest_framework import serializers
from .models import Bookings
from accounts.serializers import UserSerializer
from turf.serializers import TurfDetailsSerializer


class BookingsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    turf = TurfDetailsSerializer()
    class Meta:
        model = Bookings
        fields = '__all__'

    def create(self, validated_data):
        booking = Bookings.objects.create(user=validated_data['user'], turf=validated_data['turf'], court=validated_data['court'], date=validated_data['date'], start_time=validated_data['start_time'], end_time=validated_data['end_time'], cash=validated_data['cash'])
        booking.save()
        return booking