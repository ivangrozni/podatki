 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from lxml import etree
import urllib2#, datetime
import random
import re
import socket
import time # da se malce postopa, koliko casa traja zajem...

timeout = 5 # seconds
socket.setdefaulttimeout(timeout)

def vzorec(n, ime="test.txt", vec_podatkov = True):
    """Vrne datoteko s podatki o n filmih
    Input: n - stevilo filmov; ime - ime datoteke z bazo filmov (ustvari se nova datoteka)
    vec_podatkov - Ce je True, mora film imeti cas trajanja in imdb rating, da se zapise v datoteko.
    Output: Datoteka s filmi (za obdelavo v R)"""
    ti = time.time()
    f = open(ime, 'w')
    f.write("#ID\timdbID\tletnica\tduration\timdbRating\tnr_users\tgross\tbudget\tnr_reviews\tnr_critics\tmetascore\tnr_metacritics\tdrzava\tzanr\tnaslov\n")
    i = j = nf = 0 # stevec, stevec ne filmov, stevec filmov brez podatkov
    while i<n:
        index = kandidat_str()
        print index
        film = zajem(index)
        if preveri_film(film):
            nf += 1
            p = podatki_filma(film)
            if vec_podatkov:
                #if p[3] != "None" and p[5] != "None" and p[8] != "None": #Mora imeti cas trajanja in rating
                if "None" not in p:
                    try:
                        f.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (i+1, index, p[1], p[3], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[2], p[4], p[0]) )
                        i += 1
                        print " film s podatki: %s\t, %s\ti: %d" % (p[0], p[1], i)
                        #print "pregledanih: ", j, "nefilmov: ", j-n, "delez filmov: ", n*1.0/j, "filmi brez podatkov: ", nf - n, "delez filmov s podatki: ", n*1.0/nf
                    except UnicodeEncodeError: # Tezava je v budget in gross za drzave s cudnimi valutami
                        print "film po gobe"
                else: print " film brez podatkov: %s\t%s" % (p[0], p[1])
            else:
                try:
                    f.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (i+1, index, p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[0]) )
                    i += 1
                except UnicodeEncodeError: # Tezava je v budget in gross za drzave s cudnimi valutami
                    print "film po gobe"
                
        j += 1
        
    f.close()
    ti = time.time() - ti
    return "pregledanih: ", j, "nefilmov: ", j-nf, "delez filmov: ", n*1.0/j, "filmi brez podatkov: ", nf - n, "delez filmov s podatki: ", n*1.0/nf, "cas: ", ti

def kandidat_str():
    kandidat=random.randint(1, 2400000)
    kandidat="0"*(7-st_mest(kandidat)) + str(kandidat)
    return kandidat
    
def st_mest(n):
    i=1
    while n/(10) != 0:
        i+=1
        n = n/10
    return i

def zajem(index):
    """Pogleda ali je naslov www.imdb.com/tt[index] film in zajame podatke; index = 0096256"""
    try: #if len(index) == 7 and isinstance(index, basestring):
        movieURL = "http://www.imdb.com/title/tt%s/"%index
        req = urllib2.Request(movieURL)
        resp = urllib2.urlopen(req)
        the_page = resp.read()
        #root = etree.HTML(movie)
        root = etree.HTML(the_page) # Mogoce bi to moralo biti ze prej...
        return root # String s stranjo
    except urllib2.HTTPError:
        print "HTTPError"
        return etree.HTML("<html>404</html>") #:)
    except socket.timeout:
        print "socket.timeout"
        return etree.HTML("<html>404</html>") #:)

def preveri_film(root): # FILM MORA TUDI BITI KONCAN!!!
    """"Preveri, ali je stran (z danim indexom) stran s filmom"""
    I = root.findall(".//i")
    for i in I:
        if i.text == "in development,": return False
    A = root.findall(".//a[@href]")
    for a in A:
        if a.text == "Not yet released": return False
    META = root.findall(".//meta[@content]")  #[3].get("content") #print meta
    for meta in META:
        if meta.get("content") ==  "video.movie": return True
    return False

def podatki_filma(root):
    """Poisce podatke:"""
    str_budget = str_gross = str_meta = False
    str_genre = str_rating = str_duration = str_drzava = str_review = str_critics = ''
    # OSNOVNI PODATKI
    META = root.findall(".//meta[@content]")#[5].get("content") ## naslov in letnica
    for meta in META:
        str_naslov = meta.get("content")
        #if re.search("[0-9]{4}", str_naslov): break
        if meta.get("property") == "og:title":
            str_naslov = meta.get("content")
            break
        else: str_naslov = "None"####################
    DIV = root.findall(".//div[@title]")#[0].get("title") ## rating, st_users
    for div in DIV:
        str_rating = div.get("title")
        if re.match("Users", str_rating): break
        else: str_rating = ''
    span = root.findall(".//span[@itemprop]") ## st_review, st_critic, genre
    for s in span: 
        if s.get("itemprop") == "reviewCount":
            str_review = str_review + s.text + "\n"
        elif s.get("itemprop") == "genre":
            str_genre += (' ' + s.text) # !!! append !!!
    TIME  = root.findall(".//time[@itemprop]")# runtime...kaj naredi, ce je vec runtimov?
    for time in TIME:
        if time.get("itemprop") == "duration":
            str_duration = time.text
            break
    DIV=root.findall(".//div[@class]") # print len(DIV)
    for div in DIV: ## budget, gross, drzava(pri release date)
        if div.get("class") == "txt-block":
            for child in div:
                if child.tag == "h4":
                    if child.text == "Budget:":
                        str_budget = child.tail
                    elif child.text == "Gross:":
                        str_gross = child.tail
                        break
    
                    
    A=root.findall(".//a[@href]") # metascore, nr_metcritics
    str_meta = ''
    for a in A:
        if a.get("href") == "criticreviews?ref_=tt_ov_rt":
            str_meta =  str_meta + a.text
        if re.match("/country/", a.get("href") ): # se spreminja!!!
            str_drzava = a.text

    #naslov, letnica = re.split("\(", str_naslov)
    naslov = re.sub(" \([0-9]{4}\)", '', str_naslov)
    letnica = re.search("[0-9]{4}", str_naslov).group(0) 

    if len(str_rating) != 0 and re.search("[0-9]+", str_rating):
        str_rating = re.split(" ", str_rating)
        rating = re.split("/", str_rating[3])[0]
        nr_users = re.sub("\(", "", str_rating[4])
    else: rating = nr_users = "None"
    if len(str_duration) != 0: duration = re.sub(" min|\s", "", str_duration)
    else: duration = "None"
    if len(str_drzava) != 0: drzava = re.sub("\s", '', str_drzava)#re.sub(" min", "", str_duration)
    else: drzava = "None"
    if len(str_genre) != 0: genre = re.split(" ", str_genre)[1]
    else: genre = "None"
    if str_budget != False:budget = re.sub("$|[a-zA-Z]+|\(|,|\)|\s", "", str_budget)
    else: budget = "None"
    if str_gross != False: gross = re.sub("$|[a-zA-Z]+|\(|,|\)|\s", "", str_gross)
    else: gross = "None"
    if len(str_review) != 0:
        review = re.split(" ", str_review)
        nr_reviews = review[0]
        nr_critics = re.split("\n", review[1])[1]
 #nr_reviews = re.split(" ", str_review)[0]
    else:
        nr_reviews = "None"
        nr_critics = "None"
    if str_meta != False and len(str_meta) > 2: #         print str_meta
    #if len(str_meta) > 2: #         print str_meta
        str_meta = re.split("\n", str_meta)
        metascore = re.sub("\s", "",  re.split("/", str_meta[0])[0] )
        nr_metacritic = re.sub("\s", "", str_meta[1])
        #print metascore, nr_metacritic
    else:
        metascore = nr_metacritic = "None"

    #print naslov 0, letnica 1, str_drzava 2, duration 3, genre 4, rating 5, nr_users 6, budget 7, gross 8, nr_reviews 9, nr_critics 10, metascore 11, nr_metacritic 12
    return naslov.encode('UTF-8'), letnica.encode('UTF-8'), drzava.encode('UTF-8'), duration.encode('UTF-8'), genre.encode('UTF-8'), rating.encode('UTF-8'), nr_users.encode('UTF-8'), budget.encode('UTF-8'), gross.encode('UTF-8'), nr_reviews.encode('UTF-8'), nr_critics.encode('UTF-8'), metascore.encode('UTF-8'), nr_metacritic.encode('UTF-8')


# Izkaze se, da z nakljucnim iskanjem filmov, ne najdes nicesar - domislil sem se drevesnega nacina iskanja filmov. Zacnes z nekim imdbID-jem in pogledas, kateri filmi so bili vsec ljudem, ki jim je bil vsec ta film. In tako naprej v narobe obrnjeno drevo.

# zajem se je ze zgodil
def also_like(root):
    """Vrne filme, ki so jih bili vsec ljudem, ki jim je bil vsec ta film"""
    DIV = root.findall(".//div[@data-tconst]")#[5].get("content") ## naslov in letnica
    seznam = []
    for div in DIV:
        s = div.get("data-tconst")
        imdbID = int(re.sub("tt", "", s))
        if imdbID not in seznam: seznam.append(imdbID)
    return seznam


def drevo_zajem(n, seznam, SEZNAM, N = 1000, ime = "drevo.txt"): # Tukaj bi se dalo kaj rekurzivnega sfurat
    """N - omejitev stevila filmov, seznam - filmi za pregledat, SEZNAM - ze pregledani filmi
    Output: #Seznam filmov v drevesu - Bi si zelel - je pa samo file s podatki filmov
    """
    #SEZNAM = [startID] # kateri filmi so sedaj za preverit
    #seznam = [] # kateri filmi bodo za preverit pol
    i = 0
    SEZ = []
    f = open(ime, 'a')
    #f.write("#ID\timdbID\tletnica\tduration\timdbRating\tnr_users\tgross\tbudget\tnr_reviews\tnr_critics\tmetascore\tnr_metacritics\tdrzava\tzanr\tnaslov\toce\n") # oceta ne bo...
    for index in seznam:
        if index not in SEZNAM: # Ce ga se nisem zapisal
            root = zajem(index)
            p = podatki_filma(root)
            sez = also_like(root)
            try:
                f.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (n+i+1, index, p[1], p[3], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[12], p[2], p[4], p[0]) )
                i += 1
                print "%d film s podatki: %s\t, %s\ti: %d, %d" % (index, p[0], p[1], i, n+i)
            except UnicodeEncodeError: # Tezava je v budget in gross za drzave s cudnimi valutami
                print "film po gobe"
            for imdbID in sez:
                if imdbID not in SEZ: SEZ.append(imdbID)
    n += i
    SEZNAM += seznam
    if n > N:
        f.write("#ID\timdbID\tletnica\tduration\timdbRating\tnr_users\tgross\tbudget\tnr_reviews\tnr_critics\tmetascore\tnr_metacritics\tdrzava\tzanr\tnaslov\toce\n") # oceta ne bo... Z DICTIONARYJEM bi lahko bil
        f.close()
        return "Nasel N filmov"
    else:
        f.close()
        drevo_zajem(n, SEZ, SEZNAM, N, ime)


#ID    imdbID    naslov    letnica    drzava    runtime    zanr    budget   gross    rating    nr_users    metascore    nr_reviews    nr_critics    nr_metacritic    nr_fb

# IF SOCKET DOES NOT WORK!
#import signal
#...
#def handler(signum, frame):
#    print 'Signal handler called with signal', signum
#...
#signal.signal(signal.SIGALRM, handler)
#...
#signal.alarm(5)
#response = urllib2.urlopen(request)
#signal.alarm(0) # Disable the signal
         
