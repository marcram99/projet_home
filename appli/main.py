from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
import json
import config
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)


from .fonctions import connection, db_recup, db_del, db_add 
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
    db = db_recup('cave')
    if request.method =='POST':
        params = request.form.to_dict()
        if params['command'] == 'del':
            db_del('cave',params['db_id'])
            return json.dumps({'message':'ok'})
        if params['command'] == 'add':
            donnees = [params['article'], params['quantité'], params['date_fin']]
            db_add('cave', donnees)
            return json.dumps({'message':'ok'})
    return render_template('inventaire.html',
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = Users.query.filter_by(nom=username).first()
    if not user or not check_password_hash(user.mdp, password): 
        flash('Please check your login details and try again.')
        return redirect(url_for('login')) 
    return redirect(url_for('index'))
    