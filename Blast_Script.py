'''BLAST SCRIPT V1.0'''
import os

def create_db():
    os.system("formatdb -i Proteomes/Proteoom_Phanerochaete_chrysosporium.fasta"
              " -pF")

def blast():
    '''Alle blasts (proteoom tegen proteoom)'''
    os.system("blastall -i Proteoom_Ashbya_gossypii.fasta -d"
              "Proteoom_Aspergillus_nidulans.fasta -p blastp -m9 > blasttest")

def split():
    '''Haalt alle beste hits uit de blasts en zet deze in een aparte file die
    dmv de naam van de schimmels wordt benoemd.'''
    
    os.system("cat blasttest | awk '{print $1, $2, $11}' | sed 's/# Fields: "
              "mismatches,/@/g' | awk '/@/{getline; print}' | egrep -v ^# > AshGos_AspNid")

def main():
    create_db()
    blast()
    split()

main()
