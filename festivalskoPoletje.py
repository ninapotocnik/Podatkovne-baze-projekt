import sqlite3
import hashlib

datoteka_baze = 'festivalskoPoletje.sqlite3'

def iskanje(ime = None, lokacija = None, min_cena = None, max_cena = None, min_datumZ = None, max_datumZ = None, min_datumK = None, max_datumK = None):
    cur = baza.cursor()
    cur.execute('''SELECT festival.id, festival.ime FROM festival JOIN nastopi ON festival.id = nastopi.id_festival
              JOIN glasbeniki ON nastopi.id_glasbenik = glasbeniki.id
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
    # popust je v odstotkih
    #with baza:
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
        cur.execute('''INSERT INTO Vstopnice (cena_prej, popust, cena_skupaj, id_festival,  ime, kolicina)
                        VALUES (?, ?, ?, ?, ?, ?, ?)''', [cena, popust, cena_skupaj, id_festival, kolicina])
        # odštejejo se kupljene vstopnice
        cur.execute('''UPDATE festival SET stevilo_vstopnic = ?''', [st_prodanih_festival + kolicina])
    if stevilo_vstopnic >= kolicina:
        cena_skupaj = cena * kolicina * (1 - popust/100)
        # vstopnica je prodana
        cur.execute('''INSERT INTO Vstopnice (id_festivala, ime_festivala, kolicina, cena_prej, cena_skupaj, popust)
                        VALUES (?, ?, ?, ?, ?, ?)''', [id_festival, ime_festivala, kolicina, cena, cena_skupaj, popust])
        # prištejemo prodane vstopnice
        cur.execute('''UPDATE festival SET st_prodanih_festival = ?''', [st_prodanih_festival + kolicina])
    cur.close()
    return id

def izdaj_vstopnico_nastopi(id_nastopa, kolicina, popust = 0):
    # popust je v odstotkih
    with baza:
        baza.execute('''SELECT st_prodanih_nastop, st_vstopnic_na_voljo FROM nastopi WHERE id = ?
                  ''', [id_nastopa])
        rez = baza.fetchone()
        if rez is None:
            raise Exception("Ni tega nastopa.")
        else:
            (st_prodanih_nastop, st_vstopnic_na_voljo) = rez

        baza.execute('''SELECT st_prodanih_festival FROM festival WHERE id = ?
                  ''', [id_festival])
        re1 = baza.fectone()
        if rez1 is None:
            raise Exception('Ni tega festivala.')
        else:
            st_prodanih_festival = rez1
        
        if st_prodanih_festival + st_prodanih_nastopi + kolicina <= st_vstopnic_na_voljo:
            cena_skupaj = cena * kolicina * (1 - popust/100)
            # vstopnica je prodana
            baza.execute('''INSERT INTO vstopnica_nastopi (cena_prej, popust, cena_skupaj, nastop_id, stevilo)
                            VALUES (?, ?, ?, ?, ?)''', [cena, popust, cena_skupaj, id_nastopa, kolicina])
            # odštejejo se kupljene vstopnice
            baza.execute('''UPDATE nastopi SET stevilo_vstopnic = ?''', [st_prodanih_nastop + kolicina])

        return id


def zakodiraj(geslo):
    return hashlib.md5(geslo.encode()).hexdigest()

def preveri_geslo(uporabnisko_ime, geslo):
    '''Preveri če je v bazi uporabnik z podanim uporabniškim imenom in podanim geslom'''
    with baza:
        baza.execute('''SELECT id FROM uporabniki WHERE uporabnisko_ime = ? AND geslo = ?''', [uporabnisko_ime, zakodiraj(geslo)])
        id_uporabnika = baza.fetchone()
        if id_uporabnika is None: 
            raise Exception('Vnešeno uporabniško ime ali geslo je napačno.')
        
def dodaj_uporabnika(uporabnisko_ime, geslo):
    '''V bazo dodamo uporabnika: njegovo uporabniško ime in zakodirano geslo'''
    cur = baza.cursor()
    cur.execute('''INSERT INTO uporabniki (uporabnisko_ime, geslo) VALUES (?, ?)''', [uporabnisko_ime, zakodiraj(geslo)])
    cur.close()
    id_uporabnika = cur.lastrowid #dobi zadnji id
    return id_uporabnika

def dodaj_komentar(komentar, uporabnisko_ime):
    cur = baza.cursor()
    cur.execute('''INSERT INTO komentarji (komentar, uporabnisko_ime) VALUES (?, ?)''', [komentar, uporabnisko_ime])
    cur.close()
    id_komentar = cur.lastrowid
    return id_komentar
        

    
baza = sqlite3.connect(datoteka_baze, isolation_level = None)
