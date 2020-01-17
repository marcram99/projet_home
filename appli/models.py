from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import logging as lg

from .main import app

db = SQLAlchemy(app)

entetes = {'Cave': [['article', 4], ['nb', 1], ['périmé le ', 2], ['mail', 1] ],
           'Congel': [['article', 4], ['nb', 1], ['périmé le ', 2], ['mail', 1] ],
           'Users': [['nom', 3], ['mdp', 3], ['mail', 3], ['droits', 1]]}
           
class Cave(db.Model):
    __tablename__ = 'cave'
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(40), nullable=False)
    quantite = db.Column(db.Integer(), nullable=True)
    peremption = db.Column(db.String(), nullable=True)
    envoi_mail = db.Column(db.String(), nullable=True)

    entetes = [['article', 4], ['nb', 1], ['périmé le ', 2], ['mail', 1] ]
    champ_db = ['id', 'article', 'quantite', 'peremption', 'envoi_mail']
    
    def __init__(self, article, quantite, peremption, envoi_mail):
        self.article = article
        self.quantite = quantite
        self.peremption = peremption
        self.envoi_mail = envoi_mail
        
class Congel(db.Model):
    __tablename__ = 'congel'
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(40), nullable=False)
    quantite = db.Column(db.Integer(), nullable=True)
    peremption = db.Column(db.String(), nullable=True)
    envoi_mail = db.Column(db.String(), nullable=True)

    entetes = [['article', 4], ['nb', 1], ['périmé le ', 2], ['mail', 1] ]
    champ_db = [id, article, quantite, peremption, envoi_mail]

    def __init__(self, article, quantite, peremption, envoi_mail):
        self.article = article
        self.quantite = quantite
        self.peremption = peremption
        self.envoi_mail = envoi_mail

    def __repr__(self):
        return 'article:{} / nb: {} / perim.: {}'.format(self.article, self.quantite, self.peremption)

class Inventaire(db.Model):
    __tablename__ = 'inventaire'
    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(40), nullable=False)
    quantite = db.Column(db.Integer(), nullable=True)
    perime = db.Column(db.String(), nullable=True)
    tag = db.Column(db.String(), nullable=True)

    entetes = [['article', 4], ['nb', 1], ['périmé le ', 2]]
    champ_db = ['id', 'article', 'quantite', 'perime']


    def __init__(self, article, quantite, perime, tag):
        self.article = article
        self.quantite = quantite
        self.perime = perime
        self.tag = tag

    def __repr__(self):
        return 'article:{} / nb: {} / perim.: {}'.format(self.article, self.quantite, self.perime)


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False)
    mdp = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(20), nullable=True)
    droits = db.Column(db.String(20), nullable=True)
    posts = db.relationship('Messages', backref='auteur', lazy='dynamic')

    entetes = [['nom', 3], ['mdp', 3], ['mail', 3], ['droits', 1]]
    champ_db = [id, nom, mdp, mail, droits]
    
    def __init__(self, nom, mdp, mail, droits):
        self.nom = nom
        self.mdp = generate_password_hash(mdp, method='sha256')
        self.mail = mail
        self.droits = droits

    def __repr__(self):
        return 'user: {} / {} /  {}/  {}'.format(self.nom, self.mdp, self.mail, self.droits)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message


def init_db():
    print('lancé init_db')
    db.drop_all()
    db.create_all()
    db.session.add(Inventaire('pates', 3, '01.01.2019','cave'))
    db.session.add(Inventaire('pq', 1, '01.01.2019','cave'))
    db.session.add(Inventaire('pizza margeritte', 1, '01.01.2019','congel'))
    db.session.add(Users('marcram', 'marcram', 'marcram99@gmail.com', 'admin'))
    db.session.add(Users('Marc', 'marcram', 'marcram99@gmail.com', 'user'))
    db.session.add(Users('Sophie', 'sosso', 'slofie130@gmail.com', 'user'))
    db.session.add(Users('Nolan', 'nono', 'no_mail', 'user'))
    db.session.add(Users('Timéo', 'timi', 'no_mail', 'user'))
    db.session.add(Messages(1,'Bonjour... premier message'))
    db.session.add(Messages(1,'Et un deuxième message'))
    db.session.add(Messages(1,'Et de 3 pour moi'))
    db.session.add(Messages(3,'Un message pour Sosso'))
    db.session.commit()
    lg.warning('db initialisée!')