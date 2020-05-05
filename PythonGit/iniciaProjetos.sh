#!/bin/bash

cd /home/fabricio/PythonProjetos/
source env/bin/activate 
django-admin startproject $1 
cd /home/fabricio/PythonProjetos/$1/
python3 manage.py runserver &



