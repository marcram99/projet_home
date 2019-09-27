import os

chemin = os.path.abspath(os.path.dirname(__file__))
pi1_conf = ['192.168.1.50', 5555]
pi2_conf = ['192.168.1.51', 5555]

class Configuration():
    chemin = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(chemin, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'super mot de passe introuvable'
