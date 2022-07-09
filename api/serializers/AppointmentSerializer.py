from rest_framework import serializers
from api.models import Appointment


class AdminAppointmentSerializer(serializers.ModelSerializer):
    tutee_email = serializers.ReadOnlyField(source='tutee.user.email')
    tutor_email = serializers.ReadOnlyField(source='tutor_schedule.user.email')
    duration = serializers.ReadOnlyField(source='tutor_schedule.duration_in_mins')
    
    class Meta:
        model = Appointment
        fields = ('__all__')
        depth=1 # fetch all related models
        

class AppointmentSerializer(serializers.ModelSerializer):
    tutor_email = serializers.ReadOnlyField(source='tutor_schedule.user.email')
    start = serializers.ReadOnlyField(source='tutor_schedule.datetime_start')
    end = serializers.ReadOnlyField(source='tutor_schedule.datetime_end')
    
    class Meta:
        model = Appointment
        fields = ('__all__')
        read_only_fields = ['tutee']
        
    

