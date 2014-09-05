LSD Dimensions
==============

All dimensions of Linked Statistical Data, codes and concept schemes
associated to them, and endpoints using them.

## What is this?

LSD Dimensions is an aggregator of all `qb:DimensionProperty` (and
their associated triples) that can be currently found in the Linked
Data Cloud (read: the SPARQL endpoints in Datahub.io). Its purpose is
to improve the reusability of statistical dimensions, codes and
concept schemes in the Web of Data, providing an interface for users
(future work: to programs) to search for resources commonly used to
describe open statistical datasets.

## How does it work?

1. Querying the Datahub.io API for a list of endpoints
2. Querying these endpoints for dimensions, codes and concept schemes
3. Storing all in a messy MongoDB instance
4. Displaying it using Boostrap Table

## Dependencies

- Python 2.7.5
- SPARQL Wrapper
- pymongo
- Bottle
- Bootstrap
- Bootstrap Table
