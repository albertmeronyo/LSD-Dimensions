# Default host and port

DEFAULT_HOST = None
DEFAULT_PORT = 8088

# Endpoint location where the lsd database lives
ENDPOINT = "http://virtuoso.amp.ops.labs.vu.nl/sparql"

# Logging format (prettier than the ugly standard in Flask)
LOG_FORMAT = '%(asctime)-15s [%(levelname)s] (%(module)s.%(funcName)s) %(message)s'

# MIME types for content negotiation
mimetypes = {
    'csv' : 'text/csv; q=1.0, */*; q=0.1',
    'json' : 'application/json; q=1.0, application/sparql-results+json; q=0.8, */*; q=0.1',
    'html' : 'text/html; q=1.0, */*; q=0.1',
    'ttl' : 'text/turtle'
}


# Application queries
construct = """
    PREFIX sdmx: <http://purl.org/linked-data/sdmx#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    CONSTRUCT {
        ?dim a qb:DimensionProperty ;
            skos:prefLabel ?dim_l .
        ?mea a qb:MeasureProperty ;
            skos:prefLabel ?mea_l .
        ?cod a qb:CodedProperty ;
            skos:preflabel ?cod_l .
    } WHERE {
        ?dim a qb:DimensionProperty .
        ?dim rdfs:label|skos:prefLabel ?dim_l .
        OPTIONAL {
            ?mea a qb:MeasureProperty .
            ?mea rdfs:label|skos:prefLabel ?mea_l .
        }
        OPTIONAL {
            ?cod a qb:CodedProperty .
            ?cod rdfs:label|skos:prefLabel ?cod_l .
        }
    }
"""

DIMENSIONS_REMOTE_QUERY = """
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX qb: <http://purl.org/linked-data/cube#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT DISTINCT ?dim ?dim_l ?codelist ?code ?code_l
    WHERE {
        ?dim a qb:DimensionProperty ;
            rdfs:label ?dim_l .
            OPTIONAL {
                ?dim qb:codeList ?codelist .
                ?code skos:inScheme ?codelist .
                ?code skos:prefLabel ?code_l .
            }
    }
"""


# query = """
#     PREFIX sdmx: <http://purl.org/linked-data/sdmx#>
#     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#     PREFIX qb: <http://purl.org/linked-data/cube#>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     SELECT DISTINCT ?dimensionu ?dimension ?codeu ?code
#     WHERE {
#         ?dimensionu a qb:DimensionProperty ;
#             rdfs:label ?dimension .
#         OPTIONAL {
#             ?dimensionu qb:codeList ?codelist .
#             ?codelist skos:hasTopConcept ?codeu .
#             ?codeu skos:prefLabel ?code .
#         }
#     } GROUP BY ?dimensionu ?dimension ?codeu ?code ORDER BY ?dimension
# """

query_dsd = """
    PREFIX qb: <http://purl.org/linked-data/cube#>
    SELECT ?dsd ?component ?p ?o
    WHERE {
    ?dsd a qb:DataStructureDefinition ;
      qb:component ?component .
    ?component ?p ?o .
    } ORDER BY ?dsd
"""

query_obscount_a = """
prefix qb: <http://purl.org/linked-data/cube#>
select ?dsd (count(distinct(?obs)) as ?count) where {
  ?obs qb:dataSet ?ds .
  ?ds qb:structure ?dsd .
  ?obs a qb:Observation .
} group by ?dsd
"""

query_obscount_b = """
prefix qb: <http://purl.org/linked-data/cube#>
select ?dsd (count(distinct?obs) as ?count) where {
  ?ds a qb:DataSet .
  ?ds qb:structure ?dsd .
  ?ds qb:slice ?slice .
  ?slice qb:observation ?obs .
} group by ?dsd
"""

DIMENSIONS_LOCAL_QUERY = """
PREFIX qb: <http://purl.org/linked-data/cube#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?dim ?dim_l FROM <http://lsd-dimensions.org> WHERE {
    ?dim a qb:DimensionProperty ;
         rdfs:label ?dim_l .
}
"""

NUM_ENDPOINTS_LOCAL_QUERY = """
PREFIX qb: <http://purl.org/linked-data/cube#>
SELECT (COUNT(DISTINCT ?endpoint) AS ?num_endpoints) FROM <http://lsd-dimensions.org> WHERE {
    ?dimension qb:endpoint ?endpoint .
}
"""
