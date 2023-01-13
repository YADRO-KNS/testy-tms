#!/bin/bash
if [ -f "22.12.0.tar.gz" ]; then
    echo "Archive already exists."
else
    wget https://github.com/getsentry/self-hosted/archive/refs/tags/22.12.0.tar.gz
fi
tar -xzf 22.12.0.tar.gz
cd self-hosted-22.12.0/ || exit
cp sentry/enhance-image.example.sh sentry/enhance-image.sh
printf "\napt-get update && \\
        apt-get install -y --no-install-recommends gcc libsasl2-dev libldap2-dev libssl-dev  && \\
        rm -r /var/lib/apt/lists/*\n
pip install sentry-ldap-auth" >> sentry/enhance-image.sh
docker build -t sentry-self-hosted-jq-local --platform=linux/amd64 ./jq
cp /opt/sentry/sentry.conf.py sentry/sentry.conf.py
./install.sh