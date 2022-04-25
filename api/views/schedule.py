from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import generics, permissions, status

from api.models import Schedule
from api.serializers import ScheduleSerializer

"""
@route    GET /admin/schedules/
@desc     Get all User Schedules
@access   Private
"""
class Schedules(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


"""
@route  POST /schedule/
@desc   Create a Schedule
@access Private
"""
class ListCreateSchedule(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        #filter schedule by logged in user, return [] if there are none.
        return qs.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED)

"""
@route  GPD /schedule/<id>/
@desc   Retrieve, Edit or Delete Schedule
@access Private
"""
class GetEditDeleteSchedule(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    
    def get_object(self):
        # #get initial object
        obj = super().get_object()
        # raise 403 error if logged in user does not own schedule
        if not obj.user == self.request.user:
            raise PermissionDenied()
        return obj

    


