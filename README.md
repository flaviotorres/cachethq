# cachethq
cachethq ComponentGroup API

Python - RESTFul interface for CachetHQ Component Group

    * /componentgroups: List all component groups.
        URI: /componentgroups
        Method: GET
    * /componentgroup/<group_name>: Create a new group name
        URI: /componentgroup/new_group_name
        Method: PUT
    * /componentgroup/<group_name>: Delete a group name
        URI: /componentgroup/new_group_name
        Method: DELETE
    *  /help: Print this help.
        URI: /help
        Method: GET

# Examples:

Create a new component group
============================
<pre>curl -s -X PUT http://localhost:8090/componentgroups/test | python -m json.tool
{
    "id": 31
}</pre>


List all component groups
============================
<pre>curl -s -X GET http://localhost:8090/componentgroups | python -m json.tool
[
    {
        "id": 23,
        "name": "YOUR_CP"
    },
    {
        "id": 25,
        "name": "new_cp"
    },
    {
        "id": 27,
        "name": "test"
    }
]</pre>


Delete a component group
============================
<pre> curl -s -X DELETE http://localhost:8090/componentgroups/test | python -m json.tool
{
    "groupname": "test",
    "status": "deleted"
}</pre>


# INSTALLING

All you need is:

* pymysql [1]
* Python 2.7 [2]
* Bottle [3]

[1]: https://github.com/PyMySQL/PyMySQL/
[2]: http://www.python.org/download/releases/2.7.3/
[3]: http://bottlepy.org/docs/dev/