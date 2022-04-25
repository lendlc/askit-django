from datetime import datetime, timedelta
from rest_framework import serializers
from api.models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    user_full_name = serializers.ReadOnlyField(source='user.get_full_name')
    duration_in_mins = serializers.ReadOnlyField()
    
    class Meta:
        model = Schedule
        fields = ('__all__')
        read_only_fields = ['user']
    
    def validate(self, attrs):    
        # check if datetime_end's date is same with datetime_start
        if not attrs.get('datetime_end').date() == attrs.get('datetime_start').date():
            raise serializers.ValidationError({"datetime": "end datetime should be same with start datetime"})
        # print('DATETIME CHECK: PASS')
        
        # check if schedule duration is > 1 and < 2 hours.
        duration = attrs.get('datetime_end') - attrs.get('datetime_start') #datetime.timedelta type
        if duration < timedelta(hours=1, minutes=00): # if lte 1 hour
            raise serializers.ValidationError({'datetime': 'schedule min duration is 1 hour'})
        elif duration > timedelta(hours=2, minutes=00): # if gte 2 hours
            raise serializers.ValidationError({'datetime': 'schedule max duration is 2 hours'})
        # print('DURATION CHECK: PASS')
        
        # check if there will be conflict with existing schedules.
        schedules = Schedule.objects.filter(user=self.context.get('user')).values()
        for item in schedules:
            if attrs.get('datetime_start') >= item.get('datetime_start') and attrs.get('datetime_start') <= item.get('datetime_end'):
                raise serializers.ValidationError({'datetime': 'schedule conflict'})
        # print('CONFLICT CHECK: PASS')
        
        return super().validate(attrs)
