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


####### EMETTEURS #######
#########################

##### GETS

@app.route('/emetteurs')
def get_emetteurs():
    """recupère la liste des emetteurs"""
    emetteurs = execute_query("select nom from emetteurs")
    # ajout de _links à chaque dico région
    for i in range(len(emetteurs)):
        emetteurs[i]["_links"] = [
            {
                "href": "/emetteurs/" + urllib.parse.quote(emetteurs[i]["nom"]),
                "rel": "self"
            },
            {
                "href": "/emetteurs/" + urllib.parse.quote(emetteurs[i]["nom"]) + "/mailboxes",
                "rel": "mailboxes"
            },
            {
                "href": "/emetteurs/" + urllib.parse.quote(emetteurs[i]["nom"]) + "/mails",
                "rel": "mails"
            }
        ]
    return jsonify(emetteurs), 200

@app.route('/emetteurs/<string:nom>')
def get_emetteur(nom: str):
    """recupère la liste des emetteurs"""
    emetteur = execute_query("select nom from emetteurs where nom=?", (nom,))
    # ajout de _links à l'emetteur
    emetteur[0]["_links"] = [
        {
            "href": "/emetteurs/" + urllib.parse.quote(emetteur[0]["nom"]),
            "rel": "self"
        },
        {
            "href": "/emetteurs/" + urllib.parse.quote(emetteur[0]["nom"]) + "/mailboxes",
            "rel": "mailboxes"
        },
        {
            "href": "/emetteurs/" + urllib.parse.quote(emetteur[0]["nom"]) + "/mails",
            "rel": "mails"
        }
    ]
    return jsonify(emetteur), 200


@app.route('/emetteurs/<string:nom>/mailboxes')
def get_mailboxes_for_emetteur(nom: str):
    """Récupère les mailboxes d'un emetteur"""
    mailboxes = execute_query("""select mailboxes.nom, emetteurs.nom
                                    from mailboxes
                                    join emetteurs on mailboxes.emetteur_id = emetteurs.id
                                    where lower(emetteurs.nom) = ?""", (urllib.parse.unquote(nom.lower()),))
    if mailboxes == []:
        abort(404, "Aucune région dans cet emetteurs")
    # ajout de _links à chaque dico mailbox
    for i in range(len(mailboxes)):
        mailboxes[i]["_links"] = [{
            "href": "/mailboxes/" + mailboxes[i]["nom"],
            "rel": "self"
        }]
    return jsonify(mailboxes), 200


@app.route('/emetteurs/<string:nom>/mails')
def get_mails_for_emetteur(nom: str):
    """Récupère les mails d'un emetteur"""
    mails = execute_query("""select mails.read, mails.title, mails.message, emetteurs.nom
                                    from mails
                                    join emetteurs on mails.emetteur_id = emetteurs.id
                                    where lower(emetteurs.nom) = ?""", (urllib.parse.unquote(nom.lower()),))
    if mails == []:
        abort(404, "Aucune région dans cet emetteurs")
    # ajout de _links à chaque dico mailbox
    for i in range(len(mails)):
        mails[i]["_links"] = [{
            "href": "/mails/" + mails[i]["nom"],
            "rel": "self"
        }]
    return jsonify(mails), 200

##### POSTS

@app.route('/emetteurs', methods=['POST'])
def post_emetteur():
    """"Ajoute un emetteurs"""
    nom = request.args.get("nom")
    execute_query("insert into emetteurs (nom) values (?)", (nom,))
    # on renvoi le lien de l'emetteur que l'on vient de créer
    reponse_json = jsonify({
        "_links": [{
            "href": "/emetteurs/" + urllib.parse.quote(nom),
            "rel": "self"
        }]
    })
    return reponse_json, 201  # created

@app.route('/emetteurs/<string:nom_emetteurs>/mailboxes', methods=['POST'])
def post_mailboxes_for_emetteurs(nom_emetteurs):
    """créé une mailbox"""
    nom_mailbox = request.args.get("nom")
    execute_query("insert into mailboxes (nom, emetteur_id) values (?, (select id from emetteurs where nom = ?))", (nom_mailbox, nom_emetteurs))
    # on renvoi le lien du département  que l'on vient de créer
    reponse_json = jsonify({
        "_links": [{
            "href": "/mailboxes/" + nom_mailbox,
            "rel": "self"
        }, {
            "href": "/emetteurs/" + nom_emetteurs + "/mailboxes/" + nom_mailbox,
            "rel": "self"
        }]
    })
    return reponse_json, 201  # created

##### PUTS

@app.route('/emetteurs/<string:nom>', methods=['PUT'])
def put_emetteur(nom: str):
    """"modifie un emetteurs"""
    new_nom = request.args.get("nom")
    execute_query("update emetteurs set nom=? where nom=?", (new_nom,nom))
    # on renvoi le lien de l'emetteur que l'on vient de créer
    reponse_json = jsonify({
        "_links": [{
            "href": "/emetteurs/" + urllib.parse.quote(new_nom),
            "rel": "self"
        }]
    })
    return reponse_json, 201  # created

##### DELETES

@app.route('/emetteurs/<string:nom>', methods=['DELETE'])
def delete_emetteur(nom: str):
    """"supprime un emetteurs"""
    execute_query("delete from emetteurs where nom=?", (nom,))
    # on renvoi le lien de l'emetteur que l'on vient de créer
    return "", 204  # no data


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
