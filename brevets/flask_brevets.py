"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import os
import flask
from pymongo import MongoClient
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import db # Database operations
import config

import logging

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

db_client = db.Mongodb(os.environ['MONGODB_HOSTNAME'])
db_client.connect()
db_client.set_db("brevetsdb")

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.route("/insert", methods=["POST"])
def submit():
    data = request.form.to_dict()
    # Converting string representation of list to a list
    data['table'] = eval(data['table'])
    table = data['table']
    # Remove the previous submit result
    db_client.delete_all_rows("latestsubmit")

    for i in range(len(table)):
        row = table[str(i)]
        db_client.insert("latestsubmit", row)
    return flask.jsonify(output=str(data))


@app.route("/display")
def display():
    retrieval = db_client.list_all_rows("latestsubmit")
    app.logger.debug(retrieval)
    brevet = begin_date = ""
    if len(retrieval) > 0:
        brevet = retrieval[0]['brevet']
        begin_date = retrieval[0]['begin']
    return flask.render_template('display.html', result=retrieval, brevet=brevet, begin=begin_date)


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brevet_dist = request.args.get('brevet_dist', 200, type=int)
    begin_date = request.args.get('begin_date', '2021-01-01T00:00', type=str)

    app.logger.debug("km={}".format(km))
    app.logger.debug("brevet_dist={}".format(brevet_dist))
    app.logger.debug("begin_date={}".format(begin_date))
    app.logger.debug("request.args: {}".format(request.args))

    open_time = acp_times.open_time(km, brevet_dist, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, arrow.get(begin_date)).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}

    return flask.jsonify(result=result)


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
