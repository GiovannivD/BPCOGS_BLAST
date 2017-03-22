'''BLAST SCRIPT V1.0'''
import os

def create_db(schimmels):
    """Maakt van elke schimmel een lokale database aan. Dit wordt
    gedaan met bash script #formatdb#. Het aanmaken van deze databases
    is nodig voor het BLASTen."""

    for schimmel in schimmels:
        db_string = "formatdb -i Proteomes/Proteoom_" + schimmel + ".fasta -pT"
        os.system(db_string)


def blast(schimmels):
    """Hier wordt elke BLAST uitgevoerd, elk proteoom wordt tegen elk
    proteoom geBLAST en vice versa. Dit wordt gedaan d.m.v. 3
    for-loops.

    De middelste loop neemt de lengte van de schimmel lijst en loopt
    hier doorheen. De binnenste for-loop loopt altijd eentje voor op de
    de middelste for-loop: 'i + 1'. Zo kan de eerste schimmel met 'i'
    en de tweede schimmel met 'j' worden geselecteerd uit de lijst
    *schimmels*.

    In *file_schim_1* en *file_schim_2* worden delen van de filenaam
    van de op dat moment geselecteerde schimmels opgeslagen. In
    *file_naam* worden deze twee strings toegevoegd tot 1 string.
    Vervolgens wordt deze filenaam aan een lijst toegevoegd zodat deze
    filenames later weer gebruikt kunnen worden.

    In *blast_string* wordt de string met de juiste parameters
    opgeslagen die nodig zijn voor een BLAST. Alle BLAST-files worden
    in de map 'BLAST' opgeslagen. Voordat de BLAST wordt uitgevoerd is
    een print statement toegevoegd zodat de gebruiker kan zien waar het
    programma is gebleven met BLASTen.

    Nadat de binnenste twee for-loops klaar zijn zal de lijst
    *schimmels* worden omgedraait. Dit wordt gedaan omdat er heen én
    weer moet worden geBLAST. Er wordt dan dus weer hetzelfde gedaan
    maar dan met de schimmels andersom. Uiteindelijk returned de
    functie de *file_list*.

    @Note: BLASTen kan 48-72 uur duren."""

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

                print("BLAST-ing " + file_name + "...")
                os.system(blast_string)

        schimmels = schimmels[::-1]

    return file_list


def hits(b_file_list):
    """Haalt de eerste hits uit een BLAST en zet deze in een aparte
    file in de map 'HITS'. Dit wordt gedaan voor elke BLAST die is
    uitgevoerd.

    Er wordt d.m.v. een for-loop door de lijst geloopt waar
    alle file-names in staan. Vervolgens wordt een file-name gebruikt
    in de bash code om de juiste file op te halen. De bash code haalt
    vervolgens uit deze BLAST file de bovenste hits van elk eiwit. Deze
    hits worden opgeslagen in een nieuwe file: 'hits_' + file_name.
    Deze files worden opgeslagen in de map 'HITS'."""

    for file_name in b_file_list:
        filter_string = "awk '{print $1, $2, $11}' " \
                        "BLAST/blast_" + file_name + \
                        ".txt | egrep -A1 ^# | egrep \"^[^#-]\" >" \
                        "> HITS/hits_" + file_name + ".txt"

        os.system(filter_string)


def directional_hit(b_file_list):
    """Vergelijkt de beste hits met elkaar om de best directional hits
    te vinden. Als een hit heen en weer in een schimmel voorkomt dan is
    dit een best directional hit.

    """
    while len(b_file_list) > 0:
        for x in b_file_list:
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


def main():
    """De mappen BLAST, HITS, BDH en Modified worden aangemaakt. Er
    wordt een lijst met alle schimmels aangemaakt. Alle vier de
    functies worden aangeroepen.

    * b_file_list bevat de file names van de BLAST files."""

    os.system("mkdir -p BLAST HITS BDH Modified")
    schimmel_list = ["Ashbya_gossypii", "Aspergillus_nidulans",
                     "Neurospora_crassa", "Penicillium_canescens",
                     "Penicillium_raistrickii", "Phanerochaete_chrysosporium",
                     "Rhizoctonia_solani", "Saccharomyces_cerevisea",
                     "Trichoderma_atroviride", "Trichoderma_virens"]

    create_db(schimmel_list)
    b_file_list = blast(schimmel_list)
    hits(b_file_list)
    directional_hit(b_file_list)

main()
