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

__VERSION = 0.1

connection = Connection('localhost', 27017)
db = connection.lsddimensions

@route('/version')
def version():
    return "Version " + str(__VERSION)

@route('/')
@route('/dimensions')
@route('/dimensions/')
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
    return template('lsd-dimensions', results=dims)

@route('/dimensions/:id', method='GET')
def get_dimension(id):
    # Avoid this lazy load on demand!
    local_json = None
    with open('data.json', 'r') as infile:
        local_json = json.load(infile)
    for dim in local_json:
        if int(dim['id']) == int(id):
            dimension_uri = dim['uri']
    # Search for all we got about dimension_uri
    results = db.dimensions.aggregate([
        {"$unwind" : "$dimensions"},
        {"$unwind" : "$codes"},
        {"$group" : {"_id" : {"endpoint-uri" : "$endpoint.url"}}}
        ])
    for result in results["result"]:
        print result    
    abort(404, 'No document with id %s' % id)

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
