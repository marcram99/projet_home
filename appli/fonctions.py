import socket, sys
from sqlalchemy import text
from fpdf import FPDF
from datetime import datetime

from .models import db, Cave, Congel, Users, Messages


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
    database = {'cave': Cave, 'congel': Congel, 'users': Users, 'Messages': Messages}
    resultat = database[dbase].query.all()
    return resultat

def db_del(dbase, id):
    database = {'cave': Cave, 'congel': Congel, 'users': Users, 'Messages': Messages}
    article = database[dbase].query.get(id)
    db.session.delete(article)
    db.session.commit()
    print('DEBUG: delete article avec id: {}'.format(id))

def db_add(dbase, donnees):
    database = {'cave': Cave, 'congel': Congel, 'users': Users}
    article, nb, périmé = donnees
    db.session.add(database[dbase](article, nb, périmé, 'non'))
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
def gen_pdf():
    now = datetime.now().strftime('%d-%m-%y / %H:%M')
    texte = " Inventaire de la cave au: {}".format(now)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=texte, ln=1, align="C")

    data = [['First Name', 'Last Name', 'email', 'zip'],
            ['Mike', 'Driscoll', 'mike@somewhere.com', '55555'],
            ['John', 'Doe', 'jdoe@doe.com', '12345'],
            ['Nina', 'Ma', 'inane@where.com', '54321']
            ]
 
    col_width = pdf.w / 4.5
    row_height = pdf.font_size
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height*1,
                     txt=item, border=1)
        pdf.ln(row_height*1)

    pdf.output("inventaire.pdf")
