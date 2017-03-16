from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from django.core.urlresolvers import reverse
from serializers import AlertAPISerializer, SignupAPISerializer
from authentication import AuthCodeAuthentication, AlertOwnerAuthentication
from utils import send_email
from events.models import Alert, DApp, Event
from django.views.generic import TemplateView, RedirectView
import json


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
        email_to = self.request.user.email
        auth_code = self.request.auth.authentication_code
        dapp_name = self.request.auth.name
        self.request.auth.delete()
        # Send email
        send_email('emails/dapp_deleted.txt', {'auth_code': auth_code, 'dapp_name': dapp_name}, email_to)
        return Response(status=status.HTTP_200_OK, data={})

    def get(self, request):

        # email = request.query_params.get('email')
        alert_obj = None
        response_data = dict()
        try:
            alert_obj = Alert.objects.get(
                dapp__authentication_code=request.auth.authentication_code,
                contract=request.query_params.get('contract')
            )

            for event in alert_obj.events.all():
                response_data[event.name] = dict()
                for eventvalue in event.event_values.all():
                    response_data[event.name][eventvalue.property] = eventvalue.value

            return Response(status=status.HTTP_200_OK, data=response_data)

        except Alert.DoesNotExist:
            return Response(status=status.HTTP_200_OK, data={})


class AdminView(TemplateView, RedirectView):
    template_name = 'views/alerts.html'

    def get_context_data(self, **kwargs):
        auth_code = self.request.GET.get('code')
        if auth_code:
            try:
                dapp = DApp.objects.get(authentication_code=auth_code)
                alerts = dapp.alert_set.all()
                kwargs['dapp'] = dapp

                for alert in alerts:
                    selected_events = []
                    alert.abi = json.loads(alert.abi)
                    alert.abi = filter(lambda item: item.get('type') == 'event', alert.abi)
                    for event in alert.events.all():
                        selected_events.append(event.name)

                    setattr(alert, 'selected_events', selected_events)
                kwargs['alerts'] = alerts
            except DApp.DoesNotExist as e:
                kwargs['dapp'] = None
                kwargs['alerts'] = None

        return kwargs

    def post(self, request, *args, **kwargs):
        """Updates an Alert and its events"""
        events = filter(lambda item: item[0] != 'csrfmiddlewaretoken' and item[0] != 'contract', request.POST.items())
        auth_code = request.GET.get('code')
        contract = request.POST.get('contract')
        operation_type = request.POST.get('operation_type')
        return_message = ''

        if auth_code:
            if operation_type == 'DELETE':
                try:
                    dapp_obj = DApp.objects.get(authentication_code=auth_code)
                    dapp_obj.delete()
                    return_message = 'DApp was deleted'
                except DApp.DoesNotExist:
                    return self.get(request, *args, **kwargs)

            else:
                try:
                    alert_obj = Alert.objects.get(
                        dapp__authentication_code=auth_code,
                        contract=contract
                    )
                except Alert.DoesNotExist:
                    return self.get(request, *args, **kwargs)

                if events:
                    events_obj = Event.objects.filter(alert=alert_obj.id)
                    events_obj.delete()

                    for event in events:
                        event_obj = Event()
                        event_obj.name = event[0]
                        event_obj.alert = alert_obj
                        event_obj.save()

                    return_message = 'Alert was updated.'
                else:
                    # Delete Alert
                    alert_obj.delete()
                    return_message = 'Alert was deleted.'

        kwargs['message'] = return_message
        return self.get(request, *args, **kwargs)






