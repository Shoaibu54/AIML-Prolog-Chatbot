male(soban).
dateofbirth(dani,1999).
dateofbirth(dani,1998).
parent(dani,pomi).
dateofbirth(pomi,1988).
male(pomi).
parent(sadi,sami).
parent(dani,sadi).
parent(dani,ali).
male(dani).
dateofbirth(ali,1994).
dateofbirth(sadi,1990).
male(sami).
male(sadi).
male(ali).

neq(X,Y) :- X \= Y.
neq(X, X) :- !, fail.
neq(_, _).

age(X,A)          :- dateofbirth(X,Y), A is 2026-Y.
elder(X,Y)        :- age(X,AX), age(Y,AY), AX > AY.
younger(X,Y)      :- age(X,AX), age(Y,AY), AX < AY.
father(X,Y)       :- male(X), parent(X,Y).
mother(X,Y)       :- female(X), parent(X,Y).

husband(X,Y)      :- male(X), marriedto(X,Y).
wife(X,Y)         :- female(X), marriedto(X,Y).
spouse(X,Y)       :- marriedto(X,Y).

son(X,Y)          :- male(X), parent(Y,X).
daughter(X,Y)     :- female(X), parent(Y,X).
child(X,Y)        :- parent(Y,X).

brother(X,Y)      :- male(X), father(F,X), father(F,Y), neq(X,Y).
elderbrother(X,Y) :- brother(X,Y), elder(X,Y).
youngerbrother(X,Y):- brother(X,Y), younger(X,Y).
sister(X,Y)       :- female(X), father(F,X), father(F,Y), neq(X,Y).
eldersister(X,Y)  :- sister(X,Y), elder(X,Y).
youngersister(X,Y):- sister(X,Y), younger(X,Y).
sibling(X,Y)      :- father(Z,X), father(Z,Y), neq(X,Y).

grandfather(X,Y)  :- male(X), parent(X,Z), parent(Z,Y).
grandmother(X,Y)  :- female(X), parent(X,Z), parent(Z,Y).
grandparent(X,Y)  :- parent(X,Z), parent(Z,Y).
ancestor(X,Y)     :- parent(X,Y).
ancestor(X,Y)     :- parent(X,Z), ancestor(Z,Y).
dada(X,Y)         :- father(X,Z), father(Z,Y).
dadi(X,Y)         :- mother(X,Z), father(Z,Y).
nana(X,Y)         :- father(X,Z), mother(Z,Y).
nani(X,Y)         :- mother(X,Z), mother(Z,Y).

uncle(X,Y)        :- brother(X,PA), parent(PA,Y).
chacha(X,Y)       :- brother(X,Z), father(Z,Y), younger(Z,X).
taya(X,Y)         :- brother(X,Z), father(Z,Y), elder(Z,X).
phupha(X,Y)       :- husband(X,Z), phupho(Z,Y).
mamu(X,Y)         :- brother(X,Z), mother(Z,Y).
khalu(X,Y)        :- husband(X,Z), khala(Z,Y).

aunt(X,Y)         :- sister(X,Z), parent(Z,Y).
khala(X,Y)        :- sister(X,Z), mother(Z,Y).
phupho(X,Y)       :- sister(X,Z), father(Z,Y).
tayi(X,Y)         :- wife(X,Z), taya(Z,Y).
chachi(X,Y)       :- wife(X,Z), chacha(Z,Y).

cousin(X,Y)       :- parent(PX,X), parent(PY,Y), sibling(PX,PY), neq(X,Y).

nephew(X,Y)       :- male(X), uncle(Y,X).
neice(X,Y)        :- female(X), uncle(Y,X).
bhanja(X,Y)       :- male(X), khala(Y,X).
bhanja(X,Y)       :- male(X), mamu(Y,X).
bhanji(X,Y)       :- female(X), khala(Y,X).
bhanji(X,Y)       :- female(X), mamu(Y,X).
bhatija(X,Y)      :- male(X), phupho(Y,X).
bhatija(X,Y)      :- male(X), chacha(Y,X).
bhatija(X,Y)      :- male(X), taya(Y,X).
bhatiji(X,Y)      :- female(X), phupho(Y,X).
bhatiji(X,Y)      :- female(X), chacha(Y,X).
bhatiji(X,Y)      :- female(X), taya(Y,X).

grandson(X,Y)     :- male(X), grandparent(Y,X).
granddaughter(X,Y):- female(X), grandparent(Y,X).
grandchild(X,Y)   :- grandparent(Y,X).
pota(X,Y)         :- son(X,Z), son(Z,Y).
poti(X,Y)         :- daughter(X,Z), son(Z,Y).
nawasa(X,Y)       :- son(X,Z), daughter(Z,Y).
nawasi(X,Y)       :- daughter(X,Z), daughter(Z,Y).

fatherinlaw(X,Y)  :- father(X,Z), spouse(Z,Y).
motherinlaw(X,Y)  :- mother(X,Z), spouse(Z,Y).
soninlaw(X,Y)     :- spouse(X,Z), daughter(Z,Y).
daughterinlaw(X,Y):- spouse(X,Z), son(Z,Y).

brotherinlaw(X,Y) :- spouse(X,Z), brother(Y,Z).
dewar(X,Y)        :- youngerbrother(X,Z), husband(Z,Y).
jeth(X,Y)         :- elderbrother(X,Z), husband(Z,Y).
behnoi(X,Y)       :- male(X), wife(Z,X), sister(Z,Y).
sala(X,Y)         :- brother(X,Z), wife(Z,Y).

sisterinlaw(X,Y)  :- spouse(X,Z), sister(Y,Z).
nand(X,Y)         :- sister(X,Z), husband(Z,Y).
bhabhi(X,Y)       :- female(X), wife(X,Z), brother(Z,Y).
sali(X,Y)         :- sister(X,Z), wife(Z,Y).
jethani(X,Y)      :- wife(X,Z), jeth(Z,Y).
dewarani(X,Y)     :- wife(X,Z), dewar(Z,Y).

sandu(X,Y)        :- husband(X,Z), sister(Z,W), wife(W,Y).
