'''BLAST SCRIPT V1.0'''
import os

def create_db(schimmels):
    for item in schimmels:
        db_string = "formatdb -i /Proteoom_" + item + ".fasta -pF"
        os.system(db_string)


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

                blast_string = "blastall -i Proteoom_" + schimmel_1 + \
                               ".fasta -d Proteoom_" + schimmel_2 + \
                               ".fasta -p blastp -m9 -O BLAST/blast_" \
                               + file_name + ".txt"
                print(blast_string)
                #os.system(blast_string)

        #Draait hier de lijst om
        schimmels = schimmels[::-1]

    return file_list


def split(b_file_list):
    """Haalt de eerste hits uit een BLAST en zet deze in een aparte
    file in de map HITS. Dit wordt gedaan voor elke BLAST die is
    uitgevoerd."""

    for file in b_file_list:
        filter_string = "awk '{print $1, $2, $11}' " \
                        "BLAST/blast_" + file + \
                        ".txt | sed 's/# Fields: mismatches,/@/g' | " \
                        "awk '/@/{getline; print}' | egrep -v ^# " \
                        "-O HITS/hits_" + file + ".txt"
        #os.system(filter_string)
        print(filter_string)


def main():
    os.system("mkdir BLAST HITS")
    schimmel_list = ["Ashbya_gossypii", "Aspergillus_nidulans",
                     "Neurospora_crassa"]
                     #"Penicillium_canescens", "Penicillium_raistrickii",
                     #"Phanerochaete_chrysosporium", "Rhizoctonia_solani",
                     #"Saccharomyces_cerevisea", "Trichoderma_atroviride",
                     #"Trichoderma_virens"]

    #create_db(schimmel_list)
    b_file_list = blast(schimmel_list)
    split(b_file_list)

main()
