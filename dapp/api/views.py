from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from django.core.urlresolvers import reverse
from serializers import AlertAPISerializer, AlertDeleteAPISerializer, SignupAPISerializer
from authentication import AuthCodeAuthentication, AlertOwnerAuthentication
from utils import send_email
from events.models import Alert, Event, User
from api.utils import get_SHA256


class SignupView(CreateAPIView):

    serializer_class = SignupAPISerializer

    def handle_exception(self, exc):
        if not isinstance(exc, ValidationError):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return super(SignupView, self).handle_exception(exc)

    def perform_create(self, serializer):
        super(SignupView, self).perform_create(serializer)
        # Send email
        email_to = serializer.instance.email
        send_email('emails/signup_created.txt', {'callback': serializer.instance.callback}, email_to)


class AlertView(CreateAPIView):

    serializer_class = AlertAPISerializer
    authentication_classes = (AuthCodeAuthentication, )

    def handle_exception(self, exc):
        if not isinstance(exc, ValidationError):
            if hasattr(exc, 'status_code'):
                return Response(status=exc.status_code)

            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return super(AlertView, self).handle_exception(exc)

    def post(self, request, *args, **kwargs):
        if request.data.get('events'):
            return super(AlertView, self).post(request, *args, **kwargs)
        else:
            AlertOwnerAuthentication().authenticate(request)
            return super(AlertView, self).post(request, *args, **kwargs)

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
                # Generate API URL
                api_url = reverse('api:alert-delete-confirm', kwargs={'delete_key':event.alert.delete_key})
                absolute_url = request.build_absolute_uri(api_url)
                # Send Email
                send_email('emails/alert_deletion_request.txt', {'alert': event.alert, 'url': absolute_url}, email_to)

                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        # email = request.query_params.get('email')
        alert_obj = None
        response_data = dict()
        try:
            alert_obj = Alert.objects.get(
                user__authentication_code=request.user.authentication_code,
                contract=request.query_params.get('contract')
            )

            for event in alert_obj.events.all():
                response_data[event.name] = dict()
                for eventvalue in event.values.all():
                    response_data[event.name][eventvalue.property] = eventvalue.value

            return Response(status=status.HTTP_200_OK, data=response_data)

        except Alert.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data={})


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



