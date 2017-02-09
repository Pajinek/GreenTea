#!/usr/bin/bash
# Author: Pavel Studeni <pstudeni@redhat.com>

# How often run script for pickup tasks in seconds
schedule_t=30 # 30s.
check_t=600 # 10min.

# For asynchronous operation Green Tea needs to run cron
# */1 * * * * 	greentea 	python /data/Greantea/manage.py pickup --traceback
function schedule {
    echo "service schedule run ..."
    while true; do
        python manage.py pickup
        sleep $schedule_t
    done
}


# Following command check status of beaker jobs (automation tests)
# */20 * * * * 	greentea 	python /data/Greantea/manage.py check --quiet --traceback
function check {
    echo "service check run ..."
    while true; do
        python manage.py check_beaker
        sleep $check_t
    done
}


HOME=/data/greentea
source $HOME/env/bin/activate && cd $HOME

# Set local settings for running instance
# Beaker's variables
echo "BEAKER_SERVER=\"$BEAKER_SERVER\"" >> $HOME/tttt/settings/local.py
echo "BEAKER_OWNER=\"$BEAKER_USER\"" >> $HOME/tttt/settings/local.py
echo "BEAKER_PASS=\"$BEAKER_PASS\"" >> $HOME/tttt/settings/local.py

# Run all services of Green Tea
schedule & # Schedule jobs
check & # Check all running jobs

# Run main web service
uwsgi --http :8000 --wsgi-file tttt/wsgi.py

