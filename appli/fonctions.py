import socket, sys
from sqlalchemy import text

from .models import db, Cave, Congel, Users



def connection(host,port):
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((host, port))
        temp = my_socket.recv(4096).decode("Utf8")
        hum = my_socket.recv(4096).decode("Utf8")
        conn_message = 'connecté'
        my_socket.send(b"data received!")
        my_socket.close()
    except OSError as erreur:
        conn_message = erreur
        temp = 0
        hum = 0
    return temp, hum, conn_message


def db_recup(dbase):
    database = {'cave': Cave, 'congel': Congel, 'users': Users}
    resultat = database[dbase].query.all()
    return resultat

def db_del(dbase, id):
    database = {'cave': Cave, 'congel': Congel, 'users': Users}
    article = database[dbase].query.get(id)
    db.session.delete(article)
    db.session.commit()
    print('DEBUG: delete article avec id: {}'.format(id))

def db_add(dbase, donnees):
    database = {'cave': Cave, 'congel': Congel, 'users': Users}
    article, nb, périmé = donnees
    db.session.add(database[dbase](article, nb, périmé, 'non'))
    db.session.commit()
    print('DEBUG: ajout article ')

# ------------ old db --------------------------
def recup_db(db):
    db_select = {'Cave': Cave, 'Congel': Congel, 'Users': Users}
    liste_db=[]
    resultat = db_select[db].query.all()
    for r in resultat:
        if db == 'Cave' or db == 'Congel':
            db_items = [r.id, r.article, r.quantite, r.peremption, r.envoi_mail]
        elif db == 'Users':
            db_items = [r.id, r.nom, r.mdp, r.mail, r.droits]
        liste_db.append(db_items)
    return liste_db

def add_db(donnees):
    database, article, nb, périmé, mail = donnees
    db_select = {'Cave': Cave, 'Congel': Congel, 'Users': Users}
    db.session.add(db_select[database](article, nb, périmé, mail))
    db.session.commit()

def del_db(database, id):
    db_select = {'Cave': Cave, 'Congel': Congel, 'Users': Users}
    article = db_select[database].query.get(id)
    db.session.delete(article)
    db.session.commit()

def mod_db(*donnees):
    if donnees[0] == 'Cave':
        database, id, article, nb, perime, mail = donnees
        print(database, id, article, nb, perime, mail)
        db.session.query(Cave).filter(text("id = :val")).params(val=int(id)).update({Cave.article:article},synchronize_session = False)
        db.session.query(Cave).filter(text("id = :val")).params(val=int(id)).update({Cave.quantite:nb},synchronize_session = False)
        db.session.query(Cave).filter(text("id = :val")).params(val=int(id)).update({Cave.peremption:perime},synchronize_session = False)
        db.session.query(Cave).filter(text("id = :val")).params(val=int(id)).update({Cave.envoi_mail:mail},synchronize_session = False)
        db.session.commit()
    if donnees[0] == 'Congel':
        database, id, article, nb, perime, mail = donnees
        print(database, id, article, nb, perime, mail)
        db.session.query(Congel).filter(text("id = :val")).params(val=int(id)).update({Congel.article:article},synchronize_session = False)
        db.session.query(Congel).filter(text("id = :val")).params(val=int(id)).update({Congel.quantite:nb},synchronize_session = False)
        db.session.query(Congel).filter(text("id = :val")).params(val=int(id)).update({Congel.peremption:perime},synchronize_session = False)
        db.session.query(Congel).filter(text("id = :val")).params(val=int(id)).update({Congel.envoi_mail:mail},synchronize_session = False)
        db.session.commit()



