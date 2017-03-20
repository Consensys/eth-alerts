# eth-alerts
API for subscribing an email account for contract events

Settings
--------

For configuration purposes, the following table maps the 'dapp' environment variables to their Django setting:

| Environment Variable | Django Setting | Development Default | Production Default|
|----------------------|----------------|---------------------|-------------------|
|DJANGO_SETTINGS_MODULE| none | dapp.settings.local|dapp.settings.production|
|EMAIL_HOST | EMAIL_HOST | none | smtp.gmail.com|
|EMAIL_HOST_PASSWORD | EMAIL_HOST_PASSWORD | none | *** |
|EMAIL_HOST_USER | EMAIL_HOST_USER | none | noreply@gnosis.pm|
|EMAIL_PORT | EMAIL_PORT | 2525 | 587|
|EMAIL_SUBJECT_PREFIX | EMAIL_SUBJECT_PREFIX | none | '[gnosis alerts]' |
|EMAIL_USE_TLS| none | none | True |
|DEFAULT_FROM_EMAIL| DEFAULT_FROM_EMAIL | none |'gnosispm <noreply@gnosis.pm>' |
|EMAIL_BACKEND | none | 'django.core.mail.backends.filebased.EmailBackend'| 'email_log.backends.EmailBackend'|
|EMAIL_LOG_BACKEND | none | 'django.core.mail.backends.smtp.EmailBackend'| 'django.core.mail.backends.smtp.EmailBackend'|
|EMAIL_FILE_PATH | none | '/tmp/app-messages' | none |
|ETHEREUM_NODE_HOST | ETHEREUM_NODE_HOST | localhost | localhost |
|ETHEREUM_NODE_PORT |ETHEREUM_NODE_PORT | 8545 | 8545|
|ETHEREUM_NODE_SSL| ETHEREUM_NODE_SSL| False | False |

Getting up and running
----------------------

To get the development environment running, all you need to have is vagrant/virtualbox combo.
Get into the root folder, run a:

    $ vagrant up
    
    
You are all set. The provision script will take care of:


* install python 2.7
* install postgresql
* create required database/user
* install the project requirements declared within requirements.txt
* migrate whatever is needed


It will forward the port 8050.
To run the Django Server, please SSH into the running vagrant box, then move to /vagrant/dapp/ folder and execute the python manage.py script:


    $ vagrant ssh
    $ cd /vagrant/dapp
    $ python manage.py runserver
    
    
The last command will run an embedded Web server listening to address 127.0.0.1:8000 (values can be changed, please refer to Django Documentation).


Project Structure
----------------------


The project consists of four Django applications: 


* api (contains the REST API)
* eth (contains Events' listener/daemon)
* events (contains data models)
* taskapp (contains Celery configuration)


Email templates are stored in /templates/emails directory.

REST API ENDPOINTS
--------

| HTTP VERB | ROUTE | HEADERS | QUERY PARAMS | DESCRIPTION |
|----------------------|----------------|---------------------|---------------------|---------------------|
|POST| /alert/signup/ | none | none | Subscribes a user to the service |
|POST| /alert/ | auth-code: String | none | Creates a new Alert |
|GET| /alert/ | auth-code: String | contract : String | Retrieves an Alert data |
|DELETE| /alert/ | auth-code: String | none | Deletes a user data along with its alerts |
|[DJANO VIEW] GET| /alert/admin/ | none | code: String | View with all alerts related to the query code |
