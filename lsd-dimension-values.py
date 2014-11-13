#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound, EndPointInternalError
import urllib2
import json
from simplejson import JSONDecodeError
import socket
import time
from timeout import timeout, TimeoutError
from xml.parsers.expat import ExpatError
from pymongo import Connection

connection = Connection('localhost', 27017)
db = connection.lsddimensions

db.dimensions.drop()
db.dsds.drop()

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

query_dsd = """
    PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT ?dsd ?componentValue ?p ?o
    WHERE {
    ?dsd a qb:DataStructureDefinition ;
         qb:component ?component .
    ?component ?componentType ?componentValue .
    ?componentValue ?p ?o .
    FILTER (?componentType IN (qb:dimension, qb:measure, qb:attribute)) 
    } ORDER BY ?dsd
"""

# query = """
#     PREFIX sdmx: <http://purl.org/linked-data/sdmx#>
#     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#     PREFIX qb: <http://purl.org/linked-data/cube#>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT DISTINCT ?dimensionu ?dimension ?codeu ?code
#     WHERE {
#     ?dimensionu a qb:DimensionProperty .
#     ?dimensionu rdfs:label|skos:prefLabel ?dimension .
#     OPTIONAL {
#     ?obs a qb:Observation .
#     ?obs ?dimensionu ?codeu .
#     ?codeu rdfs:label|skos:prefLabel ?code .
#     }
#     OPTIONAL {
#     ?dimensionu qb:codeList ?codelist .
#     ?codelist skos:hasTopConcept ?codeu .
#     ?codeu rdfs:label|skos:prefLabel ?code . }
#     }
#     LIMIT 1000
# """

@timeout(70)
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
print num_endpoints
current_endpoint = 1
endpoint_results = None

# Query endpoints for variables and values
# datahub_results = [{"url" : "http://worldbank.270a.info/sparql"}]
for endpoint in datahub_results:
    # Old crap, dimensions and codes
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
        dimensions = {}
        dimensions_codes = {}
        codes = {}

        for result in endpoint_results["results"]["bindings"]:
            dimension_uri = None
            dimension_label = None
            code_uri = None
            code_label = None
            if 'dimensionu' in result and 'value' in result['dimensionu']:
                dimension_uri = result["dimensionu"]["value"]
                # print 'DIMENSION URI: ' + dimension_uri
                if 'dimension' in result and 'value' in result['dimension']:
                    dimension_label = result["dimension"]["value"]
                    # print 'DIMENSION LABEL: ' + dimension_label
            if 'codeu' in result and 'value' in result['codeu']:
                code_uri = result["codeu"]["value"]
                # print 'CODE URI: ' + code_uri
                if 'code' in result and 'value' in result['code']:
                    code_label = result["code"]["value"]
                    # print 'CODE LABEL: ' + code_label
            dimensions[dimension_uri] = dimension_label
            codes[code_uri] = code_label
            if dimension_uri not in dimensions_codes:
                dimensions_codes[dimension_uri] = [code_uri]
            else:
                dimensions_codes[dimension_uri].append(code_uri)
    except AttributeError:
        print "The endpoint did not return JSON"
        pass
    except TypeError:
        print "The endpoint did not return valid JSON"
        pass
    except KeyError:
        print "The endpoint returned an empty response"
        pass
    document_entry = {}
    endpoint_entry = endpoint
    dimensions_entry = []
    for key, value in dimensions_codes.iteritems():
        codes_entry = []
        for code in value:
            if code:
                codes_entry.append({"uri" : code, "label" : codes[code]})
        if codes_entry:
            dimensions_entry.append({"uri" : key, "label" : dimensions[key], "codes" : codes_entry})
        else:
            if key and dimensions[key]:
                dimensions_entry.append({"uri" : key, "label" : dimensions[key]})
    document_entry["endpoint"] = endpoint_entry
    if dimensions_entry:
        document_entry["dimensions"] = dimensions_entry
    db.dimensions.save(document_entry)


    # New crap, DSDs
    print "QUERYING ENDPOINT %s / %s" % (current_endpoint, num_endpoints)
    try:
        endpoint_results = query_endpoint(endpoint["url"], query_dsd)
    except TimeoutError:
        print "Endpoint timeout"
        pass
    except ValueError:
        print "Endpoint and query combination are malformed"
        pass
    try:        
        dsds_components = {}

        for result in endpoint_results["results"]["bindings"]:
            dsd_uri = None
            component_s = None
            component_p = None
            component_o = None
            if 'dsd' in result and 'value' in result['dsd']:
                dsd_uri = result["dsd"]["value"]                
            if 'componentValue' in result and 'value' in result['componentValue']:
                component_s = result["componentValue"]["value"]
            if 'p' in result and 'value' in result['p']:
                component_p = result["p"]["value"]
            if 'o' in result and 'value' in result['o']:
                component_o = result["o"]["value"]
            component = [component_s, component_p, component_o]
            if dsd_uri not in dsds_components:
                dsds_components[dsd_uri] = []
            dsds_components[dsd_uri].append(component)            
    except AttributeError:
        print "The endpoint did not return JSON"
        pass
    except TypeError:
        print "The endpoint did not return valid JSON"
        pass
    except KeyError:
        print "The endpoint returned an empty response"
        pass
    document_entry = {}
    endpoint_uri = endpoint["url"]
    dsd_entry = []
    for key, value in dsds_components.iteritems():
        dsd_uri = key
        components_entry = []
        for component in value:
            if component:
                components_entry.append({"s" : component[0], "p" : component[1], "o" : component[2]})
        if components_entry:
            dsd_entry.append({"uri" : dsd_uri, "components" : components_entry})
        else:
            if key and dsds_components[key]:
                dsd_entry.append({"uri" : dsd_uri})
        document_entry["endpoint"] = endpoint_uri
        if dsd_entry:
            document_entry["dsd"] = dsd_entry
        db.dsds.save(document_entry)
    current_endpoint += 1

if db.dimensions.count() > 500:
    connection.copy_database("lsddimensionsprod", "lsddimensions" + str(int(time.time())))
    connection.drop_database("lsddimensionsprod")
    connection.copy_database("lsddimensions", "lsddimensionsprod")

# Serialize list to JSON
# endpoints_file = open('endpoints.json', 'w')
# json.dump(datahub_json, endpoints_file)
# endpoints_file.close()
