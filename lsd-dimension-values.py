#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound, EndPointInternalError
import urllib2
import json
from simplejson import JSONDecodeError
import socket
from timeout import timeout, TimeoutError
from xml.parsers.expat import ExpatError
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.lsddimensions

db['endpoints'].remove()
db['dimensions'].remove()
db['codes'].remove()

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
    except ExpatError:
        print "The endpoint returned XML instead of JSON"
        pass
    return endpoint_results

# Query SPARQL endpoints to Datahub
datahub_api_call = "http://datahub.io/api/2/search/resource?format=api/sparql&all_fields=1&limit=1000"
datahub_stream = urllib2.urlopen(datahub_api_call)
datahub_json = json.load(datahub_stream)
datahub_results = datahub_json["results"]

num_endpoints = len(datahub_results)
current_endpoint = 1

# Query endpoints for variables and values
for endpoint in datahub_results:
    endpoint_id = None
    dimension_id = None
    code_id = None
    print "QUERYING ENDPOINT %s / %s" % (current_endpoint, num_endpoints)
    try:
        endpoint_results = query_endpoint(endpoint["url"], query)
    except TimeoutError:
        print "Endpoint timeout"
        pass
    except ValueError:
        print "Endpoint and query combination are malformed"
        pass
    try:
        endpoint_id = db['endpoints'].save(endpoint)
    except ValidationError as ve:
        abort(400, str(ve))
    try:
        for result in endpoint_results["results"]["bindings"]:
            if 'dimensionu' in result and 'value' in result['dimensionu']:
                dimension_uri = result["dimensionu"]["value"]
                print 'DIMENSION URI: ' + dimension_uri
                if 'dimension' in result and 'value' in result['dimension']:
                    dimension_label = result["dimension"]["value"]
                    print 'DIMENSION LABEL: ' + dimension_label
                    #if db['dimensions'].find({"uri" : dimension_uri, "endpoint_id" : endpoint_id}).limit(1).size() == 0:
                    dimension_id = db['dimensions'].save({"uri" : dimension_uri, "label" : dimension_label, "endpoint_id" : endpoint_id})
                
                if 'codeu' in result and 'value' in result['codeu']:
                    code_uri = result["codeu"]["value"]
                    print 'CODE URI: ' + code_uri
                    if 'code' in result and 'value' in result['code']:
                        code_label = result["code"]["value"]
                        print 'CODE LABEL: ' + code_label
                        #if db['codes'].find({"uri" : code_uri, "dimension_id" : dimension_id}).limit(1).size() == 0:
                        code_id = db['codes'].save({"uri" : code_uri, "label" : code_label, "dimension_id" : dimension_id})
    except AttributeError:
        print "The endpoint did not return JSON"
        pass
    except TypeError:
        print "The endpoint did not return valid JSON"
        pass
    except KeyError:
        print "The endpoint returned an empty response"
        pass
    current_endpoint += 1
        

# Serialize list to JSON
# endpoints_file = open('endpoints.json', 'w')
# json.dump(datahub_json, endpoints_file)
# endpoints_file.close()
