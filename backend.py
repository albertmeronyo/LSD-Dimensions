from bottle import route, run, template, request, static_file
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
def lsd_dimensions():
    dims = db.dimensions.aggregate([
        {"$unwind" : "$dimensions"},
        {"$group": {"_id": {"uri": "$dimensions.uri", "label": "$dimensions.label"}, 
                    "dimensionsCount" : {"$sum" : 1}}},
        {"$sort": SON([("dimensionsCount", -1)])}
    ])
    # Local results json serialization -- dont do this at every request!
    local_json = []
    for result in dims["result"]:
        local_json.append({"uri" : result["_id"]["uri"],
                           "label" : result["_id"]["label"],
                           "refs" : result["dimensionsCount"]
                           })
    with open('data.json', 'w') as outfile:
        json.dump(local_json, outfile)
    return template('lsd-dimensions', results=dims)

@route('/dimension', method = 'POST')
def dimension(__dim = None):
    dim = None
    if __dim:
        dim = __dim
    else:
        dim = request.forms.get("dim")
    print dim
    sparql = SPARQLWrapper("http://lod.cedar-project.nl:8080/sparql/cedar")
    det_dimension = """
    PREFIX sdmx: <http://purl.org/linked-data/sdmx#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT DISTINCT ?code ?codel ?codelist ?concept
    FROM <http://lod.cedar-project.nl/resource/harmonization>
    WHERE {
    <%s> a qb:DimensionProperty ;
    qb:concept ?concept ;
    rdfs:range ?range .
    OPTIONAL {<%s> qb:codeList ?codelist .
    ?codelist skos:hasTopConcept ?code .
    ?code skos:prefLabel ?codel . }
    }
    """ % (dim, dim)
    sparql.setQuery(det_dimension)
    sparql.setReturnFormat(JSON)
    details = sparql.query().convert()
    return template('dimension', dim=dim, details=details)

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
