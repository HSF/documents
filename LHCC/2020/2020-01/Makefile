# Simple makefile that will regenerate the CSTS PDF document from inputs

all: ctcs.pdf

ctcs.pdf: ctcs.tex ctcs.bib authors.tex input_analysis.tex input_introduction.tex input_simulation.tex input_generators.tex input_recoTrigger.tex input_summary.tex
	pdflatex ctcs
	biber ctcs
	pdflatex ctcs
	pdflatex ctcs

authors.tex: a2tex.py authors.txt address.txt footnotes.txt
	./a2tex.py

clean:
	rm -f ctcs.pdf authors.tex

