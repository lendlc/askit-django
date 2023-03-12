from rest_framework import serializers, generics, permissions, status
from rest_framework.response import Response

from .models import Video
from api.models import Tutor
from api.serializers import UserListSerializer


# Serializers go Here
class UploadVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Video
        fields = ('__all__')
    
class TutorSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    class Meta:
        model = Tutor
        fields = ('__all__')
        
        
class VideoSerializer(serializers.ModelSerializer):
    tutor = TutorSerializer()
    class Meta:
        model = Video
        fields = ('id', 'title', 'description', 'file', 'tutor', 'created_at', 'modified_at')
        

class VideoList(generics.ListAPIView):
    """ pwede na din may query dito using ?tutor=id """
    permission_classes = (permissions.AllowAny,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get('tutor')
        if q:
            qs = qs.filter(tutor=q)
        return qs
    
class VideoByID(generics.RetrieveUpdateDestroyAPIView):
    """For this, use PATCH na lang din for the update"""
    permission_classes = (permissions.AllowAny,)
    lookup_field = 'id'
    queryset = Video.objects.all()
    serializer_class = UploadVideoSerializer
    
class MyVideos(generics.ListAPIView):
    """ uploaded videos by current logged in tutor, substitute sa filter"""
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
    def get_queryset(self):
        qs = super().get_queryset()
        #filter schedule by logged in user, return [] if there are none.
        return qs.filter(tutor=self.request.user.tutor)
    

class TutorUploadVideo(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        if hasattr(request.user, 'tutor'):
            payload = {
                "title": request.data.get('title'),
                "description": request.data.get('description'),
                "file": request.data.get('file'),
                "tutor": request.user.tutor
            }
            serializer = UploadVideoSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response(status=401) 