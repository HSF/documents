#! /usr/bin/env python
#
# Process CWP signatory list into a LaTeX author list
#
# The data source is expected to be made of 3 text files:
#    - authors.txt: the list of signers in the following format: Lastname, Firstname - AffiliationKey (i) [- Role ]
#      with i a footnote number. If there are multiple affiliations, separate AffiliationKeys with &.
#    - footnotes:txt: the list of footnotes. There must be one footnote per line starting with 'i.'
#    - address.txt: the affiliation list with the following format: AffilitationKey: Affiliation text
#      AffiliationKey must not contain any space.
#
# These 3 files are typically built from the Google Docs https://docs.google.com/document/d/1tBXwlNnQsxxZA3gVS1_KSpa8wRXGyk250EIsJwJ2T34/edit#

import os
import re
import sys
from operator import attrgetter
import argparse

# Define some constants related to application exit status
EXIT_STATUS_SUCCESS = 0
EXIT_STATUS_OPTION_ERROR = 3
EXIT_STATUS_FAILURE = 5

# Default input files
AUTHOR_FILE_DEFAULT = "authors.txt"
FOOTNOTE_FILE_DEFAULT = "footnotes.txt"
AFFILIATION_ADDRESS_FILE_DEFAULT = "address.txt"
LATEX_AUTHOR_FILE_DEFAULT = "authors.tex"


class Footnote():
    def __init__(self, number_str, text):
        footnote_symbols = "abcdefghijklmnopqrstuvwxyz"
        self.mark = footnote_symbols[int(number_str)-1]
        self.text = text
    def __repr__(self):
        return repr((self.mark, self.text))

def main():

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--authors", dest="authors", default=AUTHOR_FILE_DEFAULT,
                            help="File containining author list (D: {})".format(AUTHOR_FILE_DEFAULT))
        parser.add_argument("--footnotes", dest="footnotes", default=FOOTNOTE_FILE_DEFAULT,
                            help="File containining footnote list (D: {})".format(FOOTNOTE_FILE_DEFAULT))
        parser.add_argument("--affiliations", dest="affiliations", default=AFFILIATION_ADDRESS_FILE_DEFAULT,
                            help="File containining affiliation list (D: {})".format(AFFILIATION_ADDRESS_FILE_DEFAULT))
        parser.add_argument("--output", dest="output_file", default=LATEX_AUTHOR_FILE_DEFAULT,
                            help="Output Latex file (D: {})".format(LATEX_AUTHOR_FILE_DEFAULT))
        options = parser.parse_args()
    except Exception as e:
        parser.invalid_option_value('Parsing error: {}'.format(e.msg))
        return EXIT_STATUS_OPTION_ERROR


    # Open and process the authors file
    with open(options.authors, encoding='utf-8') as author_fh:
        author_list = []
        for author_line in author_fh:
            author_line = author_line.strip()
            if author_line.startswith("#") or author_line == "":
                continue
            # Find any footnotes that the author wanted to add
            footnotes_search = re.search(r"\(([\d,]+)\)$", author_line)
            if footnotes_search:
                footnotes = footnotes_search.group(1).split(",")
                author_line = author_line.replace(footnotes_search.group(), "")
            else:
                footnotes = []
            author_elements = [ el.strip() for el in author_line.split(" - ") ]
            try:
                surname, forename = [ el.strip() for el in author_elements[0].split(",", 1) ]
                affiliation = author_elements[1]
                if len(author_elements) == 3:
                    role = author_elements[2]
                else:
                    role = ""
                author_list.append( {"surname": surname,
                     "forename": forename,
                     "affiliation": [ el.strip() for el in affiliation.split("&") ],
                     "role": role.replace("&", "\&"),
                     "footnotes": footnotes,}
                    )
            except Exception as e:
                print ("Got an exception({}) processing this line: {}".format(e, author_line))
                raise
    #print author_list
    
    # Generate the map to people's institutes
    institute_address = {}
    with open(options.affiliations, encoding='utf-8') as address_fh:
        for affiliation_line in address_fh:
            affiliation_line = affiliation_line.strip()
            if affiliation_line.startswith("#") or affiliation_line == "":
                continue
            institute, address = affiliation_line.split(": ", 1)
            institute_address[institute] = address
    #print institute_address
    
    affiliation_map = {}
    for author in author_list:
        for affiliation in author["affiliation"]:
            if affiliation in affiliation_map:
                continue
            affiliation_map[affiliation] = {
                "address": (institute_address[affiliation] if affiliation in institute_address else affiliation),
            }
    #print affiliation_map        
    
    # Alphabetise and assign footnote marks
    sorted_affiliations = sorted(affiliation_map)
    for footnote_mark, affiliation in enumerate(sorted_affiliations, start=1):
        affiliation_map[affiliation]["footnotemark"] = str(footnote_mark)
    
    # Parse and assign footnotes
    with open(options.footnotes, encoding='utf-8') as footnote_fh:
        footnote_list = []
        for footnote_line in footnote_fh:
            footnote_line = footnote_line.strip()
            if footnote_line.startswith("#") or footnote_line == "":
                continue
            number, note = footnote_line.split(" ", 1)
            number = number.rstrip(".")
            footnote_list.append(Footnote(number, note))
    sorted_footnotes = sorted(footnote_list, key=lambda footnote: footnote.mark)
    #print footnote_map
        
        
    # Write out the latex author file
    with open(options.output_file, "w", encoding="utf-8") as output:
        for author in author_list:
            affiliation_list = ",".join([ str(affiliation_map[affiliation]["footnotemark"]) for affiliation in author["affiliation"] ])
            if author["footnotes"]:
                footnote_str = ",".join( [ footnote_list[int(id)-1].mark for id in author["footnotes"] ])
                affiliation_list = affiliation_list + "," + footnote_str
            if author == author_list[-1]:
                eol_str = ""
            else:
                eol_str = ";"
            print ("{}, {} $^{{{}}}${}".format(author["surname"],
                                               author["forename"],
                                               affiliation_list,
                                               eol_str),
                   file=output)
            #if author["role"]:
            #    print >>output, "(" + author["role"] + ")"
        print ("\\bigskip", file=output)
        for affiliation in sorted_affiliations:
            print ("\\par {{\\footnotesize $^{{{}}}$ {}}}".format(str(affiliation_map[affiliation]["footnotemark"]),
                                                               affiliation_map[affiliation]["address"]),
                   file=output)
        print ("\\bigskip", file=output)
        for footnote in sorted_footnotes:
            print ("\\par {{\\footnotesize $^{{{}}}$ {}}}".format(footnote.mark,
                                                                 footnote.text),
                   file=output)


if __name__ == '__main__':
    main()

