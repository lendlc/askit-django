from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from api.models import Appointment, Schedule
from api.serializers.AppointmentSerializer import *


"""
@route  GET /admin/appointments/
@desc   View all appointments
@access Private
"""
class AppointmentsAdminList(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Appointment.objects.all()
    serializer_class = AdminAppointmentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        id = self.request.GET.get('id', None)
        if id:
            qs = qs.filter(id=id)
        return qs
    
    
class TuteeAppointment(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status', None)
        if status:
            qs = qs.filter(status=status)
        return qs
    
    def perform_create(self, serializer):
        if self.request.user.role != 'tutee':
            raise PermissionDenied()
        serializer.save(tutee=self.request.user.tutee)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        Schedule.objects.filter(id=request.data.get('tutor_schedule')).update(is_available=False)
        return Response(status=status.HTTP_201_CREATED)
