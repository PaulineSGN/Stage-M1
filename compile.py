#!/bin/python3

import sys
import pandas as pd

#lister le noms des séquences du métagénome qui ont eu un hit avec le numéro d'identifiaction de l'enzyme qui a produit ce hit (et l'ID du plastique associer) 
liste_seq = list()

with open ("correspondances.tsv","r") as f1 : 
	for li in f1 :
		li = li.rstrip("\n")
		li = li.split("\t")
		nom = li[1]
		nom = nom.split("'")
		seq = nom[1]
		seq =seq.replace(">","")
		liste_seq.append(seq)
with open ("seq_enz.tsv","w") as fe1 : 
	print("sequence:enzyme:plastique",file=fe1)
	for x in liste_seq :
		print(x,file=fe1)

#Associer les séquences (prédites) du métagénome qui ont eu un hit (avec une enzyme) avec leur taxonomy
#tableau 1
hits = pd.read_csv("seq_enz.tsv",sep=':',index_col = "sequence")

#tableau 2
taxo = pd.read_csv("~/Bureau/Stage/resultats/taxo/taxo_hits/result_taxo.tsv",sep='\t',index_col="sequence")

#supprime les colonnes qui ne nous interessent pas 
taxo.drop(columns=['ID','rank','path'], inplace = True)

#assemble les deux tableaux
result=pd.merge(hits,taxo,on='sequence',how='outer')

#on met le tout dans un fichier 

result.to_csv('taxo_seq.csv')

