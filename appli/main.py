from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
import os
import config
from config import Configuration

app = Flask(__name__)
app.config.from_object(Configuration)

from .fonctions import connection, db_recup, db_del, db_add,db_mod, add_message, gen_pdf
from . import models
from .models import db, Cave, Congel, Users, Messages

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

@app.template_filter()
def date_trunk(val):
    return val.strftime("%Y-%m-%d/%H:%M:%S")

@app.route('/', methods=['POST', 'GET'])
def index():
    posts = db.session.query(Messages)
    users = db.session.query(Users)
    if request.method == 'POST':
        querys_dict = request.form.to_dict()
        print(querys_dict)
        add_message(int(querys_dict['user_id']),querys_dict['message'] )

        return json.dumps({'message:':'OK'})
    return render_template('main.html', 
                           posts=posts,
                           users=users)


@app.route('/inventaire/<database>', methods=['POST', 'GET'])
@login_required
def inventaire(database):
    db = db_recup(database)
    if database == 'Messages':
        users = db_recup('users')
    else:
        users = None
    if request.method =='POST':
        params = request.form.to_dict()
        if params['command'] == 'del':
            db_del(database, params['db_id'])
            return json.dumps({'message':'ok'})
        if params['command'] == 'add':
            if database in ['cave', 'congel']:
                donnees = [params['article'], params['quantite'], params['date_fin']]           
                db_add(database, donnees)
            return json.dumps({'message':'ok'})
        if params['command'] == 'mod':
            if database in ['cave', 'congel']:
                donnees = [params['article'], params['quantite'], params['date_fin']]         
                db_mod(database, params['db_id'], donnees)
            return json.dumps({'message':'ok'})
        if params['command'] == 'pdf':
            print('DEBUG:PDF')
            gen_pdf()
            return json.dumps({'message':'ok'})
    return render_template('inventaire.html',
                           database=database,
                           db=db,
                           users=users
                           )

@app.route('/archives', methods=['POST', 'GET'])
@login_required
def archives():
    chemin = '/Users/mcwa/Pictures/Pictures'
    liste_dir = os.listdir(chemin)
    return render_template('archives.html',
                           liste=liste_dir,
                          )

@app.route('/documents', methods=['POST', 'GET'])
def documents():
    return render_template('documents.html'         
                           )

@login_required
@app.route('/user/<u_conected>', methods=['POST', 'GET'])
def user(u_conected):
    print(request.args.get('view'))
    if request.args.get('view') == 'messages':
        view = 'messages'
    else:
        view = 'params'
    user = db.session.query(Users).filter(Users.nom == u_conected).first()
    posts = db.session.query(Messages).filter(Messages.user_id == user.id)
   
    return render_template('user.html',
                           user=user, 
                           posts = posts,
                           view = view)

@app.route('/raspberry', methods=['POST', 'GET'])
def raspberry():
    """pi1 = connection(config.pi1_conf[0], config.pi1_conf[1])
    pi2 = connection(config.pi2_conf[0], config.pi2_conf[1])"""
    pi1 = [22 , 85, 'connecté']
    pi2 = [22 , 85, 'erreur']
    return render_template('raspberry.html',
                           pi1_data=pi1,
                           pi2_data=pi2,
                           pi1_conf=config.pi1_conf,
                           pi2_conf=config.pi2_conf
                           )

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
    