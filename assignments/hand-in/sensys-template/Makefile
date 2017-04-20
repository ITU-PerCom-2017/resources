DOC=sensys-full

all:
	pdflatex $(DOC).tex
	bibtex $(DOC)
	pdflatex $(DOC).tex
	pdflatex $(DOC).tex

clean:
	rm -f $(DOC).blg $(DOC).bbl $(DOC).aux $(DOC).log $(DOC).pdf
