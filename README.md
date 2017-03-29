# eth-alerts
API for subscribing an email account for contract events

Settings
--------

For configuration purposes, the following table maps the 'alerts' environment variables to their Django setting:

| Environment Variable | Django Setting | Development Default | Production Default| Description |
|----------------------|----------------|---------------------|-------------------|-------------|
|DJANGO_SETTINGS_MODULE| none | alerts.settings.local|alerts.settings.production||
|EMAIL_HOST | EMAIL_HOST | none | smtp.gmail.com||
|EMAIL_HOST_PASSWORD | EMAIL_HOST_PASSWORD | none | **** |For Gmail accounts or 2FA accounts remember to generate an app specific password|
|EMAIL_HOST_USER | EMAIL_HOST_USER | none | noreply@gnosis.pm||
|EMAIL_PORT | EMAIL_PORT | 2525 | 587||
|EMAIL_SUBJECT_PREFIX | EMAIL_SUBJECT_PREFIX | none | '[gnosis alerts]' ||
|EMAIL_USE_TLS| none | none | True ||
|DEFAULT_FROM_EMAIL| DEFAULT_FROM_EMAIL | none |'gnosispm <noreply@gnosis.pm>' ||
|EMAIL_BACKEND | none | 'django.core.mail.backends.filebased.EmailBackend'| 'email_log.backends.EmailBackend'||
|EMAIL_LOG_BACKEND | none | 'django.core.mail.backends.smtp.EmailBackend'| 'django.core.mail.backends.smtp.EmailBackend'||
|EMAIL_FILE_PATH | none | '/tmp/app-messages' | none |Directory containing the emails sent when EMAIL_BACKEND is a file|
|ETHEREUM_NODE_HOST | ETHEREUM_NODE_HOST | localhost | localhost ||
|ETHEREUM_NODE_PORT |ETHEREUM_NODE_PORT | 8545 | 8545||
|ETHEREUM_NODE_SSL| ETHEREUM_NODE_SSL| False | False ||
|ETHERSCAN_URL| ETHERSCAN_URL| 'https://testnet.etherscan.io' | 'https://etherscan.io/' ||
|SERVER_HOST| SERVER_HOST | http://localhost:8080 | alerts.gnosis.pm |Used in eth/mail_batch.py|

Getting up and running
----------------------

To get the development environment running, all you need is the vagrant/virtualbox combo.
Get into the root folder, run :

    $ cd PATH/TO/PROJECT/ROOT
    $ vagrant up
    
    
You are all set. The provision script will take care of:


* install python 2.7
* install postgresql
* create required database/user
* install the project requirements declared within requirements.txt
* migrate whatever is needed


It will forward the port 8050.
To run the Django Server, please SSH into the running vagrant box, then move to /vagrant/alerts/ folder and execute the python manage.py script:


    $ vagrant ssh
    $ cd /vagrant/alerts
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
|DELETE| /alert/ | auth-code: String | none | Deletes the DApp data along with its alerts |
|[DJANGO VIEW] GET| /alert/admin/ | none | code: String | View with all alerts related to the query code |

RUNNING CELERY
--------
In order to execute the Celery worker and scheduler, which take care of sending email notifications to users, we have to ssh into two separate terminals and type the following:
    
    $ cd /vagrant/
    $ celery -A taskapp.celery beat -S djcelery.schedulers.DatabaseScheduler --loglevel debug --workdir="$PWD/alerts"
    
    $ cd /vagrant/
    $ celery -A taskapp.celery worker --loglevel debug --workdir="$PWD/alerts" -c 1
    
Now declare the 'periodic tasks' executed by Celery. To achieve this please create a Django superuser and access the Admin web page. Once there, click on DJCELERY and then on Periodic tasks.

Create a new object and provide the following values:

* Name: Gnosis Alerts
* Task: eth.tasks.run_bot
* Enabled: checked
* Interval: 10 seconds

You are done, Celery will query the Django Database and execute the task.
