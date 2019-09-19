#!/usr/bin/python
# -*- coding:utf-8 -*-

from interface import *
from random import randint
from datetime import *
import os


###################################################################
#                              PARTIE  I                          #
###################################################################
# plateau = [1,1,3,3,3,2
		   # ,3,1
		   # ,3,3
		   # ,3,3
		   # ,3,1
		   # ,1,3,3,3,3,1]
		  
		  
# print(plateau)

#gold = 24
			 
# joueurs =   {0:{"position":3,"charbon":4,"or":0},1:{"position":8,"charbon":10,"or":0},
             # 2:{"position":16,"charbon":3,"or":1},3:{"position":7,"charbon":0,"or":0}}

			 
			 
####################################################################
#                             INITIALISATION                       #
####################################################################

def configuration() :
	
	nbJoueurs = -1
	valider = False
	while valider != True :
		nbJoueurs = int(input("Combien de joueur [1-4] ?"))
		if nbJoueurs > 0 :
			if nbJoueurs < 5 :
				print("Vous avez ", nbJoueurs, " joueurs")
				valider = True


	nbTours = 0
	while nbTours < 1 :	
		nbTours = int(input("Combien de tours ?"))
		print("Vous avez ", nbTours, " tours")

	nbCase = 2
	while nbCase%4 != 0 :
		nbCase = int(input("Combien de cases ?"))
		print("Vous avez ", nbCase, " cases")	

	return nbJoueurs,nbTours,nbCase
	
def initialisationJoueur(nbJoueurs):
	joueurs = []

	for x in range(nbJoueurs):
		joueurs.append({"id":x,"position":0,"charbon":10,"or":0})
				 
	return joueurs	


def initalisationPlateau(nbCases):
	plateau = []
	for x in range(nbCase):
		plateau.append(randint(1,3))
	return plateau

def initGold(nbCase):
	return randint(0,nbCase)

#############################################################################
#                                game play                                  #
#############################################################################	
	
def lancerDe(nbFace):
	return randint(1,nbFace)
	
def deplaceJoueur(joueur,de, plateau):
	#print(de)
	for x in range(de):
		joueur['position'] = (joueur['position']+1)%len(plateau)
		bougeJoueur(joueur, plateau)
	
	

def effetOr(joueur,plateau,gold):
	if joueur['position'] == gold :
		if joueur['charbon'] >= 10 :
			joueur['charbon'] -= 10
			joueur['or'] += 1
			gold = initGold(len(plateau))
			placeOr(gold, plateau)

def effetCase(joueur,plateau):
	if plateau[joueur['position']] == 1 :
		joueur['charbon'] += 3
	if plateau[joueur['position']] == 2 :
		joueur['charbon'] -= 3
		
def tourJoueur(joueur, plateau):	
	deplaceJoueur(joueur,lancerDe(6),plateau)
	effetCase(joueur,plateau)
	effetOr(joueur,plateau,gold)
	#print(joueur)
	
	
def tourDeJeu(joueurs):
	for joueur in joueurs:
		tourJoueur(joueur,plateau)


def partie(nbTours, joueurs):
	for x in range(0,nbTours):
		tourDeJeu(joueurs)

#######################################################################
#                        Ecriture                                     #
#######################################################################

def compJoueurs(joueur1,  joueur2):
	if joueur1['or'] > joueur2['or'] :
		return 1
	elif joueur1['or'] < joueur2['or'] :
		return -1
	else :
		if joueur1['charbon'] > joueur2['charbon'] :
			return 1
		elif joueur1['charbon'] < joueur2['charbon'] :
			return -1
		else :
			return 0
			
def trieJoueurs(joueurs):
	for x in joueurs :
		for y in joueurs[joueurs.index(x):] :
			val = compJoueurs(x,y)
			if val > 0 :
				memoire = joueurs[joueurs.index(y)]
				joueurs[joueurs.index(y)] = x
				joueurs[joueurs.index(x)] = y

def sauvegardeResultats(score):
	aujourdhui = date.today()
	heure = time()
	f = open("score\chariot-party-"+str(aujourdhui.day)+"-"+str(aujourdhui.month)+"-"+str(aujourdhui.year)+".txt","a",encoding="utf8")
	f.write("---------- Nouvelle Partie -----------------\n"+score+"\n\n")
	f.close()

	
def afficherJoueur(joueurs):
	trieJoueurs(joueurs)
	joueurs.reverse()
	score = ""
	for j in joueurs :
		print("Numero ",joueurs.index(j)+1," Joueur ",j['id']," avec ",j['or'], " l'ingo d'or et ",j['charbon'], " Charbon")
		score += "Numero "+ str(joueurs.index(j)+1)+" Joueur "+str(j['id'])+" avec "+str(j['or'])+ " l'ingo d'or et "+str(j['charbon'])+ " Charbon\n"
	sauvegardeResultats(score)



if __name__ == '__main__':
	
	partieEnd = False
	rep = 1
	while partie != True:
		
		if rep == 1 :
			print("---- Nouvelle Partie ---- ")
			nbJoueurs,nbTours,nbCase = configuration()
		elif rep == 2 :
			print("---- Relance ----")
			
		joueurs = initialisationJoueur(nbJoueurs)
		plateau = initalisationPlateau(nbCase)
		gold = initGold(nbCase)


		creePlateau(plateau)
		
		creeJoueurs(joueurs, plateau)
		placeOr(gold, plateau)
		partie(nbTours, joueurs)
		afficherJoueur(joueurs)
	
		print(" 1 : nouvelle partie")
		print(" 2 : relancer ")
		print(" 0 : Quiter ")
		
		rep = int(input("1, 2 ou 0 "))
		
		if rep == 0 :
			break
	
		effacePlateau()

	
	
