#!/bin/bash
python3 -mvenv env
source env/bin/activate
pip install Django > /dev/null 2>&1
python3 -c "from django.core.management.utils import get_random_secret_key; print(f'{get_random_secret_key()}\n')"
deactivate
rm -rf env