#!/bin/sh
MANAGE=django-admin.py
SCRIPT_REALPATH=`readlink -f $0`
PROJECT_DIR=`dirname $SCRIPT_REALPATH`;
PYTHONPATH=$PROJECT_DIR DJANGO_SETTINGS_MODULE=test_assignment_project.settings \
    $MANAGE project_models 2> `date +"%Y-%m-%d"`.dat
