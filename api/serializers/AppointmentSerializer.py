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
    tutor_id = serializers.ReadOnlyField(source='tutor_schedule.user.id')
    tutor_email = serializers.ReadOnlyField(source='tutor_schedule.user.email')
    tutor_full_name = serializers.ReadOnlyField(source='tutor_schedule.user.get_full_name')
    tutee_id = serializers.ReadOnlyField(source='tutee.user.id')
    tutee_full_name = serializers.ReadOnlyField(source='tutee.user.get_full_name')
    subject = serializers.ReadOnlyField(source='tutor_schedule.subject')
    start = serializers.ReadOnlyField(source='tutor_schedule.datetime_start')
    end = serializers.ReadOnlyField(source='tutor_schedule.datetime_end')
    
    class Meta:
        model = Appointment
        fields = ('__all__')
        read_only_fields = ['tutee']

    

