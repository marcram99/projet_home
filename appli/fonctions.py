import socket, sys
from sqlalchemy import text
from fpdf import FPDF
from pathlib import Path
from datetime import datetime

from .models import db, Cave, Congel, Users, Messages, Inventaire

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
    database = {'cave': Inventaire, 'congel': Inventaire, 'users': Users, 'Messages': Messages}
    resultat = database[dbase].query.filter(database[dbase].tag == dbase)
    return resultat

def db_del(dbase, id):
    database = {'cave': Inventaire, 'congel': Inventaire, 'users': Users, 'Messages': Messages}
    article = database[dbase].query.get(id)
    db.session.delete(article)
    db.session.commit()
    print('DEBUG: delete article avec id: {}'.format(id))

def db_add(dbase, donnees):
    database = {'cave': Inventaire, 'congel': Inventaire, 'users': Users}
    article, nb, périmé = donnees
    db.session.add(database[dbase](article, nb, périmé, dbase))
    db.session.commit()
    print('DEBUG: ajout article {}/{}'.format(dbase, donnees))

def db_mod(database, id, donnees):
    dbase = {'cave': Cave, 'congel': Congel}[database]
    valeurs = {dbase.article: donnees[0], dbase.quantite:donnees[1], dbase.peremption:donnees[2]}
    record = db.session.query(dbase).filter(text("id = :val")).params(val=int(id))
    record.update(valeurs, synchronize_session = False)
    db.session.commit()
    print('DEBUG: modif article {}/{}'.format(database, donnees))

# ------------ messages --------------------------
def add_message(user, message):
    db.session.add(Messages(user, message))
    db.session.commit()
    print('message ajouté')
# ------------ pdf --------------------------
def gen_pdf(database):
    now = datetime.now().strftime('%d-%m-%y %H:%M')
    pdf_file = Path(__file__).parent.joinpath('static/files/inventaire_{}.pdf'.format(database))
    titre = " Inventaire {} au {}".format(database, now)
    data =[['article', 'nombre', 'date']]
    db_data = db_recup(database)
    for lignes in db_data:
        data.append([lignes.article, str(lignes.quantite), str(lignes.peremption)])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt=titre, ln=1)
    pdf.ln(1)
    col_width = pdf.w / 4.5
    row_height = pdf.font_size + 3
    for row in data:
        pdf.cell(65, row_height,txt=row[0], border=1)
        pdf.cell(20, row_height,txt=row[1], border=1, align="C")
        pdf.cell(30, row_height,txt=row[2], border=1, align="C")
        pdf.ln(row_height*1)
    pdf.output(pdf_file)
