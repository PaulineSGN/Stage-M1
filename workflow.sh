#!/bin/bash

#Prérequis : Dernières versions de prodigal, mmseqs, python
#Modules python : pandas
#Script a adapté en fonction des données et des besoins (penser a adapter les scripts python avec)

#Etape 1 : prédiction des protéines avec prodigal

prodigal -i metagenom -o genes.gbk -a proteins.faa
#option -i = fichier d'entrée,  option -o fichier de sortie (par defaut format genbank), option -a = fichier de sortie contenant les protéines prédites.

#Etape 2 :
#Utilisation de mmseq2 pour trouver protéines d'intérêt dans un métagénome
#Il faut d'abord convertir les fichiers fasta query et target en bd afin que les données soit compatible avec mmseqs

mmseqs createdb enzyme.fasta enzyme
mmseqs createdb metagenom.fasta metagenom

#ensuite on créer un répertoire tmp

mkdir tmp

#on peut maintenant comparer nos séquences

mmseqs search enzyme metagenom my_results tmp

# Il faut ensuite convertir les résultats en fichier plus classique sous format "Blast"

mmseqs convertalis enzyme metagenom my_results my_results.tsv

#visualisé les 10 premières lignes du résultat

head my_results.tsv
#Dans l'ordre les colonnes correspondent à  (1,2) identifiers for query and target sequences/profiles, (3) sequence identity, (4) alignment length, (5) number of mismatches, (6) number of gap openings, (7-8, 9-10) domain start and end-position in query and in target, (11) E-value, and (12) bit score.

#Si on a plusieurs fichiers "my_results.tsv" (quand on l'a fait en plusieurs fois, par exemple si on a séparé les enzymes en fonction du plastique qu'elle dégradent ), on peut les concaténer avec le script python suivant

python3 compile_search_results.py

#Etape 3 : récupération des séquences protéiques du métagénome qui ont obtenu un hit contre les enzymes
#associer le nom des séquences ayant eu un hit au numéro de l'enzymes qui a "matcher"
#Fais avec un script python -> deux fichiers de sortie : le fichiers des séquences au format fasta et un fichier de correspondances au format tsv

python3 recup_seq.py

#Etape 5 : Annotation taxonomique des protéines du metagenome correspondant a des enzymes

#Téléchargement de la base de données
#ici on a utilisé la base de données swissprot mais mmseqs permet de téléchargé d'autre bases de données en fonction des besoins (voir les bases dispo : mmseqs databases)

mmseqs databases UniProtKB/Swiss-Prot UniprotDB/swissprot tmp

#adapter nos séquences au format pris en charge par mmseqs

mmseqs createdb seq_hits.fasta seq_hits

#Faire la taxonomy

mmseqs taxonomy seq_hits  UniprotDB/swissprot Resultats_taxo/lca_result tmp -s 2 --lca-ranks species,genus,family,order,class,phylum,kingdom,superkingdom

mmseqs createtsv seq_hits Resultats_taxo/lca_result results_taxo.tsv
mmseqs taxonomyreport UniprotDB/swissprot  Resultats_taxo/lca_result taxo_report.txt

#Avoir la représentation Krona
mmseqs taxonomyreport UniprotDB/swissprot Resultats_taxo/lca_result taxo_krona.html --report-mode 1

#Etape 6 : associer les protéines du métagénome ayant eu un hit avec leur taxonomie
#script python (ce script a besoin des fichier correspondances.tsv et results_taxo.tsv)

python3 compile.py

#Etape 7 : Annotation taxonomique de toute les protéines tourver dans le métagenome afin de pouvoir comparer
#réutilisation de la base de données swissprot
#même système que pour l'étape 5
#adapter les séquences au format pris en charge par mmseqs

mmseqs createdb proteins.faa my_proteins

mmseqs taxonomy my_proteins UniprotDB/swissprot Resultats_taxo/lca_result_all_prot tmp -s 2 --lca-ranks species,genus,family,order,class,phylum,kingdom,superkingdom

mmseqs createtsv my_proteins Resultats_taxo/lca_result_all_prot all_prot_taxo.tsv

mmseqs taxonomyreport UniprotDB/swissprot Resultats_taxo/lca_result_all_prot all_prot_taxo_report.txt

#Représentation de Krona
mmseqs taxonomyreport UniprotDB/swissprot Resultats_taxo/lca_result_all_prot all_prot_taxo_krona.html --report-mode 1
