from rest_framework.response import Response
from rest_framework import generics, permissions, status, serializers
from django.db.models import Q
from django.shortcuts import get_object_or_404

from chat.models import Conversation, Message


class ConvoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ('__all__')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user

        data['chat_with'] = instance.tutor.user.first_name if user.role == 'tutee' else instance.tutee.user.first_name

        # get last chat data
        try:
            qs = Message.objects.filter(
                conversation=instance.id).latest('created_at')
            msg = MessageSerializer(instance=qs, context={
                                    "request": self.context['request']}).data
        except Exception:
            msg = dict()

        data['last_message'] = msg

        return data


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('__all__')

    def to_representation(self, instance):
        data = super().to_representation(instance)

        req_user = self.context['request'].user
        data['current_user'] = True if req_user == instance.user else False
        return data
    

class CreateConvoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Conversation
        fields = ('__all__')


# Create your views here.
class ConversationCreate(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateConvoSerializer
    queryset = Conversation.objects.all()


class GetConservation(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        instance = user.tutee if hasattr(user, 'tutee') else user.tutor
        filter = Q(tutor=instance) if user.role == 'tutor' else Q(tutee=instance)

        convo_qs = Conversation.objects.filter(filter)
        convo_list = ConvoSerializer(
            convo_qs, many=True, context={"request": request})

        return Response(convo_list.data, status=status.HTTP_200_OK)


class GetMessages(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        convo = get_object_or_404(Conversation, id=id)
        qs = Message.objects.filter(conversation=convo.id)

        cnv = ConvoSerializer(instance=convo, context={
                              "request": request}).data
        msg = MessageSerializer(qs, many=True, context={"request": request})

        data = {
            "convsersation_data": cnv,
            "messages": msg.data
        }

        return Response(data, status=status.HTTP_200_OK)
    

class SendMessage(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        
        convo = get_object_or_404(Conversation, id=request.data.get('conversation'))
        
        Message.objects.create(
            conversation=convo,
            user=request.user,
            message=request.data.get('message')
        )
        
        return Response(status=201)