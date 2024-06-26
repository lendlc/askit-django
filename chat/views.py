from rest_framework.response import Response
from rest_framework import generics, permissions, status, serializers
from django.db.models import Q
from django.shortcuts import get_object_or_404

from api.models import Tutee, Tutor, Appointment
from chat.models import Conversation, Message


class ConvoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversation
        fields = ('__all__')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user = self.context['request'].user
        
        if user.role == 'tutee':
            chat_with = instance.tutor.user.get_full_name()
            chat_with_id = instance.tutor.user.id
        else:
            chat_with = instance.tutee.user.get_full_name()
            chat_with_id = instance.tutee.user.id

        data.update({
            'chat_with': chat_with,
            'chat_with_id': chat_with_id
        })

        # get last chat data
        try:
            qs = Message.objects.filter(
                conversation=instance.id).latest('created_at')
            msg = MessageSerializer(instance=qs, context={
                                    "request": self.context['request']}).data
        except Exception:
            msg = None

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

    def post(self, request):
        appointment = request.data.get('appointment')

        if appointment:
            try:
                conversation = Conversation.objects.get(appointment=appointment)
                convo = ConvoSerializer(conversation, context={"request": request})
                return Response(convo.data, status=200)
            except Exception:
                pass

        tutee = get_object_or_404(Tutee, user=request.data.get('tutee'))
        tutor = get_object_or_404(Tutor, user=request.data.get('tutor'))
        appointment = get_object_or_404(Appointment, id=appointment)

        conversation = Conversation.objects.create(
            tutee=tutee,
            tutor=tutor,
            appointment=appointment
        )

        convo = ConvoSerializer(conversation, context={"request": request})
        return Response(convo.data, status=201)


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
            "conversation_data": cnv,
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
