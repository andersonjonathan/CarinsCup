#!/usr/bin/env bash
/usr/bin/python3 /srv/wsgi/carinscup/manage.py update_results --from=$(date --date='14 days ago' +%Y-%m-%d)