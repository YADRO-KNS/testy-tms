# Sentry deploy
* Fill in sentry.conf.py in current directory
* Run install_sentry.sh
* install_sentry.sh requires user input to create super user
* Run docker-compose up -d in directory sentry/self-hosted-22.12.0
* In sentry ui change Organization slug to yadro and display name
* Don't forget to add sentry settings to your django project they can be found in sentry_settings_for_django.py
