#!/usr/bin/python
# -*- coding:utf-8 -*-

from interface import *
from random import randint, random
from datetime import *
from tkinter.messagebox import *
import os

#############################################################
#                     OBJETS                                #
#############################################################

class Joueur:
	def __init__(self,id):
		self.id = id
		self.name = str(id)
		self.position = 0
		self.charbon = 10
		self.ors = 0
		
	
	def initNom(self,name):
		self.name = name
	
	def __lt__(self, joueur):
		if self.ors < joueur.ors :
			return True
		elif self.ors == joueur.ors :
			if self.charbon < joueur.charbon :
				return True
			else:
				return False
		else :
			return False
				
	def __eq__(self,joueur):
		if self.ors == joueur.ors :
			if self.charbon == joueur.charbon :
				return True
		else :
			return False
	

	def __gt__(self, joueur):
		if self.ors > joueur.ors :
			return True
		elif self.ors == joueur.ors :
			if self.charbon > joueur.charbon :
				return True
			else:
				return False
		else :
			return False
				
	# def __le__(self, joueur):# For x <= y
		# return self < joueur or self == joueur
		
	# def __ne__(self, joueur):# For x != y OR x <> y
		# return not self == joueur
		
	# def __ge__(self, joueur):# For x >= y
		# returnself > joueur or self == joueur
		
	def afficherScore(self):
		return "Joueur "+self.name+" avec "+str(self.ors)+ " l'ingo d'or et "+ str(self.charbon)+" Charbon"

		

class Case:
	def __init__(self):
		self.couleur = 0
		
		def effet(self,joueur):
			pass


class CaseVert(Case):
	def __init__(self):
		self.couleur = 1
		
	def effet(self,joueur):
		joueur.charbon += 3

class CaseRogue(Case):
	def __init__(self):
		self.couleur = 2
		
	def effet(self,joueur):
		if joueur.charbon > 2 :
			joueur.charbon -= 3
		else :
			joueur.charbon = 0


class CaseBleu(Case):
	def __init__(self):
		self.couleur = 3
		
	def effet(self,joueur):
		f = open("question\question.txt","r",encoding="utf8").read()

		#print(f)

		questions = f.split("#")
		questions.pop(0)
		print(questions)

		nbQuestion = randint(1,1000)%len(questions)

		question = questions[nbQuestion]

		sujet = question.split("|")[0]
		rep = question.split("|")[1].split("\n")[0]

		repT = askquestion("Question ", sujet)

		print(repT)
		print(rep)
		if str(repT) == rep :
			joueur.charbon += 3
			showinfo('Resultat', 'Vous avez gagner!')	
		else :
			showinfo('Resultat', 'Vous avez perdu!')	

class CaseJaune(Case):
	def __init__(self):
		self.couleur = 4
		
	def effet(self,joueur):
		joueur.charbon += 10		

class FabriqueCase:
	
	def __init__(self):
		self.typePosible = 4
	
	def create(self,idCouleur):
		if idCouleur <= 0.5 :
			return CaseBleu()
			
		elif idCouleur <= 0.75 :
			return CaseVert()
			
		elif idCouleur <= 0.95 :
			return CaseRogue()	
			
		else :
			return CaseJaune()

		
class Plateau:
	
	def __init__(self,nbCase,nbJoueurs):
	
		fabric = FabriqueCase()
		
		self.plateau = [fabric.create(random()) for x in range(nbCase)]
			
		self.joueurs = [Joueur(x) for x in range(nbJoueurs)]
		
		self.gold = randint(0,nbCase)
				
		self.plateauCreePlateau()
		
		self.plateauCreeJoueurs()
		
		self.plateauNomerJoueurs()
		
		self.plateauPlacerGold()
		
	def plateauCreePlateau(self):
		creePlateau(self.plateau)

	
	def plateauCreeJoueurs(self):
		creeJoueurs(self.joueurs, self.plateau)
	
	def plateauNomerJoueurs(self):
		nomerJoueurs(self.joueurs)
	
	def plateauPlacerGold(self):
		placeOr(self.gold, self.plateau)
		
		
	def lancerDe(self,nbFace):
		return randint(1,nbFace)


	def deplaceJoueur(self,joueur, de ):
		for x in range(de):
			joueur.position = (joueur.position+1)%len(self.plateau)
			bougeJoueur(joueur, self.plateau)
			self.effetOr(joueur)
			
			
			
	def effetOr(self,joueur):
		if joueur.position == self.gold :
			if joueur.charbon >= 10 :
				joueur.charbon -= 10
				joueur.ors += 1
				self.gold = randint(0,len(self.plateau))
				self.plateauPlacerGold()	

				
	def tourJoueur(self,joueur):
		de = self.lancerDe(6)
		lancerDe(de)
		self.deplaceJoueur(joueur,de)
		self.effetOr(joueur)
		self.effetCase(joueur)
		
		
		
	def effetCase(self,joueur):
		self.plateau[joueur.position].effet(joueur)	
		
		
		
	def tourDeJeu(self):
		for joueur in self.joueurs:
			self.tourJoueur(joueur)
			Afficher_score(self.joueurs)


	def partie(self, nbTours):
		Afficher_score(self.joueurs)
		for x in range(1,nbTours+1):			
			print("--- TOUR N°",x,"---")
			self.tourDeJeu()
			self.afficherJoueur()
			
			if x%3 == 0:
				self.jeu1()
			
		print("--- SCORE FINAL ---")
		self.trieJoueurs()
		self.joueurs.reverse()
		Afficher_score(self.joueurs)
		annonce_score(self.joueurs)
		self.afficherJoueur()
		self.sauvegardeResultats()	





	def trieJoueurs(self):
		for x in range(len(self.joueurs)) :
			for y in range(x+1,len(self.joueurs)) :
				if (self.joueurs[x] > self.joueurs[y]) == True :
					memoire = self.joueurs[y]
					self.joueurs[y] = self.joueurs[x]
					self.joueurs[x] = memoire
					
					

	def sauvegardeResultats(self,):
		aujourdhui = date.today()
		heure = time()
		f = open("score\chariot-party-"+str(aujourdhui.day)+"-"+str(aujourdhui.month)+"-"+str(aujourdhui.year)+".txt","a",encoding="utf8")
		f.write("---------- Nouvelle Partie -----------------\n"+self.score+"\n\n")
		f.close()

		
	def afficherJoueur(self):
		self.score = ""
		for j in self.joueurs :
			print("Numero ",self.joueurs.index(j)+1, j.afficherScore())
			self.score += "Numero "+ str(self.joueurs.index(j)+1)+" "+j.afficherScore() +"\n"
			
	
	def jeu1(self):
		
		resJ1 = [ ]
		for x in self.joueurs :
			resJ1.append(affJeu1(x))
			
		nbAleratpoire = randint(1,100)

		score = abs(resJ1[0]-nbAleratpoire)
		wineur = 0
		for y in range(1,len(resJ1)):
			if score > abs(resJ1[y]-nbAleratpoire):
				score = abs(resJ1[y]-nbAleratpoire)
				wineur = y
				
		self.joueurs[wineur].charbon += 10
		print("Joueur : ",wineur, "Gagne le jeu")
		affWiner(self.joueurs[wineur])	
		
	
	def jeu2(self):
		pass
		
	
########################################################################		
		
	
			
def configuration() :
	
	# nbJoueurs = -1
	# valider = False
	# while valider != True :
		# nbJoueurs = int(input("Combien de joueur [1-4] ?"))
		# if nbJoueurs > 0 :
			# if nbJoueurs < 5 :
				# print("Vous avez ", nbJoueurs, " joueurs")
				# valider = True


	# nbTours = 0
	# while nbTours < 1 :	
		# nbTours = int(input("Combien de tours ?"))
		# print("Vous avez ", nbTours, " tours")

	# nbCase = 2
	# while nbCase%4 != 0 :
		# nbCase = int(input("Combien de cases ?"))
		# print("Vous avez ", nbCase, " cases")	
		
		
		
	nbJoueurs = demandeNbJoueurs()

	nbTours = demandeNbTours()
	
	nbCase = demandeNbCase()

	return nbJoueurs,nbTours,nbCase
	
# def initialisationJoueur(nbJoueurs):
	# joueurs = []

	# for x in range(nbJoueurs):
		# joueurs.append(Joueur(x))
				 
	# return joueurs	


# def initalisationPlateau(nbCases):
	# plateau = []
	# for x in range(nbCase):
		# plateau.append(Case(randint(1,3)))
	# return plateau

#def initGold(nbCase):
#	return randint(0,nbCase)

#############################################################################
#                                game play                                  #
#############################################################################	
	
# def lancerDe(nbFace):
	# return randint(1,nbFace)
	
# def deplaceJoueur(joueur,de, plateau):
	#print(de)
	# for x in range(de):
		# joueur.position = (joueur.position+1)%len(plateau)
		# bougeJoueur(joueur, plateau)
	
	

# def effetOr(joueur,plateau,gold):
	# if joueur.position == gold :
		# if joueur.charbon >= 10 :
			# joueur.charbon -= 10
			# joueur.ors += 1
			# gold = initGold(len(plateau))
			# placeOr(gold, plateau)

# def effetCase(joueur,plateau):
	# plateau[joueur.position].effet(joueur)

		
# def tourJoueur(joueur, plateau):	
	# deplaceJoueur(joueur,lancerDe(6),plateau)
	# effetCase(joueur,plateau)
	# effetOr(joueur,plateau,gold)
	#print(joueur)
	
	
# def tourDeJeu(joueurs):
	# for joueur in joueurs:
		# tourJoueur(joueur,plateau)


# def partie(nbTours, joueurs):
	# for x in range(0,nbTours):
		# tourDeJeu(joueurs)

#######################################################################
#                        Ecriture                                     #
#######################################################################

# def compJoueurs(joueur1,  joueur2):
	# if joueur1.ors > joueur2.ors :
		# return 1
	# elif joueur1.ors < joueur2.ors :
		# return -1
	# else :
		# if joueur1.charbon > joueur2.charbon :
			# return 1
		# elif joueur1.charbon < joueur2.charbon :
			# return -1
		# else :
			# return 0
			
# def trieJoueurs(joueurs):

	# for x in joueurs :
		# for y in joueurs[joueurs.index(x):] :
			# if (x > y) == True :
				# memoire = joueurs[joueurs.index(y)]
				# joueurs[joueurs.index(y)] = x
				# joueurs[joueurs.index(x)] = y

# def sauvegardeResultats(score):
	# aujourdhui = date.today()
	# heure = time()
	# f = open("score\chariot-party-"+str(aujourdhui.day)+"-"+str(aujourdhui.month)+"-"+str(aujourdhui.year)+".txt","a",encoding="utf8")
	# f.write("---------- Nouvelle Partie -----------------\n"+score+"\n\n")
	# f.close()

	
# def afficherJoueur(joueurs):
	# trieJoueurs(joueurs)
	# joueurs.reverse()
	# score = ""
	# for j in joueurs :
		# print("Numero ",joueurs.index(j)+1, j.afficherScore())
		# score += "Numero "+ str(joueurs.index(j)+1)+" "+j.afficherScore() +"\n"
	# sauvegardeResultats(score)



if __name__ == '__main__':
	
	partieEnd = False
	rep = 1
	while partieEnd != True:
		
		if rep == 1 :
			print("---- Nouvelle Partie ---- ")
			nbJoueurs,nbTours,nbCase = configuration()
		elif rep == 2 :
			plateau.joueurs.clear()
			print("---- Relance ----")
					
		plateau = Plateau(nbCase,nbJoueurs)
		
		plateau.partie(nbTours)
	
		print(" 1 : nouvelle partie")
		print(" 2 : relancer ")
		print(" 0 : Quiter ")
		
		# rep = int(input("1, 2 ou 0 "))
		
		rep = newPartie()
		
		if rep == 0 :
			partieEnd = True
	
		effacePlateau()	
