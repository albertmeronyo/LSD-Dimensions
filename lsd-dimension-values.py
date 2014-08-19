#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper, JSON
import csv

with open('endpoints.csv', 'rb') as csvfile:
    endpoints_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in endpoints_reader:
        print ', '.join(row)
