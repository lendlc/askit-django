from datetime import datetime, timedelta

from django.db.models.functions.datetime import ExtractDay
from django.db.models import Count
from rest_framework.response import Response
from rest_framework import generics, permissions, status

from api.models import User, Appointment



class GetDataTypeCount(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        date_today = datetime.today()
        print(date_today)
        
        tutors = User.objects.filter(role='tutor').count()
        tutees = User.objects.filter(role='tutee').count()
        today = User.objects.filter(date_joined__date=date_today).count()
        appointments = Appointment.objects.count()
        
        data = {
            "tutors": tutors,
            "tutees": tutees,
            "total_users": tutors+tutees,
            "appointments": appointments,
            "new_users": today
        }
        
        return Response(data, status=status.HTTP_200_OK)
    

class GetDonutChartData(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        tutors = User.objects.filter(role='tutor').count()
        tutees = User.objects.filter(role='tutee').count()
        
        p1, p2 = self.calculate_percentage(tutors, tutees)
        
        data = {
            "donut": [tutees, tutors],
            "tutor_percentage": p1,
            "tutee_percentage": p2
        }
        
        return Response(data, status=status.HTTP_200_OK)
    
    
    @staticmethod
    def calculate_percentage(tutors, tutees):
        total = tutors + tutees
        p_tor = (tutors/total) * 100
        p_tee = (tutees/total) * 100
        return (int(p_tor), int(p_tee))
    

class GetBarGraphData(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        today = datetime.now()
        current_week_number = today.isocalendar()[1]
        current_week_days = [today + timedelta(days=i) for i in
                             range(-1 - today.weekday(), 6 - today.weekday())]

        tutees = self.format_query_data('tutee', current_week_days)
        tutors = self.format_query_data('tutor', current_week_days)

        context = {
            "week_number": current_week_number,
            "labels": [date.strftime('%m-%d-%Y') for date in current_week_days],
            "tutees": tutees,
            "tutors": tutors
        }
        return Response(context, status=200)
    
    @staticmethod
    def format_query_data(role, current_week_days):
        data = []
        query = User.objects.filter(date_joined__range=[current_week_days[0].date(),
                                                        current_week_days[-1].date()], role=role)

        data_count = query.annotate(day=ExtractDay('date_joined')).values(
            'day').annotate(count=Count('id'))
        
        for count, date in enumerate(current_week_days):
            x = next((item['count'] for item in data_count if item['day'] == date.day), 0)
            data.append(x)
            
        return data
        
    
        
        
        
