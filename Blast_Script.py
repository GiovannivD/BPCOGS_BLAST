'''BLAST SCRIPT V1.0'''
import os

def create_db(schimmels):
    print("Databases aanmaken...")
    for item in schimmels:
        db_string = "formatdb -i Proteomes/Proteoom_" + item + ".fasta -pT"
        os.system(db_string)
        #print(db_string)
    print("Gelukt!")


def blast(schimmels):
    """Hier wordt elke BLAST uitgevoerd, elk proteoom wordt tegen elk
    proteoom geBLAST en vice versa"""
    file_list = []
    for x in range(2):
        for i in range(len(schimmels)):
            for j in range(i + 1, len(schimmels)):
                schimmel_1 = schimmels[i]
                schimmel_2 = schimmels[j]

                file_schim_1 = schimmel_1[0:3] + \
                              schimmel_1[schimmel_1.find("_"):
                              schimmel_1.find("_") + 4]
                file_schim_2 = schimmel_2[0:3] + \
                              schimmel_2[schimmel_2.find("_"):
                              schimmel_2.find("_") + 4]

                file_name = file_schim_1 + "*" + file_schim_2
                file_list.append(file_name)

                blast_string = "blastall -i Proteomes/Proteoom_" + schimmel_1 + \
                               ".fasta -d Proteomes/Proteoom_" + schimmel_2 + \
                               ".fasta -p blastp -e 0.0001 -m9 > " \
                               "BLAST/blast_" + file_name + ".txt"

                print("BLAST: " + file_name + "...")
                os.system(blast_string)
                #print(blast_string)
                print("Gelukt!")

        schimmels = schimmels[::-1]

    return file_list


def hits(b_file_list):
    """Haalt de eerste hits uit een BLAST en zet deze in een aparte
    file in de map HITS. Dit wordt gedaan voor elke BLAST die is
    uitgevoerd."""
    for file_name in b_file_list:
        filter_string = "awk '{print $1, $2, $11}' " \
                        "BLAST/blast_" + file_name + \
                        ".txt | egrep -A1 ^# | egrep \"^[^#-]\" >" \
                        "> HITS/hits_" + file_name + ".txt"
        print("Beste hits vinden voor: " + file_name)
        os.system(filter_string)
        #print(filter_string)
        print("Gelukt!")


def directional_hit(b_file_list):
    print("BDH vinden...")
    while range(len(b_file_list)) > 0:
        for x in b_file_list:
            #print("Start:", b_file_list)
            x = x.replace('*', '')
            deel1, deel2 = x[:len(x)/2], x[len(x)/2:]

            turn_string = "awk '{print $2, $1}' HITS/hits_" + deel1 + "*" + \
                          deel2 + ".txt > Modified/turned_" + deel1 + "*" + \
                          deel2 + ".txt"
            b_file_list.remove(deel1 + "*" + deel2)

            two_column = "awk '{print $1, $2}' HITS/hits_" + deel2 + "*" + \
                         deel1 + ".txt > Modified/twoCol_" + deel2 + "*" + \
                         deel1 + ".txt"
            b_file_list.remove(deel2 + "*" + deel1)

            os.system(turn_string)
            os.system(two_column)

            duplicaten = "sort Modified/turned_" + deel1 + "*" + deel2 + \
                         ".txt Modified/twoCol_" + deel2 + "*" + deel1 + \
                         ".txt | awk 'dup[$0]++ == 1' > BDH/bdh_" + deel1 + \
                         deel2 + ".txt"

            os.system(duplicaten)
            #print("Eind:", b_file_list)
    print("Gelukt!")

def main():
    os.system("mkdir -p BLAST HITS BDH Modified")
    schimmel_list = ["Ashbya_gossypii", "Aspergillus_nidulans",
                     "Neurospora_crassa"]#, "Penicillium_canescens",
                     #"Penicillium_raistrickii", "Phanerochaete_chrysosporium",
                     #"Rhizoctonia_solani", "Saccharomyces_cerevisea",
                     #"Trichoderma_atroviride", "Trichoderma_virens"]

    create_db(schimmel_list)
    b_file_list = blast(schimmel_list)
    hits(b_file_list)
    directional_hit(b_file_list)

main()
