 #!/usr/bin/python
 # -*- coding: utf-8 -*-
from lxml import etree
import urllib2#, datetime
import random
import re

def vzorec(n, ime="test.txt"):
    """Vrne datoteko s podatki o n filmih"""
    f = open(ime, 'w')
    f.write("#ID\timdbID\tnaslov\tletnica\tdrzava\tduration\tzanr\timdbRating\tnr_users\tgross\tbudget\tnr_reviews\tmetascore\tnr_metacritics\n")
    i = j = 0
    while i<n:
        index = kandidat_str()
        print index
        film = zajem(index)
        if preveri_film(film):
            p = podatki_filma(film)
            try:
                f.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (i+1, index, p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11], p[0]) )
                i += 1
            except UnicodeEncodeError: # Tezava je v budget in gross za drzave s cudnimi valutami
                print "film po gobe"
        j += 1
        
    f.close()
    return "pregledanih: ", j, "nefilmov: ", j-n, "delez: ", n*1.0/j

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
        return the_page # String s stranjo
    except urllib2.HTTPError:
        return "<html>404</html>" #:)

def preveri_film(the_page): # FILM MORA TUDI BITI KONCAN!!!
    """"Preveri, ali je stran (z danim indexom) stran s filmom"""
    root = etree.HTML(the_page) # Mogoce bi to moralo biti ze prej...
    META = root.findall(".//meta[@content]")  #[3].get("content") #print meta
    A = root.findall(".//a[@href]")
    for a in A:
        if a.text == "Not yet released": return False
    for meta in META:
        if meta.get("content") ==  "video.movie": return True
    return False

def podatki_filma(the_page):
    """Poisce podatke:"""
    parser = etree.HTMLParser(remove_blank_text=True)
    root = etree.HTML(the_page, parser) # Mogoce bi to moralo biti ze prej...
    
    str_budget = str_gross = str_review = str_meta = False
    str_genre = str_rating = str_duration = ''
    # OSNOVNI PODATKI
    str_naslov = root.findall(".//meta[@content]")[5].get("content") ## naslov in letnica
    str_rating = root.findall(".//div[@title]")[0].get("title") ## rating, st_users
    
    span = root.findall(".//span[@itemprop]") ## st_review, st_critic, genre
    for s in span: 
        if s.get("itemprop") == "reviewCount": str_review = s.text
        if s.get("itemprop") == "genre": str_genre += (' ' + s.text) # !!! append !!!
    TIME  = root.findall(".//time[@itemprop]")# runtime...kaj naredi, ce je vec runtimov?
    for time in TIME:
        if time.get("itemprop") == "duration": str_duration = time.text
    DIV=root.findall(".//div[@class]") # print len(DIV)
    for div in DIV: ## budget, gross, drzava(pri release date)
        if div.get("class") == "txt-block":
            for child in div:
                if child.tag == "h4":
                    if child.text == "Budget:": str_budget = child.tail
                    elif child.text == "Gross:": str_gross = child.tail
                    
    A=root.findall(".//a[@href]") # metascore, nr_metcritics
    str_meta = ''
    for a in A:
        if a.get("href") == "criticreviews?ref_=tt_ov_rt":
            str_meta =  str_meta + a.text
        if re.match("/country/", a.get("href") ): # se spreminja!!!
            str_drzava = a.text

        
    #print str_naslov, str_date, str_genre, str_duration, str_rating
    #print str_budget, str_gross, str_review, str_meta
    naslov, letnica = re.split("\(", str_naslov)
    letnica = re.search("[0-9]{4}", str_naslov).group(0)  #letnica = re.sub("\)", "", letnica) #print str_naslov, naslov, letnica
    #drzava = re.sub( "\)|\s+", "",  re.split("\(", str_date)[1])
    if len(str_rating) != 0 and re.search("[0-9]+", str_rating):
        str_rating = re.split(" ", str_rating)
        rating = re.split("/", str_rating[3])[0]
        nr_users = re.sub("\(", "", str_rating[4])
    else: rating = nr_users = "None"
    if len(str_duration) != 0: duration = re.sub(" min", "", str_duration)
    else: duration = "None"
    if len(str_genre) != 0: genre = re.split(" ", str_genre)[1]
    else: genre = "None"
    if str_budget != False: budget = re.sub("$|[a-zA-Z]+|\(|,|\)|\s", "", str_budget)
    else: budget = "None"
    if str_gross != False: gross = re.sub("$|[a-zA-Z]+|\(|,|\)|\s", "", str_gross)
    else: gross = "None"
    if str_review != False: nr_reviews = re.split(" ", str_review)[0]
    else: nr_reviews = "None"
    if str_meta != False and len(str_meta) > 2:
        print str_meta
        str_meta = re.split("\n", str_meta)
        metascore = re.sub("\s", "",  re.split("/", str_meta[0])[0] )
        nr_metacritic = re.sub("\s", "", str_meta[1])
    else: metascore = nr_metacritic = "None"

    #print naslov, letnica, str_drzava, duration, genre, rating, nr_users, budget, gross, nr_reviews, metascore, nr_metacritic
    return naslov.encode('UTF-8'), letnica.encode('UTF-8'), str_drzava.encode('UTF-8'), duration.encode('UTF-8'), genre.encode('UTF-8'), rating.encode('UTF-8'), nr_users.encode('UTF-8'), budget.encode('UTF-8'), gross.encode('UTF-8'), nr_reviews.encode('UTF-8'), metascore.encode('UTF-8'), nr_metacritic.encode('UTF-8')


def zajemi_vse(n):
    """zajame n filmov in njihove podatke zapise v fajl"""
    pass


#ID    imdbID    naslov    letnica    drzava    runtime    zanr    budget   gross    rating    nr_users    metascore    nr_reviews    nr_critics    nr_metacritic    nr_fb

         
