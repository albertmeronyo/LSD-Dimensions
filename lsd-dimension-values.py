#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound, EndPointInternalError
import urllib2
import json
from simplejson import JSONDecodeError
import socket
from timeout import timeout, TimeoutError

query = """
    PREFIX sdmx: <http://purl.org/linked-data/sdmx#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?dimensionu ?dimension ?codeu ?code
    WHERE {
    ?dimensionu a qb:DimensionProperty ;
    rdfs:label ?dimension .
    OPTIONAL {?dimensionu qb:codeList ?codelist .
    ?codelist skos:hasTopConcept ?codeu .
    ?codeu skos:prefLabel ?code . }
    } GROUP BY ?dimensionu ?dimension ?codeu ?code ORDER BY ?dimension
"""

@timeout(60)
def query_endpoint(endpoint_url, query):
    endpoint_results = None
    print 'ENDPOINT: ' + endpoint_url
    wrapper = SPARQLWrapper(endpoint_url)
    wrapper.setQuery(query)
    wrapper.setReturnFormat(JSON)
    try:
        endpoint_results = wrapper.query().convert()
    except urllib2.URLError:
        print "The endpoint URL could not be opened"
        pass
    except EndPointNotFound:
        print "Endpoint not found"
        pass
    except EndPointInternalError:
        print "There was an internal error at the endpoint"
        pass
    except QueryBadFormed:
        print "The endpoint does not like the query"
        pass
    except JSONDecodeError:
        print "Could not decode returned JSON"
        pass
    except socket.error:
        print "Connection reset by peer"
        pass        
    return endpoint_results

# Query SPARQL endpoints to Datahub
datahub_api_call = "http://datahub.io/api/2/search/resource?format=api/sparql&all_fields=1&limit=1000"
datahub_stream = urllib2.urlopen(datahub_api_call)
datahub_json = json.load(datahub_stream)
datahub_results = datahub_json["results"]

# Query endpoints for variables and values
for endpoint in datahub_results:
    try:
        endpoint_results = query_endpoint(endpoint["url"], query)
    except TimeoutError:
        print "Endpoint timeout"
        pass
    try:
        for result in endpoint_results["results"]["bindings"]:
            if 'dimensionu' in result:
                print 'DIMENSION URI: ' + result["dimensionu"]["value"]
            if 'dimension' in result:
                print 'DIMENSION LABEL: ' + result["dimension"]["value"]
            if 'codeu' in result:
                print 'CODE URI: ' + result["codeu"]["value"]
            if 'code' in result:
                print 'CODE LABEL: ' + result["code"]["value"]
    except AttributeError:
        print "The endpoint did not return JSON"
        pass
    except TypeError:
        print "The endpoint did not return valid JSON"
        pass
        

# Serialize list to JSON
# endpoints_file = open('endpoints.json', 'w')
# json.dump(datahub_json, endpoints_file)
# endpoints_file.close()
