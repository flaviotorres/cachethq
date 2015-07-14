#!/usr/bin/python
# -*- coding: utf-8; -*-
# setup: python-setuptools, pip, pymysql, bottle

import logging
import pymysql.cursors

from datetime import datetime 
from functools import wraps


from bottle import route, run, error, get, post, request, response, abort, put, delete

try:
    from simplejson import dumps
except ImportError:
    from json import dumps



DEBUG               = True
LOG_FORMAT       = "%(asctime)s [%(levelname)s] cachet[%(process)d/%(threadName)s].%(name)s: %(message)s"


logging.basicConfig(filename="cachet.log", format=LOG_FORMAT, level=logging.DEBUG)



def reply_json(f):
    @wraps(f)
    def json_dumps(*args, **kwargs):
        r = f(*args, **kwargs)
        if r and type(r) in (dict, list, tuple, str, unicode):
            response.content_type = "application/json; charset=UTF-8"
            return dumps(r)
        return r
    return json_dumps


@get('/<:re:componentgroup[s]?/?>')
@reply_json
def list_componentGroup():

    # Connect to the database
    connection = pymysql.connect(host='your-hostname',
                             user='your-data',
                             passwd='your-data',
                             db='your-data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "select id, name from component_groups;"
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result)

    finally:
        connection.close()

    return result

@put('/<:re:componentgroup[s]?>/<groupname>')
@reply_json
def put_componentGroup(groupname=None):

    source_date = datetime.now()

    # Connect to the database
    connection = pymysql.connect(host='your-hostname',
                             user='your-data',
                             passwd='your-data',
                             db='your-data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO component_groups (name, created_at) VALUES (%s, %s)"
            cursor.execute(sql, (groupname, source_date))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT id FROM component_groups WHERE name=%s"
            cursor.execute(sql, (groupname,))
            result = cursor.fetchone()

    finally:
        connection.close()

    return result

@delete('/<:re:componentgroup[s]?>/<groupname>')
@reply_json
def delete_componentGroup(groupname=None):

    # Connect to the database
    connection = pymysql.connect(host='your-hostname',
                             user='your-data',
                             passwd='your-data',
                             db='your-data',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "DELETE FROM component_groups WHERE name = %s"
            cursor.execute(sql, (groupname,))

            # connection is not autocommit by default. So you must commit to save
            # your changes.
            connection.commit()

    finally:
        connection.close()

    return {"groupname": groupname,
            "status": "deleted" }

@get("/<:re:(?:index.htm[l]?)?>")
def index():
    return("""<center><h3>RESTFul interface for CachetHQ Component Group.</h3></center>
              <hr size="1"><br>
              <center>Check <a href="/help">/help</a> (human readable) to see all available methods/endpoints.</center>
              """)

@get("/help")
def help(name="help"):
    return ("""
            <!doctype html>
            <html><head>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.1/css/bootstrap.min.css">
            </head>
            <body>
            <div class="starter-template">
            <h4>RESTFul interface for CachetHQ Component Group</h1>
            <p class="lead">
            <ul>
                <li>/componentgroups: List all component groups.</li>
                <ul>
                    <li>URI: /componentgroups</li>
                    <li>Method: GET </li>
                </ul>
                <li>/componentgroup/&lt;group_name&gt;: Create a new group name</li>
                <ul>
                    <li>URI: /componentgroup/new_group_name</li>
                    <li>Method: PUT </li>
                </ul>
                <li>/componentgroup/&lt;group_name&gt;: Delete a group name</li>
                <ul>
                    <li>URI: /componentgroup/new_group_name</li>
                    <li>Method: DELETE </li>
                </ul>
                <li>/help: Print this help.</li>
                <ul>
                    <li>URI: /help</li>
                    <li>Method: GET </li>
                </ul>
                <br>
            </ul>
            </p></body></html>""")

@error(500)
@reply_json
def error500(err):
    return { "http_status_code": err.status_code,
                 "http_status":      err.status,
                 "error_message":    err.body }

@error(400)
@reply_json
def error400(err):
    return { "http_status_code": err.status_code,
             "http_status":      err.status,
             "error_message":    err.body }

run(host='127.0.0.1', port=8080, debug=DEBUG, reloader=True)
