from bottle import route, run, template, request, static_file, abort
from pymongo import Connection
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
from bson.son import SON
import urllib
import logging
import glob
import sys
import traceback
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from pymongo import Connection
from bson.son import SON
from pylab import *

__VERSION = 0.1

connection = Connection('localhost', 27017)
db = connection.lsddimensionsprod

@route('/version')
def version():
    return "Version " + str(__VERSION)

@route('/')
@route('/dimensions')
def lsd_dimensions():
    dims = db.dimensions.aggregate([
        {"$unwind" : "$dimensions"},
        {"$group": {"_id": {"uri": "$dimensions.uri", "label": "$dimensions.label"}, 
                    "dimensionsCount" : {"$sum" : 1}}},
        {"$sort": SON([("dimensionsCount", -1)])}
    ])
    # Local results json serialization -- dont do this at every request!
    local_json = []
    dimension_id = 0
    for result in dims["result"]:
        local_json.append({"id" : dimension_id,
                           "view" : "<a href='/dimensions/%s'><img src='/img/eye.png' alt='Details'></a>" % dimension_id,
                           "uri" : result["_id"]["uri"],
                           "label" : result["_id"]["label"],
                           "refs" : result["dimensionsCount"]
                           })
        dimension_id += 1
    with open('data.json', 'w') as outfile:
        json.dump(local_json, outfile)
    num_endpoints = db.dimensions.count()
    return template('lsd-dimensions', results=dims, num_endpoints=num_endpoints)

@route('/dimensions/:id', method='GET')
def get_dimension(id):
    # TODO: avoid this lazy load on demand
    local_json = None
    with open('data.json', 'r') as infile:
        local_json = json.load(infile)
    for dim in local_json:
        if int(dim['id']) == int(id):
            dimension_uri = dim['uri']
    # Search for all we got about dimension_uri
    endpoints_results = db.dimensions.find(
        {"dimensions.uri" : dimension_uri},
        {"endpoint.url" : 1}
    ).distinct("endpoint.url")
    print endpoints_results
    codes_results = db.dimensions.aggregate([
        {"$unwind" : "$dimensions"}, 
        {"$unwind" : "$dimensions.codes"}, 
        {"$match" : {"dimensions.uri" : dimension_uri}}, 
        {"$group" : {"_id" : {"uri" : "$dimensions.codes.uri", "label" : "$dimensions.codes.label"}}}
    ])
    return template('dimension', dim=dimension_uri, endpoints=endpoints_results, codes=codes_results)


@route('/about', method='GET')
def about():
    return template('about')

@route('/analytics', method='GET')
def analytics():
    # TODO: avoid this lazy load on demand

    ### 1. Dim-freq distribution
    dims = db.dimensions.aggregate([
        {"$unwind" : "$dimensions"},
        {"$group": {"_id": {"uri": "$dimensions.uri", "label": "$dimensions.label"}, 
                    "dimensionsCount" : {"$sum" : 1}}},
        {"$sort": SON([("dimensionsCount", -1)])}
    ])

    freqs = [dim["dimensionsCount"] for dim in dims["result"]]
    dim_names = [dim["_id"]["uri"] for dim in dims["result"]]

    x = np.array(range(0, len(dim_names)))
    y = np.array(freqs)
    my_xticks = dim_names
    #plt.xticks(x, my_xticks, rotation=90)
    plt.plot(x, y)
    plt.grid(True)
    plt.savefig('views/img/dim-freq.png', bbox_inches='tight')
    plt.close()

    ### 2. Endpoints using LSD dimensions
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])

    num_endpoints = db.dimensions.find({"endpoint" : {"$exists" : "1"}}).count()
    with_dims = db.dimensions.find({"dimensions" : {"$exists" : "1"}}).count()
    frac_with = (float(with_dims) / num_endpoints) * 100
    frac_without = 100 - frac_with

    labels = 'With dimensions', 'Without dimensions'
    fracs = [frac_with, frac_without]
    explode=(0, 0)

    plt.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    plt.savefig('views/img/endpoint-usage.png', bbox_inches='tight')
    plt.close()
    
    return template('analytics')

# Static Routes
@route('/data.json')
def data():
    return static_file('data.json', root='./')

@route('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='views/js')

@route('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='views/css')

@route('/img/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='views/img')

@route('/fonts/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='views/fonts')

run(host = sys.argv[1], port = sys.argv[2], debug = True)
