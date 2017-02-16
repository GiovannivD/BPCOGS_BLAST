'''BLAST SCRIPT V1.0'''
import os

def blast():
    os.system("formatdb -i Proteomes/Proteoom_Phanerochaete_chrysosporium.fasta"
              " -pF")
    os.system("rm formatdb.log")
    print "hoi"

def main():
    blast()

main()
