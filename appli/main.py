from flask import Flask, redirect, render_template, request, url_for
import json
import config
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

from .fonctions import connection, recup_db, add_db, del_db, mod_db
from .fonctions import db_recup, db_del
from . import models
from .models import Cave, Congel, Users

db_select = {'Cave': Cave, 'Congel': Congel, 'Users': Users}

@app.template_filter()
def focus_page(val):
    """ permet d'activer le focus en renvoyant 'active'
        en params: une liste de 2 valeurs qui seront comparée, l'égalité des valeurs revoie 'active'"""
    if val[0] == val[1]:
        return 'active'

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('main.html')

@app.route('/inventaire/', methods=['POST', 'GET'])
def inventaire():
    db = request.args.get('database')
    liste_db = recup_db(db)
    modif_db = ''
    if request.method =='POST':
        if request.form.get('ajout') == 'ajouter':
            new_rec = [db,
                       request.form.get('article'),
                       request.form.get('nb'),
                       request.form.get('périmé'),
                       request.form.get('mail'),
                       ]
            add_db(new_rec)
            return redirect(url_for('inventaire', database=db))
        if request.form.get('supp') is not None:
            if request.form.get('supp')[:3] == 'del':
                del_db(db, request.form.get('supp')[4:])
                return redirect(url_for('inventaire', database=db))
        if request.form.get('modif') is not None:
            print(request.form.get('modif')[4:])
            if request.form.get('modif')[:3] == 'mod':
                modif_db = int(request.form.get('modif')[4:])
        if request.form.get('modify') is not None:
            if request.form.get('modify')[-7:] == 'mod_yes':
                print('modification:'+request.form.get('modify')[:-8])
                new_rec = [db,
                           request.form.get('modify')[:-8],
                           request.form.get('article'),
                           request.form.get('nb'),
                           request.form.get('périmé'),
                           request.form.get('mail'),
                           ]
                mod_db(*new_rec)
                #modifie_cave(*new_rec)
                return redirect(url_for('inventaire', database=db))
            if request.form.get('modify') == 'mod_no':
                print('annulation')
    return render_template('inventaire.html',
                           method='POST',
                           menu='inventaire',
                           db=db,
                           entete=db_select[db].entetes,
                           liste_db=liste_db,
                           modif_db=modif_db,

                           )

@app.route('/inventaire2/', methods=['POST', 'GET'])
def inventaire2():
    db = db_recup('cave')
    if request.method =='POST':
        params = request.form.to_dict()
        if params['command'] == 'del':
            db_del('cave',params['db_id'])
            print('DEBUG: {}'.format(params['db_id']))
            return json.dumps({'message':'ok'})
    return render_template('inventaire2.html',
                           db=db,
                           )

@app.route('/archives', methods=['POST', 'GET'])
def archives():
    return render_template('archives.html',
                           method='POST',
                           menu='archives',
                          )

@app.route('/documentation', methods=['POST', 'GET'])
def documentation():
    return render_template('documentation.html')

@app.route('/maison', methods=['POST', 'GET'])
def maison():
    return render_template('maison.html')

@app.route('/piscine', methods=['POST', 'GET'])
def piscine():
    return render_template('piscine.html')

@app.route('/raspberry', methods=['POST', 'GET'])
def raspberry():
    """pi1 = connection(config.pi1_conf[0], config.pi1_conf[1])
    pi2 = connection(config.pi2_conf[0], config.pi2_conf[1])"""
    return render_template('raspberry.html')

