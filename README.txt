29. jul 2013
Ljubljana

zajamemo N (~10 000) filmov
podatki:

ID    imdbID    naslov    reziser    letnica    drzava    runtime    zanr    budget   gross    rating    nr_users    metascore    nr_reviews    nr_critics    nr_metacritic    nr_fb

# drzava - 1. napisana
# zanr - 1. napisan

Resitev naloge za programiranje
Izberes vir podatkov na spletu (IMDB), zberes vsaj 1000 enot in njihove lastnosti
S pomocjo statisticnega programa R obdelaj podatke in napisi porocilo v LaTeXu

Uporabljena je koda prof. Batagela - pravzaprav ni.

1) Zajem podatkov - python, lxml

2) Obdelava - R

##############################

zajem_imdb.py

koncni cilj: ustvari datoteko, v kateri so zgoraj nasteti podatki

program prejme velikost vzorca (~10 000) in izbere toliko nakljucnih filmov


IMDb was launched on October 17, 1990, and in 1998 was acquired by Amazon.com. As of July 12, 2013 IMDb had 2,574,894 titles (includes episodes) and 5,318,849 personalities in its database,[3] as well as 45 million registered users. The website has an Alexa rank of 61.


##############################

NUJNI TO DO list:
      #1) Film po gobe: Unicode Encode Error  (treba je znake, ki jih ne zna kodirat z necim zamenjat) [SOLVED]

TO DO list
   1) Kodo naredi preglednejso
   2) Objektno programiranje
   3) Proper Error Handling
   4) Time - merjenje casa - koliko casa program dela...

##############################

Navodila za zajem_imdb.py:

Klices funkcijo vzorec(n), ki vrne datoteko z n filmi.
Manjkajoci podatki imajo vrednost None - veliko je manjkajocih podatkov :(

##############################

Dodal se malce errorHandlinga...
sockettimeout, ker se je program obesal...
