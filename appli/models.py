from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
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

    def __repr__(self):
        return 'article:{} / nb: {} / perim.: {}'.format(self.article, self.quantite, self.peremption)


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


class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(20), nullable=False)
    mdp = db.Column(db.String(20), nullable=False)
    mail = db.Column(db.String(20), nullable=True)
    droits = db.Column(db.String(20), nullable=True)

    entetes = [['nom', 3], ['mdp', 3], ['mail', 3], ['droits', 1]]
    champ_db = [id, nom, mdp, mail, droits]
    
    def __init__(self, nom, mdp, mail, droits):
        self.nom = nom
        self.mdp = generate_password_hash(mdp, method='sha256')
        self.mail = mail
        self.droits = droits

    def __repr__(self):
        return 'user: {} / {} /  {}/  {}'.format(self.nom, self.mdp, self.mail, self.droits)


def init_db():
    print('lancé init_db')
    db.drop_all()
    db.create_all()
    db.session.add(Cave('pates', 3, '01.01.2019','oui'))
    db.session.add(Cave('pq', 1, '01.01.2019','non'))
    db.session.add(Congel('pizza margeritte', 1, '01.01.2019','oui'))
    db.session.add(Users('marcram', 'marcram', 'marcram99@gmail.com', 'admin'))
    db.session.add(Users('Marc', 'marcram', 'marcram99@gmail.com', 'user'))
    db.session.add(Users('Sophie', 'sosso', 'slofie130@gmail.com', 'user'))
    db.session.add(Users('Nolan', 'nono', 'no_mail', 'user'))
    db.session.add(Users('Timéo', 'timi', 'no_mail', 'user'))
    db.session.commit()
    lg.warning('db initialisée!')