from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from serializers import AlertAPISerializer
from utils import send_email


class AlertCreateView(CreateAPIView):

    serializer_class = AlertAPISerializer

    def perform_create(self, serializer):
        super(AlertCreateView, self).perform_create(serializer)
        # Send email
        email_to = serializer.instance.email.email
        send_email('emails/alert_created.txt', {'alert': serializer.instance}, email_to)
        return Response(status=status.HTTP_201_CREATED)

