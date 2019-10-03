from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
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

# ------ configuration du login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = u"Vous devez être connecté pour accéder à cette page..."
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Users.query.get(int(user_id))
   

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('main.html')

@app.route('/inventaire/', methods=['POST', 'GET'])
@login_required
def inventaire():
    db = db_recup('users')
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
@login_required
def archives():
    return render_template('archives.html',
                           method='POST',
                           menu='archives',
                          )

@app.route('/documentation', methods=['POST', 'GET'])
def documentation():
    return render_template('documentation.html')

@app.route('/documents', methods=['POST', 'GET'])
def documents():
    return render_template('documents.html')

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
    print('DEBUG: login')
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_post():
    print('DEBUG: login post')
    username = request.form.get('username')
    password = request.form.get('pwd')
    remember = True if request.form.get('remember') else False
    user = Users.query.filter_by(nom=username).first()
    print('DEBUG: user = {}'.format(user))
    if not user or not check_password_hash(user.mdp, password): 
        flash('ERREUR !!!  veuillez réessayer...')
        return redirect(url_for('login')) 
    flash(user.nom)
    login_user(user, remember=remember)
    print("DEBUG: login_user={}".format(user))
    return redirect(url_for('index'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réusie!')
    return redirect(url_for('index'))
    