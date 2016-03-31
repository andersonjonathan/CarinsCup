#!/usr/bin/env bash
python "$OPENSHIFT_REPO_DIR"wsgi/carinscup/manage.py update_results --from=$(date --date='14 days ago' +%Y-%m-%d)