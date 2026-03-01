# Makefile for building the bachelor thesis

MAIN = main
TEX = pdflatex
BIB = biber

.PHONY: all clean build

all: build

build:
	cd thesis && $(TEX) $(MAIN).tex
	cd thesis && $(BIB) $(MAIN)
	cd thesis && $(TEX) $(MAIN).tex
	cd thesis && $(TEX) $(MAIN).tex

clean:
	cd thesis && rm -f *.aux *.bbl *.blg *.log *.out *.toc *.bcf *.run.xml *.synctex.gz

distclean: clean
	cd thesis && rm -f $(MAIN).pdf

view:
	cd thesis && xdg-open $(MAIN).pdf 2>/dev/null || open $(MAIN).pdf
