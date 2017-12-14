#! /usr/bin/env python
#
# Process CWP signatory list into a LaTeX author list

# The data source is expected to be 
#   Lastname, Firstname - Institution (1) [- Role ]
# If there are multiple affiliations, separate with &

import os
import re
import sys

def main():
    author_file = "authors.txt"
    footnote_file = "footnotes.txt"
    affiliation_address_file = "address.txt"
    
    # Open and process the authors file
    with open(author_file) as author_fh:
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
                print "Got an exception(", e, ") processing this line:", author_line
                raise
    #print author_list
    
    # Generate the map to people's institutes
    institute_address = {}
    with open(affiliation_address_file) as address_fh:
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
    sorted_affiliations = affiliation_map.keys()[:]
    sorted_affiliations.sort()
    for footnote_mark, affiliation in enumerate(sorted_affiliations, start=1):
        affiliation_map[affiliation]["footnotemark"] = str(footnote_mark)
    
    # Parse and assign footnotes
    with open(footnote_file) as footnote_fh:
        footnote_map = {}
        footnote_symbols = "abcdefghijklmnopqrstuvwxyz"
        footnotemark_index = 0
        for footnote_line in footnote_fh:
            footnote_line = footnote_line.strip()
            if footnote_line.startswith("#") or footnote_line == "":
                continue
            number, note = footnote_line.split(" ", 1)
            number = number.rstrip(".")
            footnote_map[number] = {
                "note": note.replace("&", "\&").replace("_", "\_"),
                "footnotemark": footnote_symbols[footnotemark_index],
                }
            footnotemark_index += 1
    sorted_footnotes = footnote_map.keys()[:]
    sorted_footnotes.sort(cmp=lambda x,y: cmp(int(x), int(y)))
    #print footnote_map
        
        
    # Write out the latex author file
    with open("authors.tex", "w") as output:
        for author in author_list:
            affiliation_list = ",".join([ str(affiliation_map[affiliation]["footnotemark"]) for affiliation in author["affiliation"] ])
            if author["footnotes"]:
                footnote_list = ",".join( [ footnote_map[footnote]["footnotemark"] for footnote in author["footnotes"] ])
                affiliation_list = affiliation_list + "," + footnote_list
            print >>output, author["surname"] +", "  + \
            author["forename"] + "$^{" + affiliation_list + "}$" +\
            ("" if author == author_list[-1] else ";")
            #if author["role"]:
            #    print >>output, "(" + author["role"] + ")"
        print >>output, "\\bigskip"
        for affiliation in sorted_affiliations:
            print >>output, "\\par {\\footnotesize $^{" + str(affiliation_map[affiliation]["footnotemark"]) + "}$", affiliation_map[affiliation]["address"], "}"
        print >>output, "\\bigskip"
        for footnote in sorted_footnotes:
            print >>output, "\\par {\\footnotesize $^{" + footnote_map[footnote]["footnotemark"] + "}$", footnote_map[footnote]["note"], "}"


if __name__ == '__main__':
    main()

