#!/usr/bin/env python

from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed, EndPointNotFound
import urllib2
import json
from simplejson import JSONDecodeError

# Query SPARQL endpoints to Datahub
datahub_api_call = "http://datahub.io/api/2/search/resource?format=api/sparql&all_fields=1&limit=1000"
datahub_stream = urllib2.urlopen(datahub_api_call)
datahub_json = json.load(datahub_stream)
datahub_results = datahub_json["results"]

# Query endpoints for variables and values
for endpoint in datahub_results:
    print 'ENDPOINT: ' + endpoint["url"]
    sparql = SPARQLWrapper(endpoint["url"])
    sparql.setQuery("""
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
    """)
    sparql.setReturnFormat(JSON)
    try:
        endpoint_results = sparql.query().convert()
    except urllib2.URLError:
        print "The endpoint URL could not be opened"
        pass
    except EndPointNotFound:
        print "Endpoint not found"
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
    except (AttributeError) as e:
        print "The endpoint did not return JSON"
        continue

# Serialize list to JSON
# endpoints_file = open('endpoints.json', 'w')
# json.dump(datahub_json, endpoints_file)
# endpoints_file.close()
