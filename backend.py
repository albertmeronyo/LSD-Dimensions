from bottle import route, run, template, request, static_file
from SPARQLWrapper import SPARQLWrapper, JSON, SPARQLExceptions
import urllib
import logging
import glob
import sys
import traceback
import os

__VERSION = 0.1

@route('/version')
def version():
    return "Version " + str(__VERSION)

@route('/')
def lsd_dimensions():
    sparql = SPARQLWrapper("http://lod.cedar-project.nl:8080/sparql/cedar")
    dimensions = """
    PREFIX sdmx: <http://purl.org/linked-data/sdmx#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT DISTINCT ?dimensionu ?dimension (COUNT(?code) AS ?ncodes)
    FROM <http://lod.cedar-project.nl/resource/harmonization>
    WHERE {
    ?dimensionu a qb:DimensionProperty ;
    qb:concept ?concept ;
    rdfs:label ?dimension ;
    rdfs:range ?range .
    OPTIONAL {?dimensionu qb:codeList ?codelist .
    ?codelist skos:hasTopConcept ?code . }
    } GROUP BY ?dimensionu ?dimension ORDER BY ?dimension
    """
    sparql.setQuery(dimensions)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return template('lsd-dimensions', results=results)

# Static Routes
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


run(host = 'localhost', port = 8080, debug = True)
