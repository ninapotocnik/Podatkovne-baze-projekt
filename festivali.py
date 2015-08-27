import bottle
import modeli

bottle.debug(True)

# Mapa s statičnimi datotekami (pridobljeno na github prof. Bauer)
static_dir = "./static"

################################################

# homepage
@bottle.route('/')
@bottle.view('homepage')
def homepage():
    festivali = modeli.iskanje()
    komentarji = modeli.komentarji()
    return {
        'festivali': festivali,
        'komentarji': komentarji
    }

# iskanje festivalov po imenu
@bottle.route('/iskanje/')
@bottle.view('iskanje')
def iskanje():
    ime = bottle.request.query.ime
    festivali = modeli.iskanje(ime = ime)
    return {
        'iskano_ime': ime,
        'festivali': festivali
    }

# napaka pri dodajanju komentarja
@bottle.route('/napaka/')
@bottle.view('napaka')
def napaka():
    napaka2 = 'Niste vpisali komentarja ali uporabniškega imena.'
    napaka3 = 'Niste vpisali komentarja in uporabniškega imena.'
    return {'napaka2': napaka2}

# napaka pri dodajanju nastopajočega
@bottle.route('/napaka1/')
@bottle.view('napaka1')
def napaka1():
    napaka3 = 'Niste vpisali glasbenika ali datuma.'
    return {'napaka3': napaka3}

# napaka pri dodajanju festivala
@bottle.route('/napaka2/')
@bottle.view('napaka2')
def napaka1():
    napaka4 = 'Izpolniti morate vsa polja.'
    return {'napaka4': napaka4}

# dodajanje komentarjev
@bottle.post('/festival/<id>/komentar/')
def dodaj_komentar(id):
    komentar = bottle.request.forms.get('komentar')
    uporabnisko_ime = bottle.request.forms.get('uporabnisko_ime')
    if komentar == '' or uporabnisko_ime == '':
        bottle.redirect('/napaka/')
    else:
        modeli.dodaj_komentar(id, komentar, uporabnisko_ime)
        naslov = '/festival/' + str(id)
        bottle.redirect(naslov)

# isaknje in dodajanje komentarjev
@bottle.post('/iskanje/festival/<id>/komentar/')
def dodaj_komentar(id):
    komentar = bottle.request.forms.get('komentar')
    uporabnisko_ime = bottle.request.forms.get('uporabnisko_ime')
    if komentar == '' or uporabnisko_ime == '':
        bottle.redirect('/napaka/')
    else:
        modeli.dodaj_komentar(id, komentar, uporabnisko_ime)
        naslov = '/iskanje/festival/' + str(id)
        bottle.redirect(naslov)

# pregled podatkov o festivalu
@bottle.route('/festival/<id>')
@bottle.view('festival')
def festival(id):
    podatki = modeli.pridobi_podatke(id)
    nastopi = modeli.nastopi(id)
    komentarji = modeli.komentarji_festival(id)
    return {'podatki': podatki,
            'nastopi': nastopi,
            'komentarji': komentarji}


# iskanje in pregled festivala
@bottle.route('/iskanje/festival/<id>')
@bottle.view('iskanje')
@bottle.view('festival')
def festival(id):
    podatki = modeli.pridobi_podatke(id)
    nastopi = modeli.nastopi(id)
    komentarji = modeli.komentarji_festival(id)
    return {'podatki': podatki,
            'nastopi': nastopi,
            'komentarji': komentarji}


# podatki o nakupu vstopnice za nastop na festivalu
@bottle.route('/festival/glasbenik/<id>')
@bottle.view('festival')
@bottle.view('glasbenik')
def nakup_nastop(id):
    podatki_nastop = modeli.podatki_nastop(id)
    cena_nastop = modeli.cena_nastopa(id)
    return {'podatki_nastop': podatki_nastop,
            'cena_nastop': cena_nastop}

# podatki o nakupu vstopnice za nastop na festivalu
@bottle.route('/iskanje/festival/glasbenik/<id>')
@bottle.view('iskanje')
@bottle.view('festival')
@bottle.view('glasbenik')
def nakup_nastop(id):
    podatki_nastop = modeli.podatki_nastop(id)
    cena_nastop = modeli.cena_nastopa(id)
    return {'podatki_nastop': podatki_nastop,
            'cena_nastop': cena_nastop}

# nakup vstopnice za nastop
@bottle.route('/festival/glasbenik/<id>/nakupljeno')
@bottle.view('festival')
@bottle.view('glasbenik')
@bottle.view('nakupljeno')
def nakupljeno(id):
    kolicina = bottle.request.query.kolicina
    stevilka_kartice = bottle.request.query.stevilka_kartice
    stevilka_monete = bottle.request.query.stevilka_monete
    if kolicina == '' or int(kolicina) <= 0:
        napaka = 'Niste vpisali števila vstopnic, ki jih želite kupiti ali pa ste vpisali napačno vrednost.'
        cena_skupaj = 0
        napaka1 = None
    elif stevilka_kartice == '' and stevilka_monete == '':
        napaka1 = 'Niste vpisali številke kartice ali monete.'
        napaka = None
        cena_skupaj = 0
    else:
        napaka = None
        napaka1 = None
        cena_skupaj = modeli.izdaj_vstopnico_nastop(id, kolicina)
    return {'kolicina': kolicina,
            'cena_skupaj': cena_skupaj,
            'napaka': napaka,
            'napaka1': napaka1}

# nakup vstopnice za nastop
@bottle.route('/iskanje/festival/glasbenik/<id>/nakupljeno')
@bottle.view('iskanje')
@bottle.view('festival')
@bottle.view('glasbenik')
@bottle.view('nakupljeno')
def nakupljeno(id):
    kolicina = bottle.request.query.kolicina
    stevilka_kartice = bottle.request.query.stevilka_kartice
    stevilka_monete = bottle.request.query.stevilka_monete
    if kolicina == '' or int(kolicina) <= 0:
        napaka = 'Niste vpisali števila vstopnic, ki jih želite kupiti ali pa ste vpisali napačno vrednost.'
        cena_skupaj = 0
        napaka1 = None
    elif stevilka_kartice == '' and stevilka_monete == '':
        napaka1 = 'Niste vpisali številke kartice ali monete.'
        napaka = None
        cena_skupaj = 0
    else:
        napaka = None
        napaka1 = None
        cena_skupaj = modeli.izdaj_vstopnico_nastop(id, kolicina)
    return {'kolicina': kolicina,
            'cena_skupaj': cena_skupaj,
            'napaka': napaka,
            'napaka1': napaka1}

# podatki o nakupu vstopnice za festival
@bottle.route('/<id>/nakup_vstopnice/')
@bottle.view('nakup_vstopnice')
def nakup_vstopnice(id):
    podatki = modeli.pridobi_podatke(id)
    return {'podatki': podatki}

# nakup vstopnice za festival
@bottle.route('/<id>/nakup_vstopnice/nakupljeno_festival')
@bottle.view('nakup_vstopnice')
@bottle.view('nakupljeno_festival')
def nakupljeno_festival(id):
    kolicina = bottle.request.query.kolicina
    stevilka_kartice = bottle.request.query.stevilka_kartice
    stevilka_monete = bottle.request.query.stevilka_monete
    if kolicina == '' or int(kolicina) <= 0:
        napaka = 'Niste vpisali števila vstopnic, ki  jih želite kupiti ali pa ste vpisali napačno vrednost.'
        cena_skupaj = 0
        napaka1 = None
    elif stevilka_kartice == '' and stevilka_monete == '':
        napaka1 = 'Niste vpisali številke kartice ali monete.'
        napaka = None
        cena_skupaj = 0
    else:
        napaka = None
        napaka1 = None
        cena_skupaj = modeli.izdaj_vstopnico_festival(id, kolicina)
    return {'kolicina': kolicina,
            'cena_skupaj': cena_skupaj,
            'napaka': napaka,
            'napaka1': napaka1}

# dodajanje festivalov
@bottle.post('/dodaj_festival/')
def dodaj_festival():
    ime = bottle.request.forms.get('ime')
    lokacija = bottle.request.forms.get('lokacija')
    datum_zacetek = bottle.request.forms.get('datum_zacetek')
    datum_konec = bottle.request.forms.get('datum_konec')
    cena = bottle.request.forms.get('cena')
    stevilo_vstopnic = bottle.request.forms.get('stevilo_vstopnic')
    if ime == '' or lokacija == '' or datum_zacetek == '' or datum_konec == '' or cena == '' or stevilo_vstopnic == '':
        bottle.redirect('/napaka2/')
    else:
        modeli.dodaj_festival(ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic)
        bottle.redirect('/')

# dodajanje nastopajočih
@bottle.post('/festival/<id>/dodaj_nastopajoce/')
def dodaj_nastopajoce(id):
    glasbenik = bottle.request.forms.get('glasbenik')
    datum = bottle.request.forms.get('datum')
    if glasbenik == '' or datum == '':
        bottle.redirect('/napaka1/')
    else:
        modeli.dodaj_nastopajoce(id, glasbenik, datum)
        
        naslov = '/festival/' + str(id)
        bottle.redirect(naslov)

# iskanje in dodajanje nastopajočih
@bottle.post('/iskanje/festival/<id>/dodaj_nastopajoce/')
def dodaj_nastopajoce(id):
    glasbenik = bottle.request.forms.get('glasbenik')
    datum = bottle.request.forms.get('datum')
    if glasbenik == '' or datum == '':
        bottle.redirect('/napaka1/')
    else:
        modeli.dodaj_nastopajoce(id, glasbenik, datum)
        naslov = '/festival/' + str(id)
        bottle.redirect(naslov)

#################################################################################################


#(pridobljeno na githubu prof. Bauerja)
@bottle.route("/static/<filename:path>")
def static(filename):
    """Splošna funkcija, ki servira vse statične datoteke iz naslova
       /static/..."""
    return bottle.static_file(filename, root=static_dir)


################################################

bottle.run(host='localhost', port=8080)
