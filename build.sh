#!/usr/bin/env bash
# exit on error
set -o errexit

export GOOGLEAPIKEY="AIzaSyBxpDLEWcZIXBS1Gf2Si8JdOLTuvXrLVu8"
export GEMINISTUDIOKEY2 = "AIzaSyCYtXLllulrHSAH_Sb90bsgBdSwEJp9kFE"

poetry install

python manage.py collectstatic --no-input
python manage.py migrate