# HL-LHC Computing Review: Common Tools and Community Software

This directory contains the sources of the HSF submission to the May 2020 HL-LHC
Computing and Software review by the LHCC.

## Instructions

To regenerate this document:

1. Run the `a2tex.py` script which merges the sources of author information and
   will generate the `authors.tex` input file.
2. Generate the PDF of the document with the usual LaTeX chain of commands:
    1. `pdflatex ctcs`
    2. `biber ctcs`
    3. `pdflatex ctcs`
    4. `pdflatex ctcs` (if references/labels change)

### Dependencies

The `a2tex.py` script needs Python3.

For the references it is necessary to use `biber`, rather than `bibtex`, so a
modern installation of TeX is required.
