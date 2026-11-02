"""Generates races.json for the RaceCalendar app.

Sources (checked Nov 2026): UCI 2027 WorldTour / Women's WorldTour calendars,
2026-27 UCI Cyclo-cross World Cup calendar, 2027 Haute-Savoie Worlds programme,
2026 broadcast-rights guides (Domestique, Cyclingnews, Escape Collective, Flashscore).
Broadcast info reflects 2026 rights and should be re-checked as 2027 deals are announced.
"""
import json, re

# ---- places: name -> (lat, lon) -------------------------------------------
P = {
    "Adelaide": (-34.9285, 138.6007), "Geelong": (-38.1499, 144.3617),
    "Abu Dhabi": (24.4539, 54.3773), "Ghent": (51.0543, 3.7174), "Ninove": (50.8280, 4.0250),
    "Siena": (43.3188, 11.3308), "Pavia": (45.1847, 9.1582), "Sanremo": (43.8159, 7.7761),
    "Barcelona": (41.3874, 2.1686), "Bruges": (51.2093, 3.2247), "Harelbeke": (50.8556, 3.3089),
    "Middelkerke": (51.1852, 2.8195), "Wevelgem": (50.8104, 3.1823), "Roeselare": (50.9465, 3.1228),
    "Waregem": (50.8893, 3.4269), "Oudenaarde": (50.8456, 3.6061), "Bilbao": (43.2630, -2.9350),
    "Compiègne": (49.4179, 2.8261), "Roubaix": (50.6942, 3.1746), "Maastricht": (50.8514, 5.6910),
    "Berg en Terblijt": (50.8597, 5.7861), "Huy": (50.5182, 5.2394), "Liège": (50.6326, 5.5797),
    "Lausanne": (46.5197, 6.6323), "Eschborn": (50.1436, 8.5696), "Frankfurt": (50.1109, 8.6821),
    "Rome": (41.9028, 12.4964), "Lyon": (45.7640, 4.8357), "Copenhagen": (55.6761, 12.5683),
    "Zurich": (47.3769, 8.5417), "Edinburgh": (55.9533, -3.1883), "Paris": (48.8566, 2.3522),
    "San Sebastián": (43.3183, -1.9812), "Kraków": (50.0647, 19.9450), "Hamburg": (53.5511, 9.9937),
    "Antwerp": (51.2194, 4.4025), "Plouay": (47.9150, -3.3350), "Madrid": (40.4168, -3.7038),
    "Québec City": (46.8139, -71.2080), "Montréal": (45.5019, -73.5674), "Como": (45.8081, 9.0852),
    "Bergamo": (45.6983, 9.6773), "Nanning": (22.8170, 108.3665), "Cittiglio": (45.8950, 8.6670),
    "Vitoria-Gasteiz": (42.8467, -2.6716), "Burgos": (42.3439, -3.6969), "Lorient": (47.7486, -3.3700),
    "Chongming Island": (31.6230, 121.3970), "Sallanches": (45.9360, 6.6320),
    "Annecy": (45.8992, 6.1294), "Ostrava": (49.8209, 18.2625), "Tábor": (49.4144, 14.6578),
    "Glasgow": (55.8642, -4.2518), "Koksijde": (51.1167, 2.6383), "Gavere": (50.9290, 3.6610),
    "Namur": (50.4674, 4.8720), "Besançon": (47.2378, 6.0241), "Zonhoven": (50.9910, 5.3690),
    "Benidorm": (38.5411, -0.1225), "Hamme": (51.0990, 4.1370), "Hoogerheide": (51.4240, 4.3260),
    "Oostende": (51.2154, 2.9286), "Zeddam": (51.9030, 6.2600), "Leuven": (50.8798, 4.7005),
    "Wroclaw": (51.1079, 17.0385), "London": (51.5074, -0.1278),
    "Nové Město na Moravě": (49.5614, 16.0742), "Loudenvielle": (42.7960, 0.4080),
    "Leogang": (47.4386, 12.7611), "Les Gets": (46.1586, 6.6700), "La Thuile": (45.7130, 6.9520),
    "Pal Arinsal": (42.5640, 1.4870), "Lenzerheide": (46.7290, 9.5580), "Val di Sole": (46.3260, 10.8640),
    "Soldier Hollow": (40.4880, -111.5100), "Whistler": (50.1163, -122.9574),
}

def loc(name, role="venue"):
    lat, lon = P[name]
    return {"name": name, "role": role, "lat": lat, "lon": lon}

def sf(start, finish):
    if start == finish:
        return [loc(start, "start-finish")]
    return [loc(start, "start"), loc(finish, "finish")]

TBC_TRAD = "2027 route not announced yet; traditional start/finish shown."
TBC_STAGE = "2027 route not presented yet; host region shown. Stages will be added once announced."

# ---- broadcast rules (2026 rights) ------------------------------------------
US_BY_ORG = {
    "ASO": ["Peacock"],
    "RCS": ["HBO Max"],
    "Flanders Classics": ["FloBikes"],
    "UCI": ["FloBikes"],
}
US_CHECK = ["FloBikes (check listings)"]
ES_DEFAULT = ["Eurosport", "HBO Max"]
ES_RTVE = ["RTVE (Teledeporte / RTVE Play, free)"]

races = []

def add(id, name, gender, cat, start, end, cc, country, org, locations, note=None,
        discipline="road", es_rtve=False, us=None, es=None):
    watch_us = us or US_BY_ORG.get(org, US_CHECK)
    watch_es = es or ((ES_RTVE + ES_DEFAULT) if es_rtve else ES_DEFAULT)
    r = {
        "id": id, "name": name, "discipline": discipline, "gender": gender, "category": cat,
        "startDate": start, "endDate": end, "countryCode": cc, "country": country,
        "organizer": org, "locations": locations, "stages": [],
        "watch": {"US": watch_us, "ES": watch_es},
    }
    if note:
        r["locationNote"] = note
    races.append(r)

M, W = "men", "women"
WT, WWT = "UCI WorldTour", "UCI Women's WorldTour"

# ---------------------------- Men's WorldTour 2027 ---------------------------
add("tdu-m-2027", "Santos Tour Down Under", M, WT, "2027-01-19", "2027-01-24", "AU", "Australia", "Tour Down Under", [loc("Adelaide", "host")], TBC_STAGE)
add("cadel-m-2027", "Cadel Evans Great Ocean Road Race", M, WT, "2027-01-31", "2027-01-31", "AU", "Australia", "Other", sf("Geelong", "Geelong"))
add("uae-m-2027", "UAE Tour", M, WT, "2027-02-15", "2027-02-21", "AE", "United Arab Emirates", "RCS", [loc("Abu Dhabi", "host")], TBC_STAGE)
add("omloop-m-2027", "Omloop Nieuwsblad", M, WT, "2027-02-27", "2027-02-27", "BE", "Belgium", "Flanders Classics", sf("Ghent", "Ninove"), TBC_TRAD)
add("strade-m-2027", "Strade Bianche", M, WT, "2027-03-06", "2027-03-06", "IT", "Italy", "RCS", sf("Siena", "Siena"))
add("parisnice-2027", "Paris–Nice", M, WT, "2027-03-07", "2027-03-14", "FR", "France", "ASO", [loc("Paris", "start-region")], TBC_STAGE)
add("tirreno-2027", "Tirreno–Adriatico", M, WT, "2027-03-08", "2027-03-14", "IT", "Italy", "RCS", [loc("Rome", "host")], TBC_STAGE)
add("msr-m-2027", "Milano–Sanremo", M, WT, "2027-03-20", "2027-03-20", "IT", "Italy", "RCS", sf("Pavia", "Sanremo"), TBC_TRAD)
add("catalunya-2027", "Volta Ciclista a Catalunya", M, WT, "2027-03-22", "2027-03-28", "ES", "Spain", "Other", [loc("Barcelona", "finish")], TBC_STAGE, es_rtve=True)
add("brugge-m-2027", "Ronde van Brugge – Tour of Bruges", M, WT, "2027-03-24", "2027-03-24", "BE", "Belgium", "Flanders Classics", [loc("Bruges", "start-finish")], TBC_TRAD)
add("e3-2027", "E3 Saxo Classic", M, WT, "2027-03-26", "2027-03-26", "BE", "Belgium", "Other", sf("Harelbeke", "Harelbeke"), us=["FloBikes"])
add("gw-m-2027", "In Flanders Fields (Gent–Wevelgem)", M, WT, "2027-03-28", "2027-03-28", "BE", "Belgium", "Flanders Classics", sf("Middelkerke", "Wevelgem"))
add("dwars-m-2027", "Dwars door Vlaanderen", M, WT, "2027-03-31", "2027-03-31", "BE", "Belgium", "Flanders Classics", sf("Roeselare", "Waregem"), TBC_TRAD)
add("rvv-m-2027", "Ronde van Vlaanderen", M, WT, "2027-04-04", "2027-04-04", "BE", "Belgium", "Flanders Classics", sf("Bruges", "Oudenaarde"), TBC_TRAD)
add("itzulia-m-2027", "Itzulia Basque Country", M, WT, "2027-04-05", "2027-04-10", "ES", "Spain", "Other", [loc("Bilbao", "host")], TBC_STAGE, es_rtve=True)
add("roubaix-m-2027", "Paris–Roubaix", M, WT, "2027-04-11", "2027-04-11", "FR", "France", "ASO", sf("Compiègne", "Roubaix"))
add("amstel-m-2027", "Amstel Gold Race", M, WT, "2027-04-18", "2027-04-18", "NL", "Netherlands", "Flanders Classics", sf("Maastricht", "Berg en Terblijt"), TBC_TRAD)
add("fleche-m-2027", "La Flèche Wallonne", M, WT, "2027-04-21", "2027-04-21", "BE", "Belgium", "ASO", [loc("Huy", "finish")], "Finish on the Mur de Huy; 2027 start town not announced yet.")
add("lbl-m-2027", "Liège–Bastogne–Liège", M, WT, "2027-04-25", "2027-04-25", "BE", "Belgium", "ASO", sf("Liège", "Liège"))
add("romandie-m-2027", "Tour de Romandie", M, WT, "2027-04-27", "2027-05-02", "CH", "Switzerland", "Other", [loc("Lausanne", "host")], TBC_STAGE)
add("frankfurt-2027", "Eschborn–Frankfurt", M, WT, "2027-05-01", "2027-05-01", "DE", "Germany", "Other", sf("Eschborn", "Frankfurt"), "UCI listed 2 May in error; race keeps its traditional 1 May date.")
add("giro-m-2027", "Giro d'Italia", M, WT, "2027-05-08", "2027-05-30", "IT", "Italy", "RCS", [loc("Rome", "finish")], TBC_STAGE)
add("aura-2027", "Tour Auvergne – Rhône-Alpes", M, WT, "2027-06-06", "2027-06-13", "FR", "France", "ASO", [loc("Lyon", "host")], TBC_STAGE)
add("cph-m-2027", "Copenhagen Sprint", M, WT, "2027-06-13", "2027-06-13", "DK", "Denmark", "Other", [loc("Copenhagen", "finish")])
add("suisse-m-2027", "Tour de Suisse", M, WT, "2027-06-16", "2027-06-20", "CH", "Switzerland", "Other", [loc("Zurich", "host")], TBC_STAGE)
add("tdf-2027", "Tour de France", M, WT, "2027-07-02", "2027-07-25", "FR", "France", "ASO", [loc("Edinburgh", "start"), loc("Paris", "finish")], "Grand Départ in Edinburgh, Scotland. Full stage list comes with the route presentation.", es_rtve=True)
add("dssk-2027", "Donostia San Sebastián Klasikoa", M, WT, "2027-07-31", "2027-07-31", "ES", "Spain", "Other", sf("San Sebastián", "San Sebastián"), es_rtve=True)
add("pologne-2027", "Tour de Pologne", M, WT, "2027-08-02", "2027-08-08", "PL", "Poland", "Other", [loc("Kraków", "finish")], TBC_STAGE)
add("cyclassics-2027", "ADAC Cyclassics", M, WT, "2027-08-15", "2027-08-15", "DE", "Germany", "Other", sf("Hamburg", "Hamburg"), us=["FloBikes"])
add("renewi-2027", "Renewi Tour", M, WT, "2027-08-18", "2027-08-22", "BE", "Belgium", "Other", [loc("Antwerp", "host")], TBC_STAGE)
add("bretagne-2027", "Bretagne Classic – CIC", M, WT, "2027-08-22", "2027-08-22", "FR", "France", "Other", sf("Plouay", "Plouay"))
add("vuelta-m-2027", "La Vuelta Ciclista a España", M, WT, "2027-09-04", "2027-09-26", "ES", "Spain", "ASO", [loc("Madrid", "finish")], TBC_STAGE, es_rtve=True)
add("quebec-2027", "Grand Prix Cycliste de Québec", M, WT, "2027-09-10", "2027-09-10", "CA", "Canada", "Other", sf("Québec City", "Québec City"), us=["FloBikes"])
add("montreal-2027", "Grand Prix Cycliste de Montréal", M, WT, "2027-09-12", "2027-09-12", "CA", "Canada", "Other", sf("Montréal", "Montréal"), us=["FloBikes"])
add("lombardia-2027", "Il Lombardia", M, WT, "2027-10-09", "2027-10-09", "IT", "Italy", "RCS", sf("Como", "Bergamo"), "Start and finish alternate between Como and Bergamo; 2027 direction not announced yet.")
add("guangxi-2027", "Tour of Guangxi", M, WT, "2027-10-12", "2027-10-17", "CN", "China", "Other", [loc("Nanning", "host")], TBC_STAGE)

# ---------------------------- Women's WorldTour 2027 -------------------------
add("tdu-w-2027", "Santos Tour Down Under Women", W, WWT, "2027-01-22", "2027-01-24", "AU", "Australia", "Tour Down Under", [loc("Adelaide", "host")], TBC_STAGE)
add("cadel-w-2027", "Cadel Evans Great Ocean Road Race – Women", W, WWT, "2027-01-30", "2027-01-30", "AU", "Australia", "Other", sf("Geelong", "Geelong"))
add("uae-w-2027", "UAE Tour Women", W, WWT, "2027-02-03", "2027-02-06", "AE", "United Arab Emirates", "RCS", [loc("Abu Dhabi", "host")], TBC_STAGE)
add("omloop-w-2027", "Omloop Nieuwsblad Women", W, WWT, "2027-02-27", "2027-02-27", "BE", "Belgium", "Flanders Classics", sf("Ghent", "Ninove"), TBC_TRAD)
add("strade-w-2027", "Strade Bianche Donne", W, WWT, "2027-03-06", "2027-03-06", "IT", "Italy", "RCS", sf("Siena", "Siena"))
add("binda-2027", "Trofeo Alfredo Binda", W, WWT, "2027-03-14", "2027-03-14", "IT", "Italy", "Other", sf("Cittiglio", "Cittiglio"))
add("msr-w-2027", "Milano–Sanremo Women", W, WWT, "2027-03-20", "2027-03-20", "IT", "Italy", "RCS", sf("Pavia", "Sanremo"), TBC_TRAD)
add("brugge-w-2027", "Ronde van Brugge – Tour of Bruges Women", W, WWT, "2027-03-25", "2027-03-25", "BE", "Belgium", "Flanders Classics", [loc("Bruges", "start-finish")], TBC_TRAD)
add("gw-w-2027", "In Flanders Fields – Women", W, WWT, "2027-03-28", "2027-03-28", "BE", "Belgium", "Flanders Classics", [loc("Wevelgem", "finish")])
add("dwars-w-2027", "Dwars door Vlaanderen Women", W, WWT, "2027-03-31", "2027-03-31", "BE", "Belgium", "Flanders Classics", sf("Roeselare", "Waregem"), TBC_TRAD)
add("rvv-w-2027", "Ronde van Vlaanderen Women", W, WWT, "2027-04-04", "2027-04-04", "BE", "Belgium", "Flanders Classics", sf("Oudenaarde", "Oudenaarde"), TBC_TRAD)
add("roubaix-w-2027", "Paris–Roubaix Femmes", W, WWT, "2027-04-11", "2027-04-11", "FR", "France", "ASO", [loc("Roubaix", "finish")], "Finish in the Roubaix velodrome; 2027 start town not announced yet.")
add("amstel-w-2027", "Amstel Gold Race Ladies Edition", W, WWT, "2027-04-18", "2027-04-18", "NL", "Netherlands", "Flanders Classics", sf("Maastricht", "Berg en Terblijt"), TBC_TRAD)
add("fleche-w-2027", "La Flèche Wallonne Femmes", W, WWT, "2027-04-21", "2027-04-21", "BE", "Belgium", "ASO", [loc("Huy", "finish")])
add("lbl-w-2027", "Liège–Bastogne–Liège Femmes", W, WWT, "2027-04-25", "2027-04-25", "BE", "Belgium", "ASO", [loc("Liège", "finish")])
add("itzulia-w-2027", "Itzulia Women", W, WWT, "2027-05-14", "2027-05-16", "ES", "Spain", "Other", [loc("Vitoria-Gasteiz", "host")], TBC_STAGE, es_rtve=True)
add("burgos-w-2027", "Vuelta a Burgos Féminas", W, WWT, "2027-05-20", "2027-05-23", "ES", "Spain", "Other", [loc("Burgos", "host")], TBC_STAGE, es_rtve=True)
add("giro-w-2027", "Giro d'Italia Women", W, WWT, "2027-05-29", "2027-06-06", "IT", "Italy", "RCS", [loc("Rome", "host")], TBC_STAGE)
add("cph-w-2027", "Copenhagen Sprint Women", W, WWT, "2027-06-12", "2027-06-12", "DK", "Denmark", "Other", [loc("Copenhagen", "finish")])
add("suisse-w-2027", "Tour de Suisse Women", W, WWT, "2027-06-16", "2027-06-20", "CH", "Switzerland", "Other", [loc("Zurich", "host")], TBC_STAGE)
add("tdff-2027", "Tour de France Femmes avec Zwift", W, WWT, "2027-07-30", "2027-08-07", "FR", "France", "ASO", [loc("Paris", "host")], TBC_STAGE, es_rtve=True)
add("britain-w-2027", "Lloyds Tour of Britain Women", W, WWT, "2027-08-11", "2027-08-15", "GB", "Great Britain", "Other", [loc("London", "host")], TBC_STAGE)
add("lorient-2027", "Classic Lorient Agglomération", W, WWT, "2027-08-21", "2027-08-21", "FR", "France", "Other", sf("Lorient", "Lorient"))
add("romandie-w-2027", "Tour de Romandie Féminin", W, WWT, "2027-09-10", "2027-09-12", "CH", "Switzerland", "Other", [loc("Lausanne", "host")], TBC_STAGE)
add("chongming-2027", "Tour of Chongming Island", W, WWT, "2027-10-12", "2027-10-14", "CN", "China", "Other", [loc("Chongming Island", "host")], TBC_STAGE)

# ---------------------------- Worlds 2027 (Haute-Savoie) ---------------------
WORLDS_ES = ES_RTVE + ES_DEFAULT
add("worlds-rr-m-2027", "UCI Road World Championships – Men Elite Road Race", M, "World Championships", "2027-08-29", "2027-08-29", "FR", "France", "UCI", [loc("Annecy", "host")], "Part of the 2027 'Super Worlds' in Haute-Savoie Mont-Blanc (24 Aug–5 Sep). Exact course towns to be confirmed.", es=WORLDS_ES)
add("worlds-rr-w-2027", "UCI Road World Championships – Women Elite Road Race", W, "World Championships", "2027-09-05", "2027-09-05", "FR", "France", "UCI", [loc("Sallanches", "finish")], "Closing event of the 2027 Super Worlds, finishing in Sallanches-Domancy.", es=WORLDS_ES)

# ---------------------------- Cyclocross 2026-27 -----------------------------
CX_US = ["FloBikes", "HBO Max"]
CX_ES = ["RTVE (Teledeporte / RTVE Play, free)", "Eurosport", "HBO Max"]
cx = [
    ("Ostrava", "CZ", "Czechia", "2026-11-27", 1, "Night race at an old mine site."),
    ("Tábor", "CZ", "Czechia", "2026-11-29", 2, None),
    ("Glasgow", "GB", "Great Britain", "2026-12-13", 3, "Kelvingrove Park."),
    ("Antwerp", "BE", "Belgium", "2026-12-19", 4, None),
    ("Koksijde", "BE", "Belgium", "2026-12-20", 5, "The sand course."),
    ("Gavere", "BE", "Belgium", "2026-12-26", 6, None),
    ("Namur", "BE", "Belgium", "2026-12-27", 7, "Citadel of Namur."),
    ("Besançon", "FR", "France", "2026-12-29", 8, None),
    ("Zonhoven", "BE", "Belgium", "2027-01-03", 9, "The Kuil sand pit."),
    ("Benidorm", "ES", "Spain", "2027-01-17", 10, None),
    ("Hamme", "BE", "Belgium", "2027-01-23", 11, None),
    ("Hoogerheide", "NL", "Netherlands", "2027-01-24", 12, "GP Adrie van der Poel – World Cup finale."),
]
for town, cc, country, d, rnd, note in cx:
    slug = re.sub(r"[^a-z]", "", town.lower().replace("á", "a").replace("ç", "c").replace("é", "e"))
    for g in (M, W):
        add(f"cxwc-{slug}-{g}-2627", f"UCI Cyclo-cross World Cup #{rnd} – {town}", g, "UCI Cyclo-cross World Cup",
            d, d, cc, country, "Flanders Classics", [loc(town, "venue")], note,
            discipline="cx", us=CX_US, es=CX_ES)
for g in (M, W):
    add(f"cxeuro-{g}-2026", "UEC Cyclo-cross European Championships – Zeddam", g, "European Championships",
        "2026-11-08" if g == M else "2026-11-07", "2026-11-08" if g == M else "2026-11-07",
        "NL", "Netherlands", "UEC", [loc("Zeddam", "venue")], None, discipline="cx",
        us=US_CHECK, es=ES_DEFAULT)
    add(f"cxworlds-{g}-2027", "UCI Cyclo-cross World Championships – Oostende", g, "World Championships",
        "2027-01-29", "2027-01-31", "BE", "Belgium", "UCI", [loc("Oostende", "venue")],
        "Elite races on the final weekend; exact day per category to be confirmed.", discipline="cx",
        us=["FloBikes"], es=CX_ES)

# ---------------------------- Mountain bike 2027 ---------------------------
MTB_US = ["HBO Max"]
MTB_ES = ["Eurosport", "HBO Max"]
B = "all"
wc = [
    ("Nové Město na Moravě", "CZ", "Czechia", "2027-05-21", "2027-05-23", "xco"),
    ("Loudenvielle", "FR", "France", "2027-05-29", "2027-05-30", "dhi"),
    ("Leogang", "AT", "Austria", "2027-06-11", "2027-06-13", "both"),
    ("Les Gets", "FR", "France", "2027-06-18", "2027-06-20", "both"),
    ("La Thuile", "IT", "Italy", "2027-07-02", "2027-07-04", "both"),
    ("Pal Arinsal", "AD", "Andorra", "2027-07-09", "2027-07-11", "both"),
    ("Lenzerheide", "CH", "Switzerland", "2027-08-20", "2027-08-22", "both"),
    ("Val di Sole", "IT", "Italy", "2027-09-10", "2027-09-12", "both"),
    ("Soldier Hollow", "US", "United States", "2027-09-25", "2027-09-26", "xco"),
    ("Whistler", "CA", "Canada", "2027-10-02", "2027-10-03", "dhi"),
]
display = {"Loudenvielle": "Loudenvielle-Peyragudes", "Soldier Hollow": "Soldier Hollow, Utah"}
for town, cc, country, s_, e_, kinds in wc:
    slug = re.sub(r"[^a-z]", "", town.lower().encode("ascii", "ignore").decode())
    nm = display.get(town, town)
    if kinds in ("xco", "both"):
        add(f"mtb-xco-{slug}-2027", f"UCI MTB World Cup XCO/XCC – {nm}", B, "UCI MTB World Cup",
            s_, e_, cc, country, "WBD Sports", [loc(town, "venue")],
            "Short track (XCC) runs Friday, Olympic cross-country (XCO) at the weekend.",
            discipline="xco", us=MTB_US, es=MTB_ES)
    if kinds in ("dhi", "both"):
        add(f"mtb-dhi-{slug}-2027", f"UCI MTB World Cup Downhill – {nm}", B, "UCI MTB World Cup",
            s_, e_, cc, country, "WBD Sports", [loc(town, "venue")],
            "Qualifying earlier in the weekend, finals on the last day.",
            discipline="dhi", us=MTB_US, es=MTB_ES)
add("mtb-worlds-dhi-2027", "UCI MTB World Championships – Downhill", B, "World Championships",
    "2027-08-26", "2027-08-28", "FR", "France", "UCI", [loc("Les Gets", "venue")],
    "Part of the 2027 Super Worlds in Haute-Savoie.", discipline="dhi", us=["FloBikes"], es=WORLDS_ES)
add("mtb-worlds-xco-2027", "UCI MTB World Championships – Cross-country", B, "World Championships",
    "2027-08-30", "2027-09-04", "FR", "France", "UCI", [loc("Les Gets", "venue")],
    "Part of the 2027 Super Worlds in Haute-Savoie; XCO, XCC and team relay across the week.",
    discipline="xco", us=["FloBikes"], es=WORLDS_ES)

races.sort(key=lambda r: (r["startDate"], r["name"]))

data = {
    "schemaVersion": 2,
    "dataVersion": "2026-11-02",
    "broadcastNote": "Where-to-watch is based on 2026 broadcast rights and may change for 2027.",
    "viewingCountries": [{"code": "ES", "name": "Spain"}, {"code": "US", "name": "United States"}],
    "riders": [],
    "races": races,
}
json.dump(data, open("races.json", "w"), ensure_ascii=False, indent=1)
print(len(races), "races")
