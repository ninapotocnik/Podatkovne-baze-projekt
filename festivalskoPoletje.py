import sqlite3

datoteka_baze = 'festivalskoPoletje.sqlite3'

def iskanje(ime, lokacija, min_cena, max_cena, min_datum, max_datum):
    c = baza.cursor()
    c.execute('''SELECT id, ime FROM festival JOIN nastopi ON festival.id = id_festival
              JOIN glasbeniki ON id_glasbenik = glasbeniki.id
              WHERE (festival.ime LIKE ? OR glasbeniki.ime LIKE ?)
              AND lokacija LIKE ?
              AND cena IS BETWEEN ? AND ?
              AND datum IS BETWEEN ? AND ?''', [ime, ime, lokacija, min_cena, max_cena, min_datum, max_datum])
    ime = c.fetchall()
    c.close()
    return ime

def vstopnice():
    c = baza.cursor()
    c.execute('''SELECT id FROM festival ''')
    c.close()
baza = sqlite3.connect(datoteka_baze, isolation_level = None)
