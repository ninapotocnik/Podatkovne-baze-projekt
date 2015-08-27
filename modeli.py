import sqlite3
import hashlib
import datetime

datoteka_baze = 'festivalskoPoletje.sqlite3'

def iskanje(ime = '', lokacija = '', min_cena = 30, max_cena = 1000, min_datum = None, max_datum = None):
    '''Poišče festivale glede na podane zahteve.'''
    cur = baza.cursor()
    sql = '''SELECT festival.id, festival.ime FROM festival
              WHERE (festival.ime LIKE ?)'''
    podatki = ['%'+ ime + '%']
    if min_datum is not None:
        sql += " AND festival.datum_zacetek > ?"
        podatki += [min_datum]
    if max_datum is not None:
        sql += " AND festival.datum_konec < ?"
        podatki += [max_datum]

    cur.execute(sql, podatki)
    rez_iskanja = cur.fetchall()

    # da se zadetki ne ponavljajo
    rezultat_iskanja = []
    # če se ponavljajo
    for i in range(len(rez_iskanja) - 1):
        if rez_iskanja[i] != rez_iskanja[i+1]:
            rezultat_iskanja.append(rez_iskanja[i])
    # če ni nobenega zadetka
    if len(rez_iskanja) == 0:
        rezultat_iskanja = []
    # če so vsi zadetki enaki
    else:
        rezultat_iskanja.append(rez_iskanja[len(rez_iskanja)-1])

    cur.close()
    return rezultat_iskanja


def izdaj_vstopnico_festival(id_festival, kolicina, popust = 0):
    '''Vstopnica za festival.'''
    # popust je v odstotkih
    if kolicina == '':
        kolicina = 0
    cur = baza.cursor()
    cur.execute('''SELECT stevilo_vstopnic, st_prodanih_festival FROM festival WHERE id = ?
              ''', [id_festival])
    rez = cur.fetchone()
    if rez is None:
        raise Exception("Ni tega festivala.")
    else:
        (stevilo_vstopnic, st_prodanih_festival) = rez

    stevilo_vstopnic = rez[0]

    # če še nimamo nobene prodane vstopnice, potem None pretvorimo v 0, da lahko računamo
    st_prodanih_festival = rez[1]
    if st_prodanih_festival == None:
        st_prodanih_festival = 0
    # pogledamo samo tiste nastope, ki so na festivalu, za katerega izdajamo vstopnico
    cur.execute('''SELECT st_prodanih_nastop FROM nastopi WHERE id_festival = ?
              ''', [id_festival])
    rez1 = cur.fetchone()
    
    if rez1 is None:
        raise Exception("Ni tega nastopa.")
    else:
        st_prodanih_nastop = rez1[0]

    # če še nimamo nobene prodane vstopnice, potem None pretvorimo v 0, da lahko računamo
    if st_prodanih_nastop == None:
        st_prodanih_nastop = 0

    # preštejemo število nastopov na festivalu, za katerega izdajamo vstopnico
    cur.execute('''SELECT COUNT(id) FROM nastopi WHERE id_festival = ?
              ''', [id_festival])
    st_nastopov = cur.fetchone()
    st_nastopov = st_nastopov[0]
    
    # ce je nastop že razprodan, potem damo popust na ceno festivala
    popust_zaradi_nastopa = 1 - (st_prodanih_nastop/st_nastopov)
    
    # cena festivala za katerega izdajamo vstopnico
    cur.execute('''SELECT cena FROM festival WHERE id = ?''', [id_festival])
    rez = cur.fetchone()
    cena = rez[0]

    # ime festivala
    cur.execute('''SELECT ime FROM festival WHERE id = ?''', [id_festival])
    rez1 = cur.fetchone()
    ime_festivala = rez1[0]
    
    if st_prodanih_nastop == st_nastopov:
        cena_skupaj = cena * int(kolicina) * (1 - popust//100) * popust_zaradi_nastopa
        # vstopnica je prodana
        cur.execute('''INSERT INTO Vstopnice (id_festivala, ime_festivala, kolicina, cena_prej, cena_skupaj, popust)
                        VALUES (?, ?, ?, ?, ?, ?)''', [id_festival, ime_festivala, kolicina, cena, cena_skupaj, popust])
        # odštejejo se kupljene vstopnice
        cur.execute('''UPDATE festival SET st_prodanih_festival = ?''', [st_prodanih_festival + int(kolicina)])

    if stevilo_vstopnic >= int(kolicina):
        cena_skupaj = cena * int(kolicina) * (1 - popust//100)
        # vstopnica je prodana
        cur.execute('''INSERT INTO Vstopnice (id_festivala, ime_festivala, kolicina, cena_prej, cena_skupaj, popust)
                        VALUES (?, ?, ?, ?, ?, ?)''', [id_festival, ime_festivala, kolicina, cena, cena_skupaj, popust])
        # prištejemo prodane vstopnice
        cur.execute('''UPDATE festival SET st_prodanih_festival = ? WHERE id = ?''', [st_prodanih_festival + int(kolicina), id_festival])
    else:
        raise Exception('Na zalogi nimamo dovolj vstopnic. Kupite jih lahko toliko kot jih je še na voljo.')
    cur.close()
##    return str(id_festival)
    return cena_skupaj

def izdaj_vstopnico_nastop(id_nastopa, kolicina, popust = 0):
    '''Vstopnica za nastop.'''
    # popust je v odstotkih
    if kolicina == '':
        kolicina = 0
    cur = baza.cursor()
    # prodane vstopnice in id festivala, da lahko dobimo koliko je vseh vstopnic
    cur.execute('''SELECT st_prodanih_nastop, id_festival FROM nastopi WHERE id = ?
              ''', [id_nastopa])
    rez = cur.fetchone()
    
    if rez is None:
        raise Exception("Ni tega nastopa.")
    else:
        (st_prodanih_nastop, id_festival) = rez

    st_prodanih_nastop = rez[0]
    id_festival = rez[1]

    if st_prodanih_nastop == None:
        st_prodanih_nastop = 0
    
    # koliko je vseh vstopnic
    cur.execute('''SELECT stevilo_vstopnic FROM festival WHERE id = ?''', [id_festival])
    rez1 = cur.fetchone()

    stevilo_vstopnic = rez1[0]
    
    # Koliko vstopnic je že prodanih za festival, na katerem je ta nastop
    cur.execute('''SELECT st_prodanih_festival FROM festival JOIN nastopi ON nastopi.id_festival = festival.id WHERE nastopi.id = ?
              ''', [id_nastopa])
    rez2 = cur.fetchone()

    if rez2 is None:
        raise Exception('Ni tega festivala.')
    else:
        st_prodanih_festival = rez2[0]

    if st_prodanih_festival == None:
        st_prodanih_festival = 0
 
    # preštejemo število nastopov na festivalu, za katerega izdajamo vstopnico
    cur.execute('''SELECT COUNT(id_festival) FROM nastopi WHERE id_festival = ?
              ''', [id_festival])
    st_nastopov = cur.fetchone()
    st_nastopov = st_nastopov[0]

    # cena festivala za katerega izdajamo vstopnico
    cur.execute('''SELECT cena FROM festival JOIN nastopi ON nastopi.id_festival = festival.id WHERE nastopi.id = ?'''
                , [id_nastopa])
    rez3 = cur.fetchone()
    cena = rez3[0]// st_nastopov

    if st_prodanih_festival + st_prodanih_nastop + int(kolicina) <= stevilo_vstopnic:
        cena_skupaj = cena * int(kolicina) * (1 - popust/100)

        # vstopnica je prodana
        cur.execute('''INSERT INTO vstopnice_nastopi (cena_prej, popust, cena_skupaj, id_nastop, stevilo)
                        VALUES (?, ?, ?, ?, ?)''', [cena, popust, cena_skupaj, id_nastopa, kolicina])
        # prištejejo se kupljene vstopnice
        cur.execute('''UPDATE nastopi SET st_prodanih_nastop = ? WHERE id = ?''', [st_prodanih_nastop + int(kolicina), id_nastopa])
    cur.close()
    return cena_skupaj


def cena_nastopa(id_nastopa):
    '''Cena nastopa na festivalu.'''
    cur = baza.cursor()
    # prodane vstopnice in id festivala, da lahko dobimo koliko je vseh vstopnic
    cur.execute('''SELECT id_festival FROM nastopi WHERE id = ?
              ''', [id_nastopa])
    rez = cur.fetchone()
    id_festival = rez[0]
    # preštejemo število nastopov na festivalu, za katerega izdajamo vstopnico
    cur.execute('''SELECT COUNT(id_festival) FROM nastopi WHERE id_festival = ?
              ''', [id_festival])
    st_nastopov = cur.fetchone()
    st_nastopov = st_nastopov[0]
    cur.execute('''SELECT cena FROM festival JOIN nastopi ON nastopi.id_festival = festival.id WHERE nastopi.id = ?'''
                , [id_nastopa])
    rez3 = cur.fetchone()
    cena = rez3[0]// st_nastopov
    return cena


def dodaj_komentar(id_festival, komentar, uporabnisko_ime):
    '''V bazo dodamo komentar.'''
    cur = baza.cursor()
    cur.execute('''INSERT INTO komentarji (id_festival, komentar, uporabnisko_ime) VALUES (?, ?, ?)''', [id_festival, komentar, uporabnisko_ime])
    cur.close()
    id_komentar = cur.lastrowid
    return id_komentar


def komentarji():
    '''Pridobimo vse komentarje.'''
    cur = baza.cursor()
    cur.execute('''SELECT uporabnisko_ime, komentar FROM komentarji''')
    komentarji = cur.fetchall()
    return komentarji


def komentarji_festival(id):
    '''Komentarji za določen festival.'''
    cur = baza.cursor()
    cur.execute('''SELECT id_festival, uporabnisko_ime, komentar FROM komentarji WHERE id_festival = ?''', [id])
    komentarji = cur.fetchall()
    return komentarji

        
def dodaj_festival(ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic):
    '''Dodamo festival v bazo.'''
    cur = baza.cursor()
    cur.execute('''INSERT INTO festival (ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic) VALUES (?, ?, ?, ?, ?, ?)'''
                , [ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic])
    cur.close()

def dodaj_nastopajoce(id, glasbenik, datum):
    '''Dodamo nastope v bazo.'''
    cur = baza.cursor()
    # vstavimo glasbenika 
    cur.execute('''INSERT INTO glasbeniki (glasbenik) VALUES (?)''', [glasbenik])
    # id pravkar vstavljenega glasbenika
    cur.execute('''SELECT id FROM glasbeniki WHERE glasbenik = ?''', [glasbenik])
    id_glasbenik = cur.fetchall()
    id_glasbenik = id_glasbenik[0][0]
    cur.execute('''INSERT INTO nastopi (id_festival, id_glasbenik, datum) VALUES (?, ?, ?)''', [id, id_glasbenik, datum])
    cur.close()
    
    
def pridobi_podatke(id):
    '''Pridobimo vse podatke o določenem festivalu.'''
    cur = baza.cursor()
    podatki_festival = cur.execute('''SELECT festival.ime, festival.lokacija, festival.datum_zacetek,
                festival.datum_konec, festival.cena, stevilo_vstopnic, st_prodanih_festival, festival.id FROM festival 
                WHERE festival.id = ?''', [id])
    rez_festival = cur.fetchall()
    podatki_nastopi = cur.execute('''SELECT glasbeniki.glasbenik FROM glasbeniki JOIN nastopi ON glasbeniki.id = nastopi.id_glasbenik
                            JOIN festival ON nastopi.id_festival = festival.id WHERE festival.id = ?''', [id])
    rez_nastopi = cur.fetchall()
    cur.close()
    podatki = rez_festival + rez_nastopi
    ime = podatki[0][0]
    lokacija = podatki[0][1]
    # datum zapišemo v lepši obliki
    datum_zacetek = '{0.day}. {0.month}. {0.year}'.format(podatki[0][2])
    datum_konec = '{0.day}. {0.month}. {0.year}'.format(podatki[0][3])
    cena = podatki[0][4]
    stevilo_vstopnic = podatki[0][5]
    st_prodanih_festival = podatki[0][6]
    id_festival = podatki[0][7]
    nastopajoci = podatki[1:]
    nastopi = []
    # ker so nastopajoči podani v naborih
    for el in nastopajoci:
        nastopi.append(el[0])
    if st_prodanih_festival == None:
        st_prodanih_festival = 0
    return [(ime, lokacija, datum_zacetek, datum_konec, cena, stevilo_vstopnic, st_prodanih_festival, id_festival)]

def podatki_nastop(id):
    '''Podatki o glasbeniku in festivalu na katerem nastopa.'''
    cur = baza.cursor()
    podatki_nastopi = cur.execute('''SELECT nastopi.id, nastopi.datum, glasbeniki.glasbenik, festival.ime, festival.cena FROM glasbeniki JOIN nastopi ON glasbeniki.id = nastopi.id_glasbenik
                            JOIN festival ON nastopi.id_festival = festival.id WHERE nastopi.id = ?''', [id])
    podatki = cur.fetchall()
    cur.close()
    return podatki


def nastopi(id):
    '''Podatki o nastopih na festivalu.'''
    cur = baza.cursor()
    podatki_nastopi = cur.execute('''SELECT nastopi.id, glasbeniki.glasbenik FROM glasbeniki JOIN nastopi ON glasbeniki.id = nastopi.id_glasbenik
                            JOIN festival ON nastopi.id_festival = festival.id WHERE festival.id = ?''', [id])
    nastopi = cur.fetchall()
    cur.close()
    return nastopi

    
baza = sqlite3.connect(datoteka_baze, isolation_level = None, detect_types=sqlite3.PARSE_DECLTYPES)
