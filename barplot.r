# Histogram po drzavah
# Histogram po letnicah
# Histogram po ocenah
# Odvisnost ocen od budgeta/gross
# prebere datoteko, narise barplot 10-ih najpogostejsih drzav

imdb <- read.table("p1003.txt", header=TRUE)
# Tukaj moras nares posebej za nakljucen vzorec in za iskanje preko priporocil...

drzave <- levels(imdb[,12])
nd <- length(drzave)

binned <- hist(c(imdb[,12], breaks=c(0.5:(nd+0.5)), plot=FALSE)$counts # drzave po predalckih
vrstni_red <- order(binned)
nazaj <- c(nd:1)

drzave <- drzave[vrstni_red]
binned <- binned[vrstni_red]
drzave2 <- drzave[nazaj]
binned2 <- binned[nazaj]

pdf('hist_drzav.pdf')
#barplot(binned[n-10:n], names.arg=drzave[n-10:n], cex.names=0.5)
barplot(binned2[1:10], names.arg=drzave[1:10], cex.names=0.5) # lepsi vrstni red
dev.off()

##############################
# Razporeditev po zanrih
##############################

zanri <- levels(imdb[,13])
nz <- length(zanri)

bzanri <- hist(c(imdb[,12], breaks=c(0.5:(nz+0.5)), plot=FALSE)$counts # drzave po predalckih
vrstni_red_zanrov <- order(bzanri)
znazaj <- c(nz:1)

zanri <- zanri[vrstni_red_zanrov]
bzanri <- bzanri[vrstni_red_zanrov]
zanri2 <- zanri[znazaj]
bzanri2 <- bzanri[znazaj]
pdf('hist_zanr.pdf')
barplot(bzanri2[1:10], names.arg=zanri2[1:10], cex.names=0.5)
dev.off()

##############################
# letnice, trajanje
##############################

letnice <- imdb[,3]
pdf('hist_let.pdf')
hist(letnice, breaks=c((min(letnice)-0.5) : (max(letnice) + 0.5), main="Stevilo filmov v posameznem letu" )
dev.off()
# desetletje...
pdf('hist_delet.pdf')
hist(letnice, breaks=seq((min(letnice)-1), (max(letnice) + 1), 10), main="Stevilo filmov v posameznem letu" )
dev.off()

# glede na desetletje
# filme lahko razporedis v zgodovinska obdobja - sam jih potrebujes vec...

dur <- imdb[,4]
hist(dur, breaks=seq(0, max(dur), 5), main="razporeditev po casu trajanja"
dev.off()

##############################
# ocene
##############################

ocene <- imdb[,5]
