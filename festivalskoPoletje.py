import sqlite3

datoteka_baze = 'festivalskoPoletje.sqlite3'

def iskanje(ime, lokacija, min_cena, max_cena, min_datum, max_datum):
    with baza:
        baza.execute('''SELECT id, ime FROM festival JOIN nastopi ON festival.id = id_festival
                  JOIN glasbeniki ON id_glasbenik = glasbeniki.id
                  WHERE (festival.ime LIKE ? OR glasbeniki.ime LIKE ?)
                  AND lokacija LIKE ?
                  AND cena IS BETWEEN ? AND ?
                  AND datum IS BETWEEN ? AND ?''', [ime, ime, lokacija, min_cena, max_cena, min_datum, max_datum])
        return baza.fetchall()

def izdaj_vstopnico_festival(id_festivala, kolicina, popust = 0):
    # popust je v odstotkih
    with baza:
        baza.execute('''SELECT cena, stevilo_vstopnic FROM festival WHERE id = ?
                  ''', [id_festivala])
        if stevilo_vstopnic >= kolicina:
            cena_skupaj = cena * kolicina * (1 - popust/100)
            # vstopnica je prodana
            baza.execute('''INSERT INTO Vstopnica (datum_zacetek, datum_konec, cena_prej, popust, cena_skupaj, ime, kolicina)
                            VALUES (?, ?, ?, ?, ?, ?, ?)''', [cena, popust, cena_skupaj, id_festival, kolicina])
            # odštejejo se kupljene vstopnic
            baza.execute('''UPDATE festivali SET stevilo_vstopnic = ?''', [stevilo_vstopnic - kolicina])
        return id

def izdaj_vstopnico_nastopi(id_nastopa, kolicina, popust = 0):
    # popust je v odstotkih
    with baza:
        baza.execute('''SELECT stevilo_vstopnic FROM festival WHERE id = ?
                  ''', [id_festivala])
        # ce je stevilo vstopnic, za nastop manjše od festivala..pol ok, èe ne ne gre -> popust
        baza.execute('''SELECT cena, stevilo_vstopnic FROM nastopi WHERE id = ?
                  ''', [id_nastopi])
        if stevilo_vstopnic >= kolicina:
            cena_skupaj = cena * kolicina * (1 - popust/100)
            # vstopnica je prodana
            baza.execute('''INSERT INTO vstopnica_nastopi (cena_prej, popust, cena_skupaj, nastop_id, stevilo)
                            VALUES (?, ?, ?, ?, ?)''', [cena, popust, cena_skupaj, id_nastopa, kolicina])
            # odštejejo se kupljene vstopnic
            baza.execute('''UPDATE nastopi SET stevilo_vstopnic = ?''', [stevilo_vstopnic - kolicina])
        return id
    
baza = sqlite3.connect(datoteka_baze, isolation_level = None)
