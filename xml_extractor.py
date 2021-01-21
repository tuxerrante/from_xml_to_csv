from xml.dom import minidom
import argparse
import csv
import sys
import os

def create_arg_parser():
    # Creates and returns the ArgumentParser object
    parser = argparse.ArgumentParser(description='Analysis.xml parser')
    parser.add_argument('inputDirectory', help='Path to the input directory.')
    return parser


arg_parser  = create_arg_parser()
parsed_args = arg_parser.parse_args(sys.argv[1:])
if os.path.exists(parsed_args.inputDirectory):
    print("Path exists, starting the parser..")

xml_dir = parsed_args.inputDirectory

### INITIALIZE CSV FILE
header="NOME FILE,RF,VALUE,COUNT (E-G-F-P-X),SENTENCE\n"
with open(r"parsed_analysis.csv", 'w') as f:
        f.write( header )


for dirpath, dirnames, filenames in os.walk(xml_dir):
    for filename in [f for f in filenames if f == "analysis.xml"]:
        
        xml_file = os.path.join(dirpath, filename)
        print(xml_file)

        ### CHECK FOR VOID FILES
        with open(xml_file, encoding="utf8") as input_file:
            lines = len(input_file.readlines())
            if lines <= 1:
                print("> WARNING, file {} is void!".format(xml_file))
                continue

        mydoc = minidom.parse(xml_file)

        riskFactor_nodes = mydoc.getElementsByTagName('riskFactors')
        entry_list       = riskFactor_nodes[0].getElementsByTagName('entry') 

        fields=[]
                
        for entry in entry_list:
            FILE_NAME = xml_file
            RF        = entry.getElementsByTagName('value')[0].attributes['name'].value
            VALUE     = entry.getElementsByTagName('value')[0].attributes['value'].value
            SENTENCE  = ""
            COUNT_TMP = [0, 0, 0, 0, 0]    # E, G, F, P, X

            # sentence_list = entry.getElementsByTagName('sentences')[0]
            s = entry.getElementsByTagName('s')
            sentence_list = []
            riskFactorValue = ""

            for s_node in s:
                if s_node.hasAttribute('riskFactorValue'):
                    riskFactorValue     = s_node.attributes['riskFactorValue'].value
                    sentence_clean_text = s_node.getElementsByTagName('text')[0].firstChild.nodeValue.replace("\n", " ").replace("\"", "'")
                    sentence_list      += [ riskFactorValue +" - "+ sentence_clean_text ]
                    
                    if riskFactorValue == "E":
                        COUNT_TMP[0] += 1
                    elif riskFactorValue == "G":
                        COUNT_TMP[1] += 1
                    elif riskFactorValue == "F":
                        COUNT_TMP[2] += 1
                    elif riskFactorValue == "P":
                        COUNT_TMP[3] += 1
                    elif riskFactorValue == "X":
                        COUNT_TMP[4] += 1

                else:
                    print(" > Entry {} has no sentence".format(RF))
            
            SENTENCE  = "-----".join(map(str, sentence_list ))
            SENTENCE  = "\"" + SENTENCE + "\""

            ### Per ogni sentence/s: numero di E,G,F,P,U            
            if RF != "U":
                COUNT = "-".join(map(str, COUNT_TMP))
            else:
                COUNT = 0


            fields    = ','.join(map(str, [FILE_NAME,RF, VALUE, COUNT, SENTENCE]))

            with open(r"parsed_analysis.csv", 'a') as f:
                f.write( fields + "\n")

