#!/bin/python
#pour executer ce script dans un terminal (bash) : python3 recup_seq.py chemin_vers_fichiers_results_mmseq chemin__vers_le_fichier_des_séquences_du_métagénome
#exemple : python3 script/recup_seq.py results/results_1/ Data/

#############Importation des modules#####################################

import sys
import os
from collections import defaultdict
#############Déclaration des variables###################################

filepath = sys.argv[1] #mettre dans la variable filepath l'argument[1] de la ligne de commande bash = chemin vers les fichiers résultats de mmseq #ici result/results_1
filepath2= sys.argv[2] #mettre dans la variable filepath2 l'argument[2] de la ligne de commande bash = chemin vers le fichier des séquences du métagénome.
list_seq = list() #liste contenant les séquences le nom des séquences qui ont eu un hit
seq =""
dico_seq = dict() #dictionnaire comprenant le nom de la séquence du métagénome ayant eu un hit associer à sa séquence
lli=""
dico_lli=defaultdict(list) #dictionnaire comprenant le nom de la séquence du métagénome ayant un hit (avec ID enzyme et type de plastique) associer a son nom dans le fichier métagénome (my_protein.fasta)
#ce dictonnaire va nous permettre de retrouver contre quelle(s) enzyme(s) la séquence a eu un hit

############################Script#######################################

with open (filepath+"result_PET.tsv",'r')as f1: #ouvrir le fichier
        for li in f1 :				#pour chaque ligne du fichier
                li=li.strip()			#nettoyage des ligne
                nom = li.split("\t")[0:2]	#recupère dans la variable nom l'identifiant de la séquence et l'ID de l'enzyme qui a produit le hit
                nom_seq = ">"+nom[1]+":"+nom[0]+":"+"PET" #mettre dans la variable nom_seq l'identifiant de la séquence ainsi que l'ID de l'enzyme qui a produit le hit et le nom du plastique de dégradation de l'enzyme
                if nom_seq not in list_seq :	#si le nom de la séquence n'est pas dans la liste de nom de séquence
                        list_seq.append(nom_seq) #ajouter le nom de la séquence à la liste

#même chose pour les autres fichiers de résultats mmseq
with open (filepath+"result_PE.tsv",'r')as f2:
        for li in f2 :
                li=li.strip()
                nom = li.split("\t")[0:2]
                nom_seq = ">"+nom[1]+":"+nom[0]+":"+"PE"
                if nom_seq not in list_seq :
                        list_seq.append(nom_seq)

with open (filepath+"result_PS.tsv",'r')as f3:
        for li in f3 :
                li=li.strip()
                nom = li.split("\t")[0:2]
                nom_seq = ">"+nom[1]+":"+nom[0]+":"+"PS"
                if nom_seq not in list_seq :
                        list_seq.append(nom_seq)

with open (filepath+"result_PU.tsv",'r')as f4:
        for li in f4 :
                li=li.strip()
                nom = li.split("\t")[0:2]
                nom_seq = ">"+nom[1]+":"+nom[0]+":"+"PU"
                if nom_seq not in list_seq :
                        list_seq.append(nom_seq)

with open (filepath+"result_Rubber.tsv",'r')as f5:
        for li in f5 :
                li=li.strip()
                nom = li.split("\t")[0:2]
                nom_seq = ">"+nom[1]+":"+nom[0]+":"+"RU"
                if nom_seq not in list_seq :
                        list_seq.append(nom_seq)

for nom in list_seq :				#pour chaque nom dans la liste des noms de séquence
        lli = nom.split(":")[0]			#mettre dans la variable lli le nom sans l'id de l'enzyme et sans le non du plastique pour pouvoir comparer par la suite ce nom a celui dans le fichier my_proteins.fasta qui lui ne les contient pas 
        dico_lli[lli].append(nom)			#création du dictionnaire contenant les noms avec ID associer au nom sans ID pour pouvoir les retrouver plus tard.

'''for nom in dico_lli:                        #permet de visualiser le dictionnaire dico_lli
        print(dico_lli[nom])'''

with open (filepath2+"my_proteins.fasta",'r') as f6 :	#ouvrir le fichier contenant toutes les séquences protéique du métagénome
        for li in f6 :					#pour chaque ligne du fichier
                li=li.strip()					#nettoyage de la ligne
                if li.startswith(">"):				#si la ligne commence par >
                        nom2_seq=li.split(" ")[0]			#mettre le nom de la séquence dans la variable nom2_seq
                        if nom2_seq in dico_lli :			#si le nom de la séquence se trouve dans le dictionnaire dico_lli
                                 dico_seq[nom2_seq]=''		#alors on remplit le dictionnaire dico_seq avec le nom de la séquence
                else :						#sinon (si la ligne ne commence pas par >)
                        if nom2_seq in dico_lli :			#si le nom de la séquence se trouve dans le dictionnaire dico_lli
                                 dico_seq[nom2_seq]+=li		#alors  on remplit le dictionnaire dico_seq pour chaque clé avec la séquence qui lui correspond

##################Resultats####################

with open(filepath+"seq_hits.fa",'w') as fe1 : #ouvrir un nouveau fichier (pour écrire dedans)
        for nom_seq in dico_seq:			#pour chaque nom de séquence dans le dictionnaire dico_seq
                print(nom_seq,"\n",dico_seq[nom_seq],sep='',file=fe1)	#écrire dans le fichier le nom de la séquence, revenir à la ligne, la séquence

with open(filepath+"correspondances.tsv","w") as fe2 : 
        for lli in dico_lli :
                print(lli,"\t",dico_lli[lli],sep='',file=fe2)

#################Formatage#####################

#pour formater le ficher obtenu au format fasta, on peut utiliser l'outil fasta_formatter (enlever les "'" pour executer la commande)
#cela va créer un deuxième fichier de résultats qui contiendra les séquence sous format fasta (60 aa par ligne)'''

'''os.system("fasta_formatter -i results/seq_hits.fa  -o results/seq_hits.fasta -w 60")'''
