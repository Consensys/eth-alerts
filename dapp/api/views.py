from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.core.urlresolvers import reverse
from serializers import AlertAPISerializer, AlertDeleteAPISerializer, SignupAPISerializer
from utils import send_email
from events.models import Alert, Event, User
from api.utils import get_SHA256

from django.core import serializers


class SignupView(CreateAPIView):

    serializer_class = SignupAPISerializer

    def handle_exception(self, exc):
        if not isinstance(exc, ValidationError):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return super(SignupView, self).handle_exception(exc)


class AlertView(CreateAPIView):

    serializer_class = AlertAPISerializer

    def perform_create(self, serializer):
        super(AlertView, self).perform_create(serializer)
        # Send email
        email_to = serializer.instance.email.email
        api_url = reverse('api:alert-confirm', kwargs={'confirmation_key':serializer.instance.confirmation_key})
        absolute_url = serializer.context['request'].build_absolute_uri(api_url)
        send_email('emails/alert_created.txt', {'alert': serializer.instance, 'url':absolute_url}, email_to)

    def handle_exception(self, exc):
        if not isinstance(exc, ValidationError):
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return super(AlertView, self).handle_exception(exc)

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

        email = request.query_params.get('email')
        alerts_query_set = Alert.objects.filter(email__email=email)

        if alerts_query_set.count() > 0:

            contracts = dict()
            # Retrieve contracts
            for alert in alerts_query_set:
                events = alert.events.all()

                for event in events:
                    contract_address = str(event.contract.address)
                    values = []

                    if event.name:
                        name = event.name.name
                    else:
                        name = None

                    for value in event.values.all():
                        v = dict()
                        v[str(value.property)] = str(value.value)
                        values.append(v)

                    contract_dict = dict()
                    contract_dict['eventName'] = name
                    contract_dict['values'] = values

                    if contract_address in contracts:
                        contracts[contract_address].append(contract_dict)
                    else:
                        contracts[contract_address] = [contract_dict]

            return Response(status=status.HTTP_200_OK, data=contracts)

        else:
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



