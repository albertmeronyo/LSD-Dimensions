#!/usr/bin/env python

from simplejson import JSONDecodeError
from timeout import timeout, TimeoutError
import logging
import requests
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, SKOS

# lsd modules
import static as static

logging.basicConfig(level=logging.DEBUG, format=static.LOG_FORMAT)
lsdlogger = logging.getLogger(__name__)

lsdlogger.info("Starting LSD Dimensions crawler")

qb = Namespace("http://purl.org/linked-data/cube#")

dim_g = Graph()

@timeout(70)
def query_endpoint(endpoint_url, query):
    response_json = None
    lsdlogger.info("Processing endpoint: {}".format(endpoint_url))
    try:
        response_json = requests.get(endpoint_url, params={'query' : query}, headers={'Accept' : static.mimetypes['json']}).json()
    except JSONDecodeError as e:
        lsdlogger.error(e)
        return
    except requests.exceptions.ConnectionError as e:
        lsdlogger.error(e)
        return
    except TimeoutError as e:
        lsdlogger.error(e)
        return
    except requests.exceptions.MissingSchema as e:
        lsdlogger.error(e)
        return
    if 'results' in response_json:
        for res in response_json['results']['bindings']:
            dim = res["dim"]["value"]
            dim_l = res["dim_l"]["value"]
            lsdlogger.debug("Adding result {}".format(dim))
            dim_g.add( (URIRef(dim), RDF.type, qb.DimensionProperty) )
            dim_g.add( (URIRef(dim), RDFS.label, Literal(dim_l)))
            # TODO: the qb:endpoint is wrong! Find alternative
            dim_g.add( (URIRef(dim), qb.endpoint, URIRef(endpoint_url)) )
            if 'codelist' in res and 'code' in res and 'value' in res['codelist'] and 'value' in res['code']:
                codelist = res["codelist"]["value"]
                code = res["code"]["value"]
                code_l = res["code_l"]["value"]
                lsdlogger.debug("Adding result {}".format(code))
                dim_g.add( (URIRef(dim), qb.codeList, URIRef(codelist)) )
                dim_g.add( (URIRef(code), SKOS.inScheme, URIRef(codelist)) )
                dim_g.add( (URIRef(code), SKOS.prefLabel, Literal(code_l)) )

    return

# Query SPARQL endpoints to Datahub
datahub_json = requests.get("http://datahub.io/api/2/search/resource?format=api/sparql&all_fields=1&limit=1000").json()
datahub_results = datahub_json["results"]

num_endpoints = len(datahub_results)
lsdlogger.info("Got {} endpoints from DataHub".format(num_endpoints))
current_endpoint = 1

dimensions = []

for endpoint in datahub_results:
    lsdlogger.info("Now querying endpoint {} / {}".format(current_endpoint, num_endpoints))
    query_endpoint(endpoint["url"], static.DIMENSIONS_REMOTE_QUERY)

    for dim in dim_g.subjects(RDF.type, qb.DimensionProperty):
        if dim not in dimensions:
            dimensions.append(dim)

    lsdlogger.info("Got {} dimensions so far!".format(len(dimensions)))

    current_endpoint += 1

dim_g.bind("qb", qb)

outfile = open("dimensions.ttl", "w")
outfile.write(dim_g.serialize(format='turtle'))
outfile.close()
