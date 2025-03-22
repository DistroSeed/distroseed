#!/bin/bash
# Dump the current environment to a file
printenv > /etc/environment

set -e

# Activate the virtualenv
source /app/env/bin/activate

# Start cron in the background
cron

# Set Transmission Daemon configuration (optional)
CONFIG_DIR="/etc/transmission-daemon"
mkdir -p $CONFIG_DIR
touch $CONFIG_DIR/settings.json

# Start Transmission Daemon in the background
echo "Starting Transmission Daemon..."
transmission-daemon --log-level=debug --config-dir $CONFIG_DIR --foreground &

# Wait for Transmission to be ready
sleep 5

# migrating 
echo "Django migrating..."
cd /app/distroseed && /app/env/bin/python /app/distroseed/manage.py makemigrations
cd /app/distroseed && /app/env/bin/python /app/distroseed/manage.py migrate
cd /app/distroseed && /app/env/bin/python /app/distroseed/manage.py collectstatic --noinput

# Create default superuser if not exists
echo "from django.contrib.auth import get_user_model; User = get_user_model(); x = not User.objects.filter(username='root').exists(); User.objects.create_superuser('root','root@distroseed.com','distroseed') if x else None" | python manage.py shell

# Add Excludes defaults
echo "Importing Excludes..."
cd /app/distroseed && /app/env/bin/python manage.py shell -c "import json; from dashboard.models import Excludes; [Excludes.objects.get_or_create(phrase=item['phrase']) for item in json.load(open('/app/default_data_jsons/excludes.json'))]"

# Add Includes defaults
echo "Importing Includes..."
cd /app/distroseed && /app/env/bin/python manage.py shell -c "import json; from dashboard.models import Includes; [Includes.objects.get_or_create(phrase=item['phrase']) for item in json.load(open('/app/default_data_jsons/includes.json'))]"

# Add AutoTorrent
echo "Importing Default Torrents..."
cd /app/distroseed && /app/env/bin/python manage.py shell -c "import json; from dashboard.models import AutoTorrent; [AutoTorrent.objects.get_or_create(name=item['name'],url=item['url']) for item in json.load(open('/app/default_data_jsons/auto_torrent.json'))]"

# Add TransmissionSetting
echo "Importing Transmission Settings..."
cd /app/distroseed && /app/env/bin/python manage.py shell -c "import json; from dashboard.models import TransmissionSetting; [TransmissionSetting.objects.get_or_create(**item) for item in json.load(open('/app/default_data_jsons/transmission_settings.json'))]"

# TODO: adding in code to overright the default transmission settings.json with database settings

# Start Django app using Gunicorn
echo "Starting Django application..."
cd /app/distroseed && /app/env/bin/gunicorn distroseed.wsgi:application --bind 0.0.0.0:8000 --workers 3
# bash