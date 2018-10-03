#! /usr/bin/env python
#
# Process CWP signatory list into a LaTeX author list
#
# The data source is expected to be made of 3 text files:
#    - authors.txt: the list of signers in the following format: Lastname, Firstname - AffiliationKey [- Role ] (i)
#      with i a footnote number. If there are multiple affiliations, separate AffiliationKeys with &.
#    - footnotes:txt: the list of footnotes. There must be one footnote per line starting with 'i.'
#    - address.txt: the affiliation list with the following format: AffilitationKey: Affiliation text
#      AffiliationKey must not contain any space.
#
# These 3 files are typically built from the Google Docs https://docs.google.com/document/d/1tBXwlNnQsxxZA3gVS1_KSpa8wRXGyk250EIsJwJ2T34
#
# Note: this script requires Python >= 3.5
#
# Initial version written by Graeme Stewart (graeme.andrew.stewart@cern.ch) and Michel Jouvin (jouvin@lal.in2p3.fr)

import sys
PYTHON_MIN = (2, 6)
major, minor, _, _, _ = sys.version_info
if (major, minor) < PYTHON_MIN:
    python_min_str = '.'.join(str(x) for x in PYTHON_MIN)
    # Keep old formatter syntax to be sure it works with old version of Python
    print ("This script requires Python %s or later" % python_min_str)
    sys.exit(2)

import os
import re
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
ARXIV_AUTHOR_FILE_DEFAULT = "arxiv.txt"


class Footnote():
    def __init__(self, number_str, text):
        footnote_symbols = "abcdefghijklmnopqrstuvwxyz"
        self.mark = footnote_symbols[int(number_str)-1]
        self.text = text
    def __repr__(self):
        return repr((self.mark, self.text))

class Author():
    def __init__(self, author_line):
        footnotes_search = re.search(r"\((?P<footnotes>[\d,]+)\)$", author_line)
        if footnotes_search:
            self.footnotes = footnotes_search.group('footnotes').split(",")
            author_line = author_line.replace(footnotes_search.group(), "")
        else:
            self.footnotes = []
        author_elements = [el.strip() for el in author_line.split(" - ")]
        print author_elements
#        try:
        self.surname, self.forename = [el.strip() for el in author_elements[0].split(",", 1)]
        self.affiliations = [el.strip() for el in author_elements[1].split("&")]
        if len(author_elements) == 3:
            self.role = author_elements[2]
        else:
            self.role = ""
#        except Exception as e:
#            raise Exeption("Got an exception({}) processing line: {}".format(e, author_line))


class Affiliation():
    def __init__(self,address):
        self.address = address
        self.mark = ''

    def set_mark(self, i):
        self.mark = str(i)

def latex_escape(string):
    """
    Function to escape latex reserved characters
    :param string: the string containing the characters to escape
    :return: the escaped string
    """

    CHARS_TO_ESCAPE_PATTERN = re.compile(r'(?<!\\)(?P<char>[&%\$#_{}])')
    SPECIAL_LATEX_CHARS = {'~':'$\\\\textasciitilde$',
                           '^':'$\\\\textasciicircum$'}
    # Do not attempt to escape \ as it may have been added as an escape character
    # and is unlikely to be present in an affiliation or footnote...
    # If it is present, if will have to be escaped manually
    #                       '\\':'$\\\\textbackslash$'}
    # Escape all reserved characters that can be escaped
    string = CHARS_TO_ESCAPE_PATTERN.sub('\\\\\g<char>', string)
    # Then replace special chars
    for special_char, repl in SPECIAL_LATEX_CHARS.items():
       string = re.sub(re.escape(special_char), repl, string)
    return string

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
        parser.add_argument("--arxivoutput", dest="arxiv_output_file", default=ARXIV_AUTHOR_FILE_DEFAULT,
                            help="Output arXiv author list (D: {})".format(ARXIV_AUTHOR_FILE_DEFAULT))
        options = parser.parse_args()
    except Exception as e:
        parser.invalid_option_value('Parsing error: {}'.format(e.msg))
        return EXIT_STATUS_OPTION_ERROR


    # Open and process the authors file
    with open(options.authors) as author_fh:
#    with open(options.authors, encoding='utf-8') as author_fh:
        author_list = []
        for author_line in author_fh:
            author_line = author_line.strip()
            if author_line.startswith("#") or author_line == "":
                continue
            author_list.append(Author(author_line))

    # Generate the map to people's institutes
    institute_address = {}
    with open(options.affiliations) as address_fh:
#    with open(options.affiliations, encoding='utf-8') as address_fh:
        for affiliation_line in address_fh:
            affiliation_line = affiliation_line.strip()
            if affiliation_line.startswith("#") or affiliation_line == "":
                continue
            institute, address = affiliation_line.split(": ", 1)
            institute_address[institute] = address

    affiliation_map = {}
    affiliation_listing = []
    for author in sorted(author_list, key=lambda author: author.surname):
#    for author in author_list:
        for affiliation in author.affiliations:
            if affiliation not in affiliation_map:
                if affiliation in institute_address:
                    affiliation_map[affiliation] = Affiliation(institute_address[affiliation])
                    affiliation_listing.append(affiliation)
                else:
                    print Exception('Affiliation {} not defined'.format(affiliation))

    # Alphabetise and assign footnote marks
    sorted_affiliations = sorted(affiliation_map)
#    print sorted_affiliations
#    for footnote_mark, affiliation in enumerate(sorted_affiliations, start=1):
#        affiliation_map[affiliation].set_mark(footnote_mark)
    for footnote_mark, affiliation in enumerate(affiliation_listing, start=1):
        affiliation_map[affiliation].set_mark(footnote_mark)
    
    # Parse and assign footnotes
    with open(options.footnotes) as footnote_fh:
#    with open(options.footnotes, encoding='utf-8') as footnote_fh:
        footnote_list = []
        for footnote_line in footnote_fh:
            footnote_line = footnote_line.strip()
            if footnote_line.startswith("#") or footnote_line == "":
                continue
            number, note = footnote_line.split(" ", 1)
            number = number.rstrip(".")
            footnote_list.append(Footnote(number, note))
    sorted_footnotes = sorted(footnote_list, key=lambda footnote: footnote.mark)

    # Write out the author list to copy into the arXiv author file
    with open(options.arxiv_output_file, "w") as arxivoutput:
#    with open(options.arxiv_output_file, "w", encoding="utf-8") as arxivoutput:
        arxivoutput.write("HEP Software Foundation: "+ ", ".join([ "{} {}".format(author.forename, author.surname) 
                                                                   for author in  sorted(author_list, key=lambda author: author.surname) ]))
#        print("HEP Software Foundation: ", ", ".join([ "{} {}".format(author.forename, author.surname) 
#                                                      for author in  sorted(author_list, key=lambda author: author.surname) ]),file=arxivoutput)
        
    # Write out the latex author file
#    with open(options.output_file, "w", encoding="utf-8") as output:
    with open(options.output_file, "w") as output:
        for author in sorted(author_list, key=lambda author: author.surname):
            affiliation_list = ",".join([ affiliation_map[affiliation].mark for affiliation in author.affiliations ])
            if author.footnotes:
                footnote_str = ",".join( [ footnote_list[int(id)-1].mark for id in author.footnotes ])
                affiliation_list = affiliation_list + "," + footnote_str
            if author == author_list[-1]:
                eol_str = ""
            else:
                eol_str = ";"
            output.write ("{}, {}$^{{{}}}${}\n".format(author.surname,
                                               author.forename,
                                               affiliation_list,
                                               eol_str))
#            print ("{}, {}$^{{{}}}${}".format(author.surname,
#                                               author.forename,
#                                               affiliation_list,
#                                               eol_str),
#                   file=output)

#        print ("\\bigskip", file=output)
        output.write ("\\bigskip \n")
#        for affiliation in sorted_affiliations:
        for affiliation in affiliation_listing:
            output.write("\\par {{\\footnotesize $^{{{}}}$ {}}}\n".format(str(affiliation_map[affiliation].mark),
                                                                  latex_escape(affiliation_map[affiliation].address)))
#                   file=output)
#            print ("\\par {{\\footnotesize $^{{{}}}$ {}}}".format(str(affiliation_map[affiliation].mark),
#                                                                  latex_escape(affiliation_map[affiliation].address)),
#                   file=output)

        output.write("\\bigskip\n")
#        print ("\\bigskip", file=output)
        for footnote in sorted_footnotes:
            output.write("\\par {{\\footnotesize $^{{{}}}$ {}}}\n".format(footnote.mark,
                                                                  latex_escape(footnote.text)))

#            print ("\\par {{\\footnotesize $^{{{}}}$ {}}}".format(footnote.mark,
#                                                                  latex_escape(footnote.text)),
#                   file=output)


if __name__ == '__main__':
    main()

