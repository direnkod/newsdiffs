#!/bin/bash

while true; do
	/usr/local/bin/python2.7 website/manage.py scraper &> /dev/null
	sleep 1h
done


