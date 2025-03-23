# Use an official base image with Python and dependencies
FROM ubuntu:24.04

# Set non-interactive frontend for apt
ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update && apt-get install -y gcc cron tzdata python3 \
    python3-venv python3-dev python3-pip  \
    transmission-daemon \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN python3 -mvenv /app/env
RUN /app/env/bin/pip install --upgrade pip wheel setuptools && \ 
/app/env/bin/pip install -r requirements.txt

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy application files
RUN mkdir -p /data/torrents/downloads
RUN mkdir -p /data/torrents/incomplete
RUN mkdir -p /data/torrents/torrents
RUN chmod -R 777 /data/
COPY conf/settings.json /etc/transmission-daemon/settings.json

RUN mkdir /app/default_data_jsons
COPY default_data_jsons/ /app/default_data_jsons/
RUN mkdir /app/distroseed
COPY distroseed/ /app/distroseed/
COPY entrypoint.sh /app/
RUN mkdir /app/scripts
COPY scripts/ /app/scripts/

# Set timezone to EST
RUN ln -fs /usr/share/zoneinfo/America/New_York /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Add cron job
RUN echo "*/5 * * * * root /app/scripts/update_torrents.sh > /var/log/cron.log 2>&1" > /etc/cron.d/updatetorrents

# Set permissions and apply cron job
RUN chmod 0644 /etc/cron.d/updatetorrents && crontab /etc/cron.d/updatetorrents

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh
RUN chmod +x /app/scripts/update_torrents.py
RUN chmod +x /app/scripts/update_torrents.sh

# Collect static files (ensure your settings are configured for production)
RUN cd /app/distroseed && /app/env/bin/python /app/distroseed/manage.py collectstatic --noinput

# Expose ports for Transmission and Django
EXPOSE 8000 9091 51413 51413/udp

# Use the entrypoint script as the container's startup command
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]
