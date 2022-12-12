from flask import Flask, jsonify, abort, request
import mariadb
import urllib.parse

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False  # pour utiliser l'UTF-8 plutot que l'unicode


def execute_query(query, data=()):
    config = {
        'host': 'mariadb',
        'port': 3306,
        'user': 'root',
        'password': 'root',
        'database': 'mydatabase'
    }
    """Execute une requete SQL avec les param associés"""
    # connection for MariaDB
    conn = mariadb.connect(**config)
    # create a connection cursor
    cur = conn.cursor()
    # execute a SQL statement
    cur.execute(query, data)

    if cur.description:
        # serialize results into JSON
        row_headers = [x[0] for x in cur.description]
        rv = cur.fetchall()
        list_result = []
        for result in rv:
            list_result.append(dict(zip(row_headers, result)))
        return list_result
    else:
        conn.commit()
        return cur.lastrowid

@app.route('/emetteurs')
def get_emetteurs():
    """recupère la liste des emetteurs"""
    emetteurs = execute_query("select nom from emetteurs")
    # ajout de _links à chaque dico région
    for i in range(len(emetteurs)):
        emetteurs[i]["_links"] = [
            {
                "href": "/emetteurs/" + urllib.parse.quote(pays[i]["nom"]),
                "rel": "self"
            },
            {
                "href": "/emetteurs/" + urllib.parse.quote(pays[i]["nom"]) + "/mailboxes",
                "rel": "mailboxes"
            },
            {
                "href": "/emetteurs/" + urllib.parse.quote(pays[i]["nom"]) + "/mails",
                "rel": "mails"
            }
        ]
    return jsonify(emetteurs), 200

# we define the route /
@app.route('/')
def welcome():
    liens = [{}]
    liens[0]["_links"] = [{
        "href": "/emetteurs",
        "rel": "emetteurs"
    }]
    return jsonify(liens), 200


if __name__ == '__main__':
    # define the localhost ip and the port that is going to be used
    app.run(host='0.0.0.0', port=5000)
