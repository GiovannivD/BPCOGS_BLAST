'''BLAST SCRIPT V1.0'''
import os

def create_db(schimmels):
    for item in schimmels:
        db_string = "formatdb -i /Proteoom_" + item + ".fasta -pF"
        os.system(db_string)

def blast(schimmel_1, schimmel_2, schimmels):
    '''Alle blasts (proteoom tegen proteoom)'''

    for x in range(len(schimmels)):
        schimmel_1 = schimmels[x]
        schimmel_2 = schimmels[x+1]
        blast_string = "blastall -i Proteoom_" + schimmel_1 + ".fasta -d Proteoom_" + schimmel_2 + ".fasta -p blastp -m9 > blast_" + schimmel_1 + "_vs_" + schimmel_2
        print(blast_string)


    #os.system("blastall -i Proteoom_Ashbya_gossypii.fasta -d"
    #          "Proteoom_Aspergillus_nidulans.fasta -p blastp -m9 > blasttest")

def split():
    '''Haalt alle beste hits uit de blasts en zet deze in een aparte file die
    dmv de naam van de schimmels wordt benoemd.'''
    
    os.system("cat blasttest | awk '{print $1, $2, $11}' | sed 's/# Fields: "
              "mismatches,/@/g' | awk '/@/{getline; print}' | egrep -v ^# > "
              "AshGos_AspNid")

def main():
    schimmel_list = ["Ashbya_gossypii", "Aspergillus_nidulans", "Neurospora_crassa",
                    "Penicillium_canescens", "Penicillium_raistrickii",
                    "Phanerochaete_chrysosporium", "Rhizoctonia_solani",
                    "Saccharomyces_cerevisea", "Trichoderma_atroviride",
                    "Trichoderma_virens"]

    #create_db(schimmel_list)
    blast("test_1", "test_2", schimmel_list)
    #split()

main()
