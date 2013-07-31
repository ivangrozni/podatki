from lxml import etree
import urllib2#, datetime
import random

def vzorec(n):
    """Vrne array n nakljucnih stevil (urejenih po veliksti?)"""
    seznam=[]
    i=0
    while i<n:
        kandidat=random.randint(1, 2500000)
        if preveri_film(kandidat):
            kandidat="0"*(7-st_mest(kandidat)) + str(kandidat)
            seznam+=kandidat
            i+=1
    return seznam
    
def st_mest(n):
    i=1
    while n//(10)^i!=0:
        i+=1
    return i


def zajem(index):
    """Pogleda ali je naslov www.imdb.com/tt[index] film in zajame podatke; index = 0096256"""
    if len(index) == 7 and isinstance(index, basestring):
        movieURL = "http://www.imdb.com/title/tt%s/"%index
        req = urllib2.Request(movieURL)
        resp = urllib2.urlopen(req)
        the_page = resp.read()
        #root = etree.HTML(movie)
        return the_page # String s stranjo
    else: return "index Ni prave oblike."

def preveri_film(the_page):
    """"Preveri, ali je stran (z danim indexom) stran s filmom"""
    root = etree.HTML(the_page)

    f, g = open('test_neurejeno.txt', 'w'), open('test_iter.txt', 'w')

    #f.write(etree.tostring(root))
    for element in root.iter():
        g.write("%s - %s" % (element.tag, element.text))
    
    f.close(); g.close()
    return None


def zajemi_vse(n):
    """zajame n filmov in njihove podatke zapise v fajl"""
    pass


#ID    imdbID    naslov    letnica    drzava    runtime    zanr    budget   gross    rating    nr_users    metascore    nr_reviews    nr_critics    nr_metacritic    nr_fb

         
