import sqlite3
import hashlib

# iskanje??

datoteka_baze = 'festivalskoPoletje.sqlite3'

def iskanje(ime = '', lokacija = '', min_cena = 30, max_cena = 1000, min_datumZ = '1.5.2014', max_datumZ = '1.9.2014', min_datumK = '3.5.2014', max_datumK = '30.9.2014'):
    '''Poišče festival glede na podane zahteve.'''
    cur = baza.cursor()
    cur.execute('''SELECT festival.id, festival.ime FROM festival JOIN nastopi ON festival.id = nastopi.id_festival
              JOIN glasbeniki ON nastopi.id_glasbenik = glasbenik.id
              WHERE (festival.ime LIKE ? OR glasbeniki.glasbenik LIKE ?)
              AND festival.lokacija LIKE ?
              AND festival.cena BETWEEN ? AND ?
              AND festival.datum_zacetek BETWEEN ? AND ?
              AND festival.datum_konec BETWEEN ? AND ?
              ''', [ime, ime, lokacija, min_cena, max_cena, min_datumZ, max_datumZ, min_datumK, max_datumK])
    rezultat_iskanja = cur.fetchall()
    cur.close()
    return rezultat_iskanja

def izdaj_vstopnico_festival(id_festival, kolicina, popust = 0):
    '''Vstopnica za festival.'''
    # popust je v odstotkih
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
        cena_skupaj = cena * kolicina * (1 - popust/100) * popust_zaradi_nastopa
        # vstopnica je prodana
        cur.execute('''INSERT INTO Vstopnice (id_festivala, ime_festivala, kolicina, cena_prej, cena_skupaj, popust)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', [id_festival, ime_festivala, kolicina, cena, cena_skupaj, popust])
        # odštejejo se kupljene vstopnice
        cur.execute('''UPDATE festival SET st_prodanih_festival = ?''', [st_prodanih_festival + kolicina])

    if stevilo_vstopnic >= kolicina:
        cena_skupaj = cena * kolicina * (1 - popust/100)
        # vstopnica je prodana
        cur.execute('''INSERT INTO Vstopnice (id_festivala, ime_festivala, kolicina, cena_prej, cena_skupaj, popust)
                        VALUES (?, ?, ?, ?, ?, ?)''', [id_festival, ime_festivala, kolicina, cena, cena_skupaj, popust])
        # prištejemo prodane vstopnice
        cur.execute('''UPDATE festival SET st_prodanih_festival = ? WHERE id = ?''', [st_prodanih_festival + kolicina, id_festival])
    cur.close()
    return id

def izdaj_vstopnico_nastop(id_nastopa, kolicina, popust = 0):
    '''Vstopnica za nastop.'''
    # popust je v odstotkih
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

    # koliko je vseh vstopnic
    cur.execute('''SELECT stevilo_vstopnic FROM festival WHERE id = ?''', [id_festival])
    rez1 = cur.fetchone()

    stevilo_vstopnic = rez1[0]

    cur.execute('''SELECT st_prodanih_festival FROM festival WHERE id = ?
              ''', [id_nastopa])
    rez2 = cur.fetchone()
    if rez2 is None:
        raise Exception('Ni tega festivala.')
    else:
        st_prodanih_festival = rez2[0]

    # preštejemo število nastopov na festivalu, za katerega izdajamo vstopnico
    cur.execute('''SELECT COUNT(id) FROM nastopi WHERE id_festival = ?
              ''', [id_festival])
    st_nastopov = cur.fetchone()
    st_nastopov = st_nastopov[0]

    # cena festivala za katerega izdajamo vstopnico
    cur.execute('''SELECT cena FROM festival WHERE id = ?''', [id_festival])
    rez3 = cur.fetchone()
    cena = rez3[0]/ st_nastopov
    
    if st_prodanih_festival + st_prodanih_nastop + kolicina <= stevilo_vstopnic:
        cena_skupaj = cena * kolicina * (1 - popust/100)
        # vstopnica je prodana
        cur.execute('''INSERT INTO vstopnice_nastopi (cena_prej, popust, cena_skupaj, id_nastop, stevilo)
                        VALUES (?, ?, ?, ?, ?)''', [cena, popust, cena_skupaj, id_nastopa, kolicina])
        # prištejejo se kupljene vstopnice
        cur.execute('''UPDATE nastopi SET st_prodanih_nastop = ? WHERE id = ?''', [st_prodanih_nastop + kolicina, id_nastopa])
    cur.close()
    return id


def zakodiraj(geslo):
    '''Zakodiramo dano geslo.'''
    return hashlib.md5(geslo.encode()).hexdigest()

def preveri_geslo(uporabnisko_ime, geslo):
    '''Preverimo, če je v bazi uporabnik s podanim uporabniškim imenom in geslom'''
    with baza:
        baza.execute('''SELECT id FROM uporabniki WHERE uporabnisko_ime = ? AND geslo = ?''', [uporabnisko_ime, zakodiraj(geslo)])
        id_uporabnika = baza.fetchone()
        if id_uporabnika is None: 
            raise Exception('Vnešeno uporabniško ime ali geslo je napačno.')
        
def dodaj_uporabnika(uporabnisko_ime, geslo):
    '''V bazo dodamo uporabnika, to pomeni njegovo uporabniško ime in zakodirano geslo'''
    cur = baza.cursor()
    cur.execute('''INSERT INTO uporabniki (uporabnisko_ime, geslo) VALUES (?, ?)''', [uporabnisko_ime, zakodiraj(geslo)])
    cur.close()
    # dobi zadnji id
    id_uporabnika = cur.lastrowid 
    return id_uporabnika

def dodaj_komentar(komentar, uporabnisko_ime):
    '''V bazo dodamo komentar.'''
    cur = baza.cursor()
    cur.execute('''INSERT INTO komentarji (komentar, uporabnisko_ime) VALUES (?, ?)''', [komentar, uporabnisko_ime])
    cur.close()
    id_komentar = cur.lastrowid
    return id_komentar
        

    
baza = sqlite3.connect(datoteka_baze, isolation_level = None)
