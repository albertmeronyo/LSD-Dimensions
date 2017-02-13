from flask import Flask, render_template
import requests
import logging
import sys
import json
import distance
import itertools
import csv
from rdflib import Graph

# lsd modules
import static

app = Flask(__name__)

# Set logging format
logging.basicConfig(level=logging.DEBUG, format=static.LOG_FORMAT)
app.debug_log_format = static.LOG_FORMAT
lodlogger = logging.getLogger(__name__)

@app.route("/")
@app.route("/dimensions")
def lsd_dimensions():
    lodlogger.debug("Querying store on all dimensions")
    params = {'query' : static.DIMENSIONS_LOCAL_QUERY}
    headers = {'Accept' : static.mimetypes['json']}
    dims = requests.get(static.ENDPOINT, params=params, headers=headers).json()
    lodlogger.debug("Querying store on all endpoints")
    params = {'query' : static.NUM_ENDPOINTS_LOCAL_QUERY}
    headers = {'Accept' : static.mimetypes['json']}
    num_endpoints = requests.get(static.ENDPOINT, params=params, headers=headers).json()

    return render_template('lsd-dimensions.html', results=dims, num_dims=len(dims["results"]["bindings"]), num_endpoints=int(num_endpoints["results"]["bindings"][0]["num_endpoints"]["value"]))

@app.route("/dimensions/<id>", methods=["GET"])
def get_dimension(id):
    # TODO: avoid this lazy load on demand
    local_json = None
    with open('data.json', 'r') as infile:
        local_json = json.load(infile)
    for dim in local_json:
        if int(dim['id']) == int(id):
            dimension_uri = dim['uri']
    # Search for all we got about dimension_uri
    endpoints_results = db.dimensions.find(
        {"dimensions.uri" : dimension_uri},
        {"endpoint.url" : 1}
    ).distinct("endpoint.url")
    codes_results = db.dimensions.aggregate([
        {"$unwind" : "$dimensions"},
        {"$unwind" : "$dimensions.codes"},
        {"$match" : {"dimensions.uri" : dimension_uri}},
        {"$group" : {"_id" : {"uri" : "$dimensions.codes.uri", "label" : "$dimensions.codes.label"}}}
    ])

    return render_template('dimension.html', dim=dimension_uri, endpoints=endpoints_results, codes=codes_results)

@app.route("/about", methods=["GET"])
def about():
    return render_template('about.html')

@app.route("/dsds", methods=["GET"])
def dsds():
    num_endpoints = db.dimensions.count()
    dsds = db.dsds.find(
        {},
        {"_id" : 1, "dsd.uri" : 1}
        )
    num_dsds = db.dsds.count()

    return render_template('dsds.html', num_endpoints=num_endpoints, results=dsds, num_dsds=num_dsds)

@app.route('/dsds/<id>', methods=["GET"])
def get_dsd(id):
    # Search for all we got about dsd_uri
    dsd_results = db.dsds.find_one(
        {"_id" : ObjectId(id)}
        )

    return render_template('dsd.html', dsd_results=dsd_results)

@app.route('/dsds/sim-load', methods=["GET"])
def dsd_sim_load():
    # Get all dsds
    dsds = db.dsds.find({})
    with open('dsd_data.json', 'w') as outfile:
        with open('dsd_data.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                   quotechar='\"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(["dsd_a", "dsd_b", "distance"])
            outfile.write("[")
            for pair in itertools.combinations(dsds, 2):
                a_components = [comp["o"] for comp in pair[0]["dsd"]["components"]]
                b_components = [comp["o"] for comp in pair[1]["dsd"]["components"]]
                a_uri = pair[0]["dsd"]["uri"]
                b_uri = pair[1]["dsd"]["uri"]
                a_id = pair[0]["_id"]
                b_id = pair[1]["_id"]
                dist = distance.jaccard(a_components, b_components)
                item = {"uri_a" : "<a href='/dsds/%s'>%s</a>" % (a_id, a_uri),
                        "uri_b" : "<a href='/dsds/%s'>%s</a>" % (b_id, b_uri),
                        "dist" : dist}
                outfile.write(json.dumps(item, outfile)+",")
                csvwriter.writerow([a_uri, b_uri, dist])
            outfile.write("]")

    return "OK"

@app.route('/dsds/sim', methods=["GET"])
def dsd_sim():
    # load json
    return render_template('dsd-sim.html')

@app.route('/analytics', methods=["GET"])
def analytics():
    # TODO: avoid this lazy load on demand

    ### 1. Dim-freq distribution
    # dims = db.dimensions.aggregate([
    #     {"$unwind" : "$dimensions"},
    #     {"$group": {"_id": {"uri": "$dimensions.uri", "label": "$dimensions.label"},
    #                 "dimensionsCount" : {"$sum" : 1}}},
    #     {"$sort": SON([("dimensionsCount", -1)])}
    # ])
    #
    # freqs = [dim["dimensionsCount"] for dim in dims["result"]]
    # dim_names = [dim["_id"]["label"] for dim in dims["result"]]
    #
    # dims_freqs = [[dim_names[i], freqs[i]] for i in range(len(dim_names))]
    #
    # ### 2. Endpoints using LSD dimensions
    #
    # num_endpoints = db.dimensions.find({"endpoint" : {"$exists" : "1"}}).count()
    # with_dims = db.dimensions.find({"dimensions" : {"$exists" : "1"}}).count()
    # fracs = [['With dimensions', with_dims], ['Without dimensions', num_endpoints - with_dims]]
    #
    # ### 3. Dimensions with and without codes
    # total_dims = len(dims["result"])
    # codes = db.dimensions.aggregate([
    #     {"$match" : {"dimensions.codes.uri" : {"$exists" : 1}}},
    #     {"$unwind" : "$dimensions"},
    #     {"$unwind" : "$dimensions.codes"},
    #     {"$group": {"_id" : {"duri" : "$dimensions.uri"}}}
    # ])
    # with_codes = len(codes["result"])
    # fracs_codes = [['With codes', with_codes], ['Without codes', total_dims - with_codes]]

    # return render_template('analytics.html', dims=range(len(dim_names)), freqs=freqs, dims_freqs=dims_freqs, fracs=fracs, fracs_codes=fracs_codes)
    return render_template('analytics.html')

if __name__ == '__main__':
    app.run(host=static.DEFAULT_HOST, port=static.DEFAULT_PORT, debug=True)
