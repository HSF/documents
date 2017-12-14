#! /usr/bin/env python
#
# Process CWP signatory list into a LaTeX author list

import os
import re
import sys

def main():
    author_file = "authors.txt"
    footnote_file = "footnotes.txt"

    # Open and process the authors file
    with open(author_file) as author_fh, open(footnote_file) as footnote_fh:
        author_list = []
        for author_line in author_fh:
            if author_line.startswith("#"):
                continue
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
                     "affiliation": affiliation.replace("&", "\&"),
                     "role": role.replace("&", "\&"),}
                    )
            except:
                print "Got an exception processing this line:", author_line
        
        print author_list

    # Generate the map to people's institutes
    affiliation_map = {}
    for author in author_list:
        if author["affiliation"] in affiliation_map:
            continue
        affiliation_map[author["affiliation"]] = {
            "address": author["affiliation"],
            }
    # Alphabetise and assign footnote marks
    sorted_affiliations = affiliation_map.keys()[:]
    sorted_affiliations.sort()
    for footnote_mark, affiliation in enumerate(sorted_affiliations, start=1):
        affiliation_map[affiliation]["footnotemark"] = str(footnote_mark)
    
        
    # Write out the latex author file
    with open("authors.tex", "w") as output:
        for author in author_list:
            print >>output, author["surname"] +", "  + \
            author["forename"] + "$^{" + str(affiliation_map[author["affiliation"]]["footnotemark"]) + "}$" +\
            ("" if author == author_list[-1] else ";")
            #if author["role"]:
            #    print >>output, "(" + author["role"] + ")"
        print >>output
        for affiliation in sorted_affiliations:
            print affiliation
            print >>output, "\par {\\footnotesize $^{" + str(affiliation_map[affiliation]["footnotemark"]) + "}$", affiliation_map[affiliation]["address"], "}"


if __name__ == '__main__':
    main()

