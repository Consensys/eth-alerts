from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from serializers import AlertAPISerializer, AlertDeleteAPISerializer
from utils import send_email
from events.models import Alert, Event
from api.utils import get_SHA256


class AlertView(CreateAPIView):

    serializer_class = AlertAPISerializer

    def perform_create(self, serializer):
        super(AlertView, self).perform_create(serializer)
        # Send email
        email_to = serializer.instance.email.email
        try:
            send_email('emails/alert_created.txt', {'alert': serializer.instance}, email_to)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        serializer = AlertDeleteAPISerializer(data=request.data)

        if serializer.is_valid():
            address = serializer.data.get('address')
            eventName = serializer.data.get('eventName')

            # Find alert
            events_query_set = Event.objects.filter(contract__address=address)
            if events_query_set.count() == 1:
                event = events_query_set[0]
                email_to = event.alert.email.email
                # delete_key = event.alert.delete_key

                try:
                    send_email('emails/alert_deletion_request.txt', {'alert': event.alert}, email_to)
                except:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AlertConfirmView(APIView):

    def get(self, request, confirmation_key):
        # Get Alert by confirmartion_key
        alerts_query_set = Alert.objects.filter(confirmation_key=confirmation_key)

        if alerts_query_set.count() == 1:
            alert = alerts_query_set[0]
            alert.is_confirmed = True
            alert.confirmation_key = get_SHA256()
            alert.save()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AlertDeleteView(CreateAPIView):

    def get(self, request, delete_key):
        # Get Alert by delete_key
        alerts_query_set = Alert.objects.filter(delete_key=delete_key)

        if alerts_query_set.count() == 1:
            alert = alerts_query_set[0]
            alert.delete()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)



